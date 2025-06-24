import cv2
import mediapipe as mp
import numpy as np
from openai import OpenAI
import time
import json
import os
from datetime import timedelta
import pandas as pd
from pathlib import Path
from moviepy import VideoFileClip
import whisper
from gtts import gTTS
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
import gc
from tqdm import tqdm
import logging
from functools import lru_cache
import threading
from queue import Queue
import warnings
warnings.filterwarnings('ignore')
from improved_facial_emotion import call_facial_emotion_functions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("body_language_analyzer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BodyLanguageAnalyzer:
    def __init__(self, api_key):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            enable_segmentation=True
        )
        
        # Initialize MediaPipe Face Mesh for facial expressions
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.7,  # Increased from 0.5 for better detection
            min_tracking_confidence=0.7,   # Increased from 0.5 for better tracking
            refine_landmarks=True          # Added to improve landmark accuracy
        )
        
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize OpenAI client with API key
        self.client = OpenAI(api_key=api_key)
        
        # Store time series data
        self.time_series_data = []
        self.frame_count = 0
        self.fps = 0
        
        # Store facial expression data
        self.facial_expressions = []
        
        # Store movement data
        self.movement_history = []
        self.repetitive_movements = []
        self.stimming_behaviors = []
        self.meltdown_precursors = []
        
        # Thread-safe queue for processing results
        self.result_queue = Queue()
        
        # Lock for thread safety
        self.lock = threading.Lock()
        
    def calculate_angles(self, landmarks, image_width, image_height):
        """Calculate important body angles for action recognition."""
        angles = {}
        
        # Convert normalized coordinates to pixel coordinates
        def to_pixels(x, y):
            return (int(x * image_width), int(y * image_height))
        
        # Calculate shoulder angle
        left_shoulder = np.array(to_pixels(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                                         landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y))
        right_shoulder = np.array(to_pixels(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                                          landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y))
        left_elbow = np.array(to_pixels(landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW].x,
                                      landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW].y))
        right_elbow = np.array(to_pixels(landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                                       landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW].y))
        
        # Calculate vectors
        left_arm_vec = left_elbow - left_shoulder
        right_arm_vec = right_elbow - right_shoulder
        
        # Calculate angles
        angles['left_arm'] = np.degrees(np.arctan2(left_arm_vec[1], left_arm_vec[0]))
        angles['right_arm'] = np.degrees(np.arctan2(right_arm_vec[1], right_arm_vec[0]))
        
        return angles
        
    def detect_facial_expression(self, frame, face_results):
        """Detect and classify facial expressions from face mesh landmarks with high accuracy."""
        if not face_results.multi_face_landmarks:
            return None
            
        face_landmarks = face_results.multi_face_landmarks[0].landmark
        
        # Define key facial landmarks with more precision
        # Mouth corners
        left_mouth = face_landmarks[61]
        right_mouth = face_landmarks[291]
        
        # Upper lip
        upper_lip = face_landmarks[0]
        
        # Lower lip
        lower_lip = face_landmarks[17]
        
        # Eyebrows - using multiple points for better accuracy
        left_eyebrow_inner = face_landmarks[105]
        left_eyebrow_outer = face_landmarks[66]
        right_eyebrow_inner = face_landmarks[334]
        right_eyebrow_outer = face_landmarks[296]
        
        # Eyes - using multiple points for better accuracy
        left_eye_top = face_landmarks[159]
        left_eye_bottom = face_landmarks[145]
        left_eye_left = face_landmarks[133]
        left_eye_right = face_landmarks[33]
        
        right_eye_top = face_landmarks[386]
        right_eye_bottom = face_landmarks[374]
        right_eye_left = face_landmarks[362]
        right_eye_right = face_landmarks[263]
        
        # Additional landmarks for better expression detection
        # Nose tip
        nose_tip = face_landmarks[4]
        
        # Cheeks
        left_cheek = face_landmarks[123]
        right_cheek = face_landmarks[352]
        
        # Calculate facial metrics with improved precision
        mouth_width = abs(right_mouth.x - left_mouth.x)
        mouth_height = abs(upper_lip.y - lower_lip.y)
        mouth_ratio = mouth_height / mouth_width if mouth_width > 0 else 0
        
        # Mouth corner position relative to nose
        left_mouth_height = left_mouth.y - nose_tip.y
        right_mouth_height = right_mouth.y - nose_tip.y
        
        # Eyebrow height relative to eyes - using average of inner and outer points
        left_eyebrow_height_inner = left_eyebrow_inner.y - left_eye_top.y
        left_eyebrow_height_outer = left_eyebrow_outer.y - left_eye_top.y
        left_eyebrow_height = (left_eyebrow_height_inner + left_eyebrow_height_outer) / 2
        
        right_eyebrow_height_inner = right_eyebrow_inner.y - right_eye_top.y
        right_eyebrow_height_outer = right_eyebrow_outer.y - right_eye_top.y
        right_eyebrow_height = (right_eyebrow_height_inner + right_eyebrow_height_outer) / 2
        
        # Eye openness - using width and height for better accuracy
        left_eye_width = abs(left_eye_right.x - left_eye_left.x)
        left_eye_height = abs(left_eye_top.y - left_eye_bottom.y)
        left_eye_openness = left_eye_height / left_eye_width if left_eye_width > 0 else 0
        
        right_eye_width = abs(right_eye_right.x - right_eye_left.x)
        right_eye_height = abs(right_eye_top.y - right_eye_bottom.y)
        right_eye_openness = right_eye_height / right_eye_width if right_eye_width > 0 else 0
        
        # Calculate mouth corner angles (for detecting smile vs. frown)
        mouth_corner_angle = 0
        if left_mouth_height != 0 and right_mouth_height != 0:
            # Positive angle indicates upturned corners (smile), negative indicates downturned (frown)
            mouth_corner_angle = (left_mouth_height + right_mouth_height) / 2
        
        # Calculate asymmetry for better emotion detection
        eyebrow_asymmetry = abs(left_eyebrow_height - right_eyebrow_height)
        eye_asymmetry = abs(left_eye_openness - right_eye_openness)
        
        # Classify expression based on metrics with improved thresholds
        expression = "neutral"
        confidence = 0.5
        
        # Calculate emotion scores for each expression
        emotion_scores = {
            "happy": 0.0,
            "sad": 0.0,
            "surprised": 0.0,
            "angry": 0.0,
            "fearful": 0.0,
            "disgusted": 0.0,
            "neutral": 0.0
        }
        
        # Happy: upturned mouth corners, wider mouth, raised eyebrows
        if mouth_corner_angle < -0.006:  # Mouth corners are upturned
            emotion_scores["happy"] += 0.3
        if mouth_ratio > 0.12:  # Mouth is somewhat open
            emotion_scores["happy"] += 0.2
        if left_eyebrow_height < -0.003 or right_eyebrow_height < -0.003:  # Eyebrows are raised
            emotion_scores["happy"] += 0.2
        if left_eye_openness > 0.15 and right_eye_openness > 0.15:  # Eyes are open
            emotion_scores["happy"] += 0.1
        if eyebrow_asymmetry < 0.01:  # Symmetrical eyebrows
            emotion_scores["happy"] += 0.1
        if eye_asymmetry < 0.05:  # Symmetrical eyes
            emotion_scores["happy"] += 0.1
        
        # Sad: downturned mouth corners, lowered eyebrows, slightly closed eyes
        if mouth_corner_angle > 0.006:  # Mouth corners are downturned
            emotion_scores["sad"] += 0.3
        if left_eyebrow_height > 0.006 or right_eyebrow_height > 0.006:  # Eyebrows are lowered
            emotion_scores["sad"] += 0.2
        if left_eye_openness < 0.15 or right_eye_openness < 0.15:  # Eyes are slightly closed
            emotion_scores["sad"] += 0.2
        if mouth_ratio < 0.1:  # Closed mouth
            emotion_scores["sad"] += 0.1
        if eyebrow_asymmetry < 0.01:  # Symmetrical eyebrows
            emotion_scores["sad"] += 0.1
        if eye_asymmetry < 0.05:  # Symmetrical eyes
            emotion_scores["sad"] += 0.1
        
        # Surprised: raised eyebrows, wide eyes, open mouth
        if left_eyebrow_height < -0.012 and right_eyebrow_height < -0.012:  # Both eyebrows raised
            emotion_scores["surprised"] += 0.3
        if left_eye_openness > 0.2 and right_eye_openness > 0.2:  # Wide eyes
            emotion_scores["surprised"] += 0.3
        if mouth_ratio > 0.1:  # Open mouth
            emotion_scores["surprised"] += 0.2
        if eyebrow_asymmetry < 0.01:  # Symmetrical eyebrows
            emotion_scores["surprised"] += 0.1
        if eye_asymmetry < 0.05:  # Symmetrical eyes
            emotion_scores["surprised"] += 0.1
        
        # Angry: lowered eyebrows, narrowed eyes, tight mouth
        if left_eyebrow_height > 0.006 and right_eyebrow_height > 0.006:  # Both eyebrows lowered
            emotion_scores["angry"] += 0.3
        if left_eye_openness < 0.1 and right_eye_openness < 0.1:  # Narrowed eyes
            emotion_scores["angry"] += 0.3
        if mouth_ratio < 0.1:  # Tight mouth
            emotion_scores["angry"] += 0.2
        if eyebrow_asymmetry < 0.01:  # Symmetrical eyebrows
            emotion_scores["angry"] += 0.1
        if eye_asymmetry < 0.05:  # Symmetrical eyes
            emotion_scores["angry"] += 0.1
        
        # Fearful: raised eyebrows, wide eyes, slightly open mouth
        if left_eyebrow_height < -0.006 and right_eyebrow_height < -0.006:  # Both eyebrows raised
            emotion_scores["fearful"] += 0.3
        if left_eye_openness > 0.15 and right_eye_openness > 0.15:  # Wide eyes
            emotion_scores["fearful"] += 0.3
        if mouth_ratio > 0.06 and mouth_ratio < 0.3:  # Slightly open mouth
            emotion_scores["fearful"] += 0.2
        if eyebrow_asymmetry < 0.01:  # Symmetrical eyebrows
            emotion_scores["fearful"] += 0.1
        if eye_asymmetry < 0.05:  # Symmetrical eyes
            emotion_scores["fearful"] += 0.1
        
        # Disgusted: wrinkled nose, narrowed eyes, downturned mouth
        if left_eye_openness < 0.1 and right_eye_openness < 0.1:  # Narrowed eyes
            emotion_scores["disgusted"] += 0.3
        if mouth_corner_angle > 0.003:  # Slightly downturned mouth
            emotion_scores["disgusted"] += 0.3
        if mouth_ratio < 0.06:  # Tight mouth
            emotion_scores["disgusted"] += 0.2
        if eyebrow_asymmetry < 0.01:  # Symmetrical eyebrows
            emotion_scores["disgusted"] += 0.1
        if eye_asymmetry < 0.05:  # Symmetrical eyes
            emotion_scores["disgusted"] += 0.1
        
        # Neutral: balanced features
        if abs(mouth_corner_angle) < 0.004:  # Neutral mouth
            emotion_scores["neutral"] += 0.3
        if abs(left_eyebrow_height) < 0.004 and abs(right_eyebrow_height) < 0.004:  # Neutral eyebrows
            emotion_scores["neutral"] += 0.3
        if 0.1 < left_eye_openness < 0.2 and 0.1 < right_eye_openness < 0.2:  # Normal eye openness
            emotion_scores["neutral"] += 0.2
        if mouth_ratio < 0.1:  # Closed mouth
            emotion_scores["neutral"] += 0.1
        if eyebrow_asymmetry < 0.01:  # Symmetrical eyebrows
            emotion_scores["neutral"] += 0.1
        
        # Find the emotion with the highest score
        max_score = 0
        for emotion, score in emotion_scores.items():
            if score > max_score:
                max_score = score
                expression = emotion
        
        # Calculate confidence based on the difference between the top two emotions
        sorted_scores = sorted(emotion_scores.values(), reverse=True)
        if len(sorted_scores) >= 2:
            # If there's a clear winner, confidence is high
            if sorted_scores[0] > sorted_scores[1] * 1.5:
                confidence = min(0.5 + sorted_scores[0] * 0.5, 0.95)
            # If there's a close second, confidence is moderate
            elif sorted_scores[0] > sorted_scores[1] * 1.2:
                confidence = min(0.5 + sorted_scores[0] * 0.3, 0.8)
            # If there's no clear winner, confidence is low
            else:
                confidence = min(0.5 + sorted_scores[0] * 0.2, 0.7)
        else:
            confidence = 0.5
        
        return {
            "expression": expression,
            "confidence": confidence,
            "metrics": {
                "mouth_width": mouth_width,
                "mouth_height": mouth_height,
                "mouth_ratio": mouth_ratio,
                "left_eyebrow_height": left_eyebrow_height,
                "right_eyebrow_height": right_eyebrow_height,
                "left_eye_openness": left_eye_openness,
                "right_eye_openness": right_eye_openness,
                "eyebrow_asymmetry": eyebrow_asymmetry,
                "eye_asymmetry": eye_asymmetry,
                "emotion_scores": emotion_scores
            }
        }
        
    def extract_pose_features(self, frame):
        """Extract pose features from a frame using MediaPipe with enhanced landmark detection."""
        # Get image dimensions
        image_height, image_width, _ = frame.shape
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process pose with enhanced settings
        pose_results = self.pose.process(rgb_frame)
        
        # Process facial expressions with enhanced settings
        face_results = self.face_mesh.process(rgb_frame)
        
        if not pose_results.pose_landmarks:
            return None, None, None
            
        # Extract relevant pose features with more detailed landmarks
        landmarks = pose_results.pose_landmarks.landmark
        
        # Calculate angles with more detailed points
        angles = self.calculate_angles(landmarks, image_width, image_height)
        
        # Enhanced feature extraction with more landmarks
        features = {
            'shoulders': {
                'left': {
                    'x': landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].visibility
                },
                'right': {
                    'x': landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].visibility
                }
            },
            'arms': {
                'left_elbow': {
                    'x': landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW].z,
                    'angle': angles['left_arm'],
                    'visibility': landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW].visibility
                },
                'right_elbow': {
                    'x': landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW].z,
                    'angle': angles['right_arm'],
                    'visibility': landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW].visibility
                }
            },
            'hands': {
                'left_wrist': {
                    'x': landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST].visibility
                },
                'right_wrist': {
                    'x': landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST].visibility
                }
            },
            'head': {
                'nose': {
                    'x': landmarks[self.mp_pose.PoseLandmark.NOSE].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.NOSE].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.NOSE].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.NOSE].visibility
                },
                'left_eye': {
                    'x': landmarks[self.mp_pose.PoseLandmark.LEFT_EYE].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.LEFT_EYE].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.LEFT_EYE].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.LEFT_EYE].visibility
                },
                'right_eye': {
                    'x': landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE].visibility
                }
            },
            'torso': {
                'left_hip': {
                    'x': landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].visibility
                },
                'right_hip': {
                    'x': landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].visibility
                }
            },
            'legs': {
                'left_knee': {
                    'x': landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE].visibility
                },
                'right_knee': {
                    'x': landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE].x,
                    'y': landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE].y,
                    'z': landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE].z,
                    'visibility': landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE].visibility
                }
            }
        }
        
        # Enhanced facial expression detection with more landmarks
        facial_expression = None
        if face_results.multi_face_landmarks:
            facial_expression = self.detect_facial_expression(frame, face_results)
            if facial_expression:
                # Add detailed face landmarks
                face_landmarks = face_results.multi_face_landmarks[0].landmark
                facial_expression['detailed_landmarks'] = {
                    'eyebrows': {
                        'left': [face_landmarks[i] for i in range(70, 76)],  # Left eyebrow points
                        'right': [face_landmarks[i] for i in range(300, 306)]  # Right eyebrow points
                    },
                    'eyes': {
                        'left': [face_landmarks[i] for i in range(133, 144)],  # Left eye points
                        'right': [face_landmarks[i] for i in range(362, 373)]  # Right eye points
                    },
                    'mouth': {
                        'outer': [face_landmarks[i] for i in range(61, 68)],  # Outer mouth points
                        'inner': [face_landmarks[i] for i in range(291, 298)]  # Inner mouth points
                    },
                    'jaw': [face_landmarks[i] for i in range(172, 176)]  # Jaw points
                }
                facial_expression['face_landmarks'] = face_results.multi_face_landmarks[0]
            
        return features, pose_results, facial_expression
    
    def calculate_pose_changes(self, current_features, previous_features):
        """Calculate significant changes between two pose frames."""
        # Check if current_features is None
        if current_features is None:
            return None
            
        if not previous_features:
            return current_features
            
        changes = {}
        threshold = 0.1  # Minimum change threshold to consider significant
        
        # Compare current features with previous features
        for key in current_features:
            if key not in previous_features:
                changes[key] = current_features[key]
                continue
                
            if isinstance(current_features[key], dict):
                changes[key] = {}
                for subkey in current_features[key]:
                    if subkey not in previous_features[key]:
                        changes[key][subkey] = current_features[key][subkey]
                        continue
                        
                    if isinstance(current_features[key][subkey], dict):
                        changes[key][subkey] = {}
                        for coord in ['x', 'y']:
                            if coord in current_features[key][subkey]:
                                curr_val = current_features[key][subkey][coord]
                                prev_val = previous_features[key][subkey][coord]
                                delta = abs(curr_val - prev_val)
                                if delta > threshold:
                                    changes[key][subkey][coord] = curr_val
                    elif subkey == 'angle':
                        curr_val = current_features[key][subkey]
                        prev_val = previous_features[key][subkey]
                        delta = abs(curr_val - prev_val)
                        if delta > threshold:
                            changes[key][subkey] = curr_val
                            
        return changes if any(changes.values()) else None

    def detect_repetitive_movements(self, movement_history, current_movements, timestamp):
        """Detect repetitive movements that might indicate stimming or other patterns."""
        if not movement_history:
            return [], []
            
        # Define time window for repetition detection (in seconds)
        time_window = 5.0
        
        # Filter movements within the time window
        recent_movements = [m for m in movement_history if timestamp - m['timestamp'] <= time_window]
        
        # If we don't have enough movements yet, return empty lists
        if len(recent_movements) < 3:
            return [], []
            
        # Group similar movements
        movement_groups = {}
        for movement in recent_movements:
            movement_key = movement['movement']
            if movement_key not in movement_groups:
                movement_groups[movement_key] = []
            movement_groups[movement_key].append(movement)
            
        # Check for repetitive movements (same movement occurring multiple times)
        repetitive_movements = []
        for movement_key, occurrences in movement_groups.items():
            if len(occurrences) >= 3:  # At least 3 occurrences to consider it repetitive
                # Calculate frequency (movements per second)
                time_span = occurrences[-1]['timestamp'] - occurrences[0]['timestamp']
                if time_span > 0:
                    frequency = len(occurrences) / time_span
                    repetitive_movements.append({
                        'movement': movement_key,
                        'count': len(occurrences),
                        'frequency': frequency,
                        'start_time': occurrences[0]['timestamp'],
                        'end_time': occurrences[-1]['timestamp']
                    })
                    
        # Check for potential stimming behaviors
        stimming_behaviors = []
        for movement_key, occurrences in movement_groups.items():
            # Define stimming patterns based on movement type and frequency
            if len(occurrences) >= 3:
                time_span = occurrences[-1]['timestamp'] - occurrences[0]['timestamp']
                if time_span > 0:
                    frequency = len(occurrences) / time_span
                    
                    # Check for high-frequency repetitive movements that might indicate stimming
                    # Only classify as stimming if it meets specific criteria
                    if frequency > 1.5 and self.is_likely_stimming(movement_key, frequency):
                        stimming_type = self.classify_stimming_behavior(movement_key, frequency)
                        if stimming_type:
                            stimming_behaviors.append({
                                'type': stimming_type,
                                'movement': movement_key,
                                'frequency': frequency,
                                'start_time': occurrences[0]['timestamp'],
                                'end_time': occurrences[-1]['timestamp']
                            })
                            
        return repetitive_movements, stimming_behaviors
        
    def is_likely_stimming(self, movement, frequency):
        """Determine if a repetitive movement is likely to be stimming rather than a meaningful action."""
        # Define characteristics that suggest a movement is likely stimming
        stimming_indicators = {
            'hand_flapping': ['hand', 'flap', 'wave'],
            'rocking': ['rock', 'sway', 'back and forth'],
            'finger_tapping': ['finger', 'tap', 'fidget'],
            'head_banging': ['head', 'bang', 'shake'],
            'spinning': ['spin', 'rotate', 'turn'],
            'pacing': ['pace', 'walk back and forth'],
            'repetitive_speech': ['speak', 'talk', 'vocal']
        }
        
        # Check if the movement matches any stimming indicators
        for stim_type, indicators in stimming_indicators.items():
            if any(indicator in movement.lower() for indicator in indicators):
                # For these specific movements, consider them stimming if frequency is high
                return True
                
        # For other movements, check if they have characteristics of stimming
        # Stimming is often:
        # 1. Very high frequency (more than 2 movements per second)
        # 2. Unrelated to any apparent purpose or goal
        # 3. Often involves hands, head, or whole body
        # 4. May be accompanied by facial expressions of concentration or self-regulation
        
        # Check if movement involves hands, head, or whole body
        body_parts = ['hand', 'head', 'body', 'arm', 'leg', 'foot']
        involves_body_part = any(part in movement.lower() for part in body_parts)
        
        # Check if movement seems purposeless (not walking, not reaching for something, etc.)
        purposeful_actions = ['walk', 'reach', 'grab', 'hold', 'push', 'pull', 'open', 'close']
        seems_purposeless = not any(action in movement.lower() for action in purposeful_actions)
        
        # If it's a high-frequency movement involving body parts and seems purposeless,
        # it might be stimming
        if frequency > 2.0 and involves_body_part and seems_purposeless:
            return True
            
        return False
        
    def classify_stimming_behavior(self, movement, frequency):
        """Classify a repetitive movement as a specific type of stimming behavior."""
        # Define common stimming patterns
        stimming_patterns = {
            'hand_flapping': ['hand raised', 'hand lowered', 'hand flapping'],
            'rocking': ['body swaying', 'body rocking'],
            'finger_tapping': ['finger movement', 'hand tapping'],
            'head_banging': ['head tilted down', 'head movement', 'head banging'],
            'spinning': ['body rotation', 'turning', 'spinning'],
            'pacing': ['walking', 'moving', 'pacing'],
            'repetitive_speech': ['mouth movement', 'speaking']
        }
        
        # Check if the movement matches any stimming pattern
        for stim_type, patterns in stimming_patterns.items():
            if any(pattern in movement.lower() for pattern in patterns):
                return stim_type
                
        # If no specific pattern is matched but frequency is high and it's likely stimming,
        # classify as general stimming
        if frequency > 2.0 and self.is_likely_stimming(movement, frequency):
            return 'general_stimming'
            
        return None
        
    def detect_meltdown_precursors(self, movement_history, current_movements, timestamp):
        """Detect behaviors that might indicate an approaching meltdown."""
        if not movement_history:
            return []
            
        # Define time window for precursor detection (in seconds)
        time_window = 10.0
        
        # Filter movements within the time window
        recent_movements = [m for m in movement_history if timestamp - m['timestamp'] <= time_window]
        
        # If we don't have enough movements yet, return empty list
        if len(recent_movements) < 5:
            return []
            
        # Define potential meltdown precursors
        precursors = []
        
        # Check for increased movement frequency
        movement_counts = {}
        for movement in recent_movements:
            movement_key = movement['movement']
            if movement_key not in movement_counts:
                movement_counts[movement_key] = 0
            movement_counts[movement_key] += 1
            
        # If any movement occurs frequently, it might indicate agitation
        for movement_key, count in movement_counts.items():
            if count >= 5:  # High frequency of any movement
                precursors.append({
                    'type': 'increased_movement_frequency',
                    'movement': movement_key,
                    'count': count,
                    'time_period': time_window
                })
                
        # Check for specific precursors like hand flapping, rocking, or pacing
        for movement in recent_movements:
            movement_key = movement['movement'].lower()
            
            # Hand flapping is often a sign of anxiety or excitement
            if 'hand' in movement_key and ('flap' in movement_key or 'wave' in movement_key):
                precursors.append({
                    'type': 'hand_flapping',
                    'movement': movement['movement'],
                    'timestamp': movement['timestamp']
                })
                
            # Rocking can indicate anxiety or self-soothing
            if 'rock' in movement_key or 'sway' in movement_key:
                precursors.append({
                    'type': 'rocking',
                    'movement': movement['movement'],
                    'timestamp': movement['timestamp']
                })
                
            # Pacing can indicate anxiety or restlessness
            if 'pace' in movement_key or 'walk' in movement_key:
                precursors.append({
                    'type': 'pacing',
                    'movement': movement['movement'],
                    'timestamp': movement['timestamp']
                })
                
        return precursors

    def interpret_movement(self, changes):
        """Interpret the changes into meaningful movement descriptions."""
        movements = []
        
        # Check for arm movements
        if 'arms' in changes:
            arms = changes['arms']
            for side in ['left_elbow', 'right_elbow']:
                if side in arms:
                    elbow = arms[side]
                    if 'angle' in elbow:
                        angle = elbow['angle']
                        if angle > 45:
                            movements.append(f"{side.split('_')[0]} arm raised")
                        elif angle < -45:
                            movements.append(f"{side.split('_')[0]} arm lowered")
        
        # Check for hand movements
        if 'hands' in changes:
            hands = changes['hands']
            for side in ['left_wrist', 'right_wrist']:
                if side in hands:
                    wrist = hands[side]
                    if 'y' in wrist:
                        if wrist['y'] < 0.3:  # Wrist above shoulder level
                            movements.append(f"{side.split('_')[0]} hand raised")
                        elif wrist['y'] > 0.7:  # Wrist below hip level
                            movements.append(f"{side.split('_')[0]} hand lowered")
                        
                        # Check for hand flapping (rapid up and down movement)
                        if 'previous_y' in wrist:
                            y_change = abs(wrist['y'] - wrist['previous_y'])
                            if y_change > 0.2:  # Significant vertical movement
                                movements.append(f"{side.split('_')[0]} hand flapping")
        
        # Check for head movements
        if 'head' in changes:
            head = changes['head']
            if 'y' in head:
                if head['y'] < 0.3:  # Head tilted up
                    movements.append("head tilted up")
                elif head['y'] > 0.7:  # Head tilted down
                    movements.append("head tilted down")
                    
                # Check for head banging or shaking
                if 'previous_y' in head:
                    y_change = abs(head['y'] - head['previous_y'])
                    if y_change > 0.2:  # Significant vertical movement
                        movements.append("head banging or shaking")
        
        # Check for body movements (rocking, swaying)
        if 'body' in changes:
            body = changes['body']
            if 'rotation' in body:
                rotation = body['rotation']
                if abs(rotation) > 15:  # Significant rotation
                    if rotation > 0:
                        movements.append("body rocking right")
                    else:
                        movements.append("body rocking left")
                        
            if 'sway' in body:
                sway = body['sway']
                if abs(sway) > 0.2:  # Significant swaying
                    if sway > 0:
                        movements.append("body swaying right")
                    else:
                        movements.append("body swaying left")
        
        return movements

    def build_final_prompt(self, description, movement_sequences, facial_expressions, repetitive_movements, stimming_behaviors, meltdown_precursors):
        """Build a structured prompt for GPT analysis based on the FinalPrompt.py format."""
        
        # Helper to wrap unavailable modules
        def module_or_note(value, module_name):
            return value if value != "not provided" else f"**Note:** {module_name} was not provided. Please ignore this data during your analysis."

        # Check if spinning was detected locally
        spinning_detected = getattr(self, 'spinning_detected', False)

        # Format movement sequences
        movement_sequences_text = "No movement sequences detected."
        if movement_sequences:
            movement_sequences_text = "\n".join([
                f"- {seq['start_time']} to {seq['end_time']}: {', '.join(seq['movements'])}"
                for seq in movement_sequences[:10]  # Limit to first 10 sequences
            ])
        
        # Format facial expressions
        facial_expressions_text = "No facial expressions detected."
        if facial_expressions:
            facial_expressions_text = "\n".join([
                f"- {expr['timestamp']}: {expr['expression']} (confidence: {expr['confidence']:.2f})"
                for expr in facial_expressions[:10]  # Limit to first 10 expressions
            ])
        
        # Format repetitive movements
        repetitive_movements_text = "No repetitive movements detected."
        if repetitive_movements:
            repetitive_movements_text = "\n".join([
                f"- {movement['movement']}: {movement['count']} times, {movement['frequency']:.2f} per second, from {movement['start_time']} to {movement['end_time']}"
                for movement in repetitive_movements[:5]  # Limit to first 5 movements
            ])
        
        # Format stimming behaviors
        stimming_behaviors_text = "No stimming behaviors detected."
        if stimming_behaviors:
            # Check if spinning is in the stimming behaviors
            spinning_detected = spinning_detected or any('spinning' in behavior.get('movement', '').lower() for behavior in stimming_behaviors)
            
            stimming_behaviors_text = "\n".join([
                f"- {behavior['type']}: {behavior['movement']}, {behavior['frequency']:.2f} per second, from {behavior['start_time']} to {behavior['end_time']}"
                for behavior in stimming_behaviors[:5]  # Limit to first 5 behaviors
            ])
            
            # Add spinning-specific note if detected
            if spinning_detected:
                stimming_behaviors_text += """
                
**CRITICAL SPINNING ANALYSIS:**
1. Spinning is a significant stimming behavior that can express different emotions:
   - Happy stimming: Expressing joy, excitement, or positive energy
   - Self-regulation: Managing sensory input and emotional state
   - Emotional expression: Both positive and negative emotions
   - Focus and attention management

2. When spinning is detected, consider the context:
   - Facial expressions and body language for emotional context
   - Duration and intensity of spinning
   - Environmental triggers or stimuli
   - Overall mood and behavior patterns

3. Safety Considerations:
   - Monitor for dizziness or disorientation
   - Ensure safe space for spinning
   - Watch for potential falls or collisions
   - Be aware of duration and intensity of spinning"""
        
        # Format meltdown precursors
        meltdown_precursors_text = "No meltdown precursors detected."
        if meltdown_precursors:
            meltdown_precursors_text = "\n".join([
                f"- {precursor['type']}: {precursor.get('movement', 'N/A')} at {precursor.get('timestamp', 'N/A')}"
                for precursor in meltdown_precursors[:5]  # Limit to first 5 precursors
            ])

        # Add spinning detection note to the description if spinning was detected
        if spinning_detected:
            description += """
            
**CRITICAL SPINNING BEHAVIOR DETECTED:**
The person is engaging in spinning behavior, which is a significant form of stimming. This behavior has been CONFIRMED through local detection algorithms. Your analysis MUST:

1. Acknowledge spinning as a primary stimming behavior
2. Consider the emotional context (could be happy or self-regulatory stimming)
3. Analyze facial expressions and body language for emotional context
4. Provide specific recommendations for managing spinning
5. Consider the sensory and emotional needs indicated by spinning
6. Include safety considerations for spinning behavior
7. Suggest appropriate alternative stimming activities
8. Address environmental modifications to support safe spinning
9. Include specific communication strategies for when spinning occurs
10. Do not assume spinning indicates distress - it could be a positive expression"""

        final_prompt = {
            "role": "user",
            "content": f"""
            # VIDEO ANALYSIS INSTRUCTIONS
            
            ## DATA SOURCES
            You are analyzing a video of a person, with special focus on behaviors relevant to autistic children. Use the following data sources for your analysis:
          
            ### Movement Sequences (Timestamps Included):
            {movement_sequences_text}

            ### Facial Expressions (Timestamps Included):
            {facial_expressions_text}

            ### Repetitive Movements:
            {repetitive_movements_text}

            ### Stimming Behaviors:
            {stimming_behaviors_text}

            ### Meltdown Precursors:
            {meltdown_precursors_text}
            
            ### Special Focus:
            {description}
            
            ## ANALYSIS REQUIREMENTS
            
            You must provide a CONSISTENT, STRUCTURED analysis following this exact format:
            
            # 1. BODY LANGUAGE ANALYSIS
            [KEYWORD: Insert the most prevalent body language keyword here]
            
            - **Posture:** [Describe posture with specific details]
            - **Hand/Finger Movements:** [Describe with specific details]
            - **Leg/Foot Movements:** [Describe with specific details]
            - **Repetitive Behaviors:** [List any repetitive behaviors with timestamps]
            - **Overall Body Language Assessment:** [2-3 sentences summarizing body language]
            
            # 2. STIMMING BEHAVIOR ANALYSIS
            [KEYWORD: Insert the most prevalent stimming keyword here - use "None" if no stimming detected]
            
            - **Stimming Behaviors Detected:** [List specific stimming behaviors with timestamps]
            - **Frequency:** [Describe how often these behaviors occur]
            - **Context:** [Describe when/where these behaviors occur]
            - **Overall Stimming Assessment:** [2-3 sentences summarizing stimming patterns]
            - **Special Note on Spinning:** [If spinning was detected, provide specific analysis of this behavior and its significance as a stimming behavior. Consider both positive and self-regulatory aspects]
            
            # 3. MELTDOWN RISK ASSESSMENT
            [KEYWORD: Insert the most prevalent meltdown risk keyword here - use "None" if no risk detected]
            
            - **Pre-Meltdown Indicators:** [List any behaviors that might indicate an approaching meltdown]
            - **Environmental Triggers:** [Identify any environmental factors that could contribute to a meltdown]
            - **Emotional Escalation:** [Describe any signs of emotional escalation with timestamps]
            - **Overall Meltdown Risk Assessment:** [2-3 sentences summarizing meltdown risk level]
            
            # 4. EMOTIONAL STATE ANALYSIS
            [KEYWORD: Insert the most prevalent emotional keyword here]
            
            - **Primary Emotion:** [State the primary emotion detected]
            - **Emotional Consistency:** [Describe if emotions are consistent or changing]
            - **Emotional Triggers:** [Identify any potential emotional triggers]
            - **Overall Emotional Assessment:** [2-3 sentences summarizing emotional state]
            - **Spinning Context:** [If spinning was detected, analyze the emotional context of the spinning behavior]
            
            # 5. INTERACTION RECOMMENDATIONS
            - **Immediate Actions:** [3-5 specific, actionable recommendations]
            - **Environmental Adjustments:** [3-5 specific environmental recommendations]
            - **Communication Strategies:** [3-5 specific communication recommendations]
            - **Meltdown Prevention Strategies:** [3-5 specific strategies to prevent potential meltdowns]
            - **Spinning Management:** [If spinning was detected, provide 3-5 specific recommendations for managing spinning behavior, considering both positive and self-regulatory aspects]
            
            # 6. INTERACTION SENTENCES
            - **Opening Statements:** [3-5 specific opening statements to use]
            - **Follow-up Questions:** [3-5 specific follow-up questions to use]
            - **Closing Statements:** [3-5 specific closing statements to use]
            - **De-escalation Phrases:** [3-5 specific phrases to use if signs of distress appear]
            - **Spinning-Specific Phrases:** [If spinning was detected, provide 3-5 specific phrases to use when spinning occurs, considering both positive and self-regulatory contexts]
            
            # 7. FINAL SUMMARY
            - **Overall Mood:** [One sentence summarizing overall mood]
            - **Key Observations:** [3-5 bullet points of key observations]
            - **Primary Concerns:** [List any primary concerns, or "None" if none detected. If spinning behavior is detected, it MUST be listed as the first primary concern, as it is a definitive indicator of stimming behavior]
            - **Primary Strengths:** [List any primary strengths observed]
            - **Meltdown Risk Level:** [Rate as "Low", "Medium", "High", or "None detected"]
            
            ## IMPORTANT INSTRUCTIONS:
            1. Be OBJECTIVE and FACTUAL in your analysis
            2. Support ALL observations with specific details from the data
            3. Use TIMESTAMPS when referencing specific behaviors
            4. DO NOT make assumptions beyond what the data supports
            5. If data is missing for any section, explicitly state "Data not available"
            6. Maintain CONSISTENT formatting throughout your response
            7. DO NOT include any text outside the structured sections above
            8. For meltdown analysis, only identify risk factors if they are clearly present in the data
            9. If spinning behavior is detected, ensure to analyze it as a significant stimming behavior and provide specific recommendations for managing this behavior
            10. If spinning is detected, it MUST be listed as the first primary concern in the Final Summary section, as it is a definitive indicator of stimming behavior
            11. If spinning is detected through local algorithms, treat this as a CONFIRMED fact and base your analysis on the certainty that the person is engaging in spinning behavior as a form of stimming
            12. When providing recommendations for spinning behavior, consider:
                - Safety measures
                - Alternative stimming activities
                - Environmental modifications
                - Communication strategies
                - Sensory support needs
                - Emotional regulation techniques
            13. Do not assume spinning indicates distress - it could be a positive expression of joy or excitement
            14. Consider the emotional context of spinning through facial expressions and body language
            """
        }

        return final_prompt

    def detect_spinning(self, landmarks, image_width, image_height):
        """Detect spinning behavior by analyzing right-left position differences."""
        if not landmarks:
            return False
            
        # Get nose position as reference point
        nose_x = landmarks[self.mp_pose.PoseLandmark.NOSE].x * image_width
        nose_y = landmarks[self.mp_pose.PoseLandmark.NOSE].y * image_height
        
        # Get shoulder positions
        left_shoulder_x = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width
        left_shoulder_y = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height
        right_shoulder_x = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width
        right_shoulder_y = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height
        
        # Calculate the difference between right and left shoulder positions relative to nose
        left_diff = (left_shoulder_x - nose_x)
        right_diff = (right_shoulder_x - nose_x)
        
        # Calculate the overall difference
        position_diff = right_diff - left_diff
        
        return position_diff

    def process_video(self, video_path):
        """Process video and collect significant pose changes with optimized performance."""
        logger.info(f"Attempting to open video: {video_path}")
        
        # Reset spinning detection for new video
        self.spinning_detected = False
        spin_direction_changes = 0
        
        if not os.path.exists(video_path):
            logger.error(f"Error: Video file '{video_path}' not found!")
            return None
            
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Error: Could not open video file {video_path}")
            return None
            
        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / self.fps
        
        logger.info(f"Processing video: {frame_width}x{frame_height} @ {self.fps}fps, total frames: {total_frames}, duration: {video_duration:.2f}s")
        
        # Create a window for displaying video
        cv2.namedWindow('Body Language Analysis', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Body Language Analysis', frame_width, frame_height)
        
        previous_features = None
        significant_changes = []
        current_movement_sequence = []
        last_movement_time = 0
        
        # Track movement history for repetitive movement detection
        movement_history = []
        repetitive_movements = []
        stimming_behaviors = []
        meltdown_precursors = []
        
        # Track facial expressions
        facial_expressions = []
        current_expression = None
        last_expression_time = 0
        
        # Track spinning behavior
        position_diffs = []
        last_position_diff = None
        
        # Add a maximum size for position_diffs array
        MAX_POSITION_DIFFS = 50
        
        # Optimized frame sampling based on video length
        if video_duration < 60:  # Videos less than 1 minute
            frame_step = 10  # Sample every 10th frame
        else:
            frame_step = 20  # Sample every 20th frame
        
        logger.info(f"Using optimized frame sampling: every {frame_step} frames ({frame_step/self.fps:.2f} seconds)")
        
        # Create progress bar
        pbar = tqdm(total=total_frames, desc="Processing video", unit="frames")
        
        # Pre-allocate arrays for better memory management
        frame_buffer = []
        max_buffer_size = 30  # Keep a small buffer of frames for processing
        
        # Track last significant change to adjust sampling rate dynamically
        last_significant_change_frame = 0
        consecutive_no_change_frames = 0
        
        # Motion detection variables
        prev_gray = None
        motion_threshold = 1000  # Threshold for detecting significant motion
        
        # Process frames with adaptive sampling
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                logger.info("End of video reached")
                break
                
            self.frame_count += 1
            pbar.update(1)
            
            # Process every nth frame to reduce computation
            if self.frame_count % frame_step != 0:
                continue
                
            # Convert to grayscale for motion detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # Detect motion between frames
            motion_detected = False
            if prev_gray is not None:
                frame_delta = cv2.absdiff(prev_gray, gray)
                thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    if cv2.contourArea(contour) > motion_threshold:
                        motion_detected = True
                        break
            
            prev_gray = gray
            
            if not motion_detected and self.frame_count > frame_step * 5:
                if consecutive_no_change_frames > 3:
                    consecutive_no_change_frames += 1
                    continue
            
            if motion_detected:
                consecutive_no_change_frames = 0
            
            # Extract pose features and facial expressions
            result = self.extract_pose_features(frame)
            if result is None:
                continue
                
            features, pose_results, facial_expression = result
            
            # Check for spinning behavior
            if pose_results and pose_results.pose_landmarks:
                current_position_diff = self.detect_spinning(pose_results.pose_landmarks.landmark, frame_width, frame_height)
                
                # Only add to position_diffs if we haven't reached the maximum size
                if len(position_diffs) < MAX_POSITION_DIFFS:
                    position_diffs.append(current_position_diff)
                else:
                    # Remove oldest entry and add new one
                    position_diffs.pop(0)
                    position_diffs.append(current_position_diff)
                
                # Check for direction changes
                if last_position_diff is not None:
                    if (last_position_diff > 0 and current_position_diff < 0) or \
                       (last_position_diff < 0 and current_position_diff > 0):
                        spin_direction_changes += 1
                        
                        # If we've detected more than 3 direction changes, mark as spinning
                        if spin_direction_changes > 9 and not self.spinning_detected:
                            self.spinning_detected = True
                            logger.info("SPINNING DETECTED: Subject is showing spinning behavior!")
                            # Add spinning to movement history
                            movement_history.append({
                                'movement': 'spinning',
                                'timestamp': self.frame_count / self.fps
                            })
                
                last_position_diff = current_position_diff
            
            # Track facial expressions
            if facial_expression:
                timestamp = self.frame_count / self.fps
                
                # Only record significant expression changes or every 1 second
                if (current_expression is None or 
                    current_expression['expression'] != facial_expression['expression'] or
                    timestamp - last_expression_time > 1.0):
                    
                    current_expression = facial_expression
                    last_expression_time = timestamp
                    
                    facial_expressions.append({
                        'timestamp': timestamp,
                        'expression': facial_expression['expression'],
                        'confidence': facial_expression['confidence']
                    })
                    
                    # Log facial expression detection for debugging
                    logger.debug(f"Detected facial expression: {facial_expression['expression']} with confidence {facial_expression['confidence']:.2f}")
            
            # Calculate significant changes - only if features is not None
            if features is not None:
                changes = self.calculate_pose_changes(features, previous_features)
                
                # Dynamic sampling rate adjustment based on content
                if changes:
                    # Reset counters when significant changes are detected
                    last_significant_change_frame = self.frame_count
                    consecutive_no_change_frames = 0
                    
                    # Temporarily increase sampling rate around significant changes
                    # This helps capture the details of important movements
                    if self.frame_count - last_significant_change_frame < frame_step * 2:
                        # Reduce frame_step by 1 (increase sampling rate) but don't go below 2
                        if video_duration < 5:
                            frame_step = max(2, frame_step - 1)
                        elif video_duration < 10:
                            frame_step = max(5, frame_step - 1)
                        elif video_duration < 15:
                            frame_step = max(7, frame_step - 1)
                        elif video_duration < 20:
                            frame_step = max(10, frame_step - 1)
                        elif video_duration < 30:
                            frame_step = max(12, frame_step - 1)
                        elif video_duration < 40:
                            frame_step = max(15, frame_step - 1)
                        else:
                            frame_step = max(25, frame_step - 1)
                else:
                    consecutive_no_change_frames += 1
                    
                    # If no significant changes for a while, gradually reduce sampling rate
                    if consecutive_no_change_frames > 5:
                        # Gradually increase frame_step (reduce sampling rate)
                        # But don't exceed the original frame_step based on video length
                        original_frame_step = 10 if video_duration < 60 else 20
                        frame_step = min(frame_step + 1, original_frame_step)
                        consecutive_no_change_frames = 0  # Reset counter
                
                if changes:
                    timestamp = self.frame_count / self.fps
                    time_str = str(timedelta(seconds=int(timestamp)))
                    
                    # Interpret the changes into meaningful movements
                    movements = self.interpret_movement(changes)
                    
                    if movements:
                        # Add to movement history for repetitive movement detection
                        for movement in movements:
                            movement_history.append({
                                'movement': movement,
                                'timestamp': timestamp
                            })
                        
                        # Detect repetitive movements and stimming behaviors
                        new_repetitive, new_stimming = self.detect_repetitive_movements(
                            movement_history, movements, timestamp
                        )
                        
                        # Add new repetitive movements and stimming behaviors
                        repetitive_movements.extend(new_repetitive)
                        stimming_behaviors.extend(new_stimming)
                        
                        # Detect meltdown precursors
                        new_precursors = self.detect_meltdown_precursors(
                            movement_history, movements, timestamp
                        )
                        meltdown_precursors.extend(new_precursors)
                        
                        # If it's a new movement sequence (more than 1 second since last movement)
                        if timestamp - last_movement_time > 1.0:
                            if current_movement_sequence:
                                significant_changes.append({
                                    'start_time': str(timedelta(seconds=int(last_movement_time))),
                                    'end_time': time_str,
                                    'movements': current_movement_sequence
                                })
                            current_movement_sequence = []
                            last_movement_time = timestamp
                        
                        current_movement_sequence.extend(movements)
            
            # Only update previous_features if features is not None
            if features is not None:
                previous_features = features
            
            # Draw pose landmarks on frame
            if pose_results and pose_results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    pose_results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                )
                
                # Draw face mesh landmarks for debugging
                if facial_expression and 'face_landmarks' in facial_expression and facial_expression['face_landmarks']:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        facial_expression['face_landmarks'],
                        self.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
                    )
            
            # Draw facial expression on frame
            if current_expression:
                expression_text = f"Expression: {current_expression['expression']} ({current_expression['confidence']:.2f})"
                cv2.putText(frame, expression_text, (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display frame number and current sampling rate
            cv2.putText(frame, f"Frame: {self.frame_count} (Step: {frame_step})", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display the frame
            cv2.imshow('Body Language Analysis', frame)
            
            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info("User interrupted the analysis")
                break
                
            # Force garbage collection periodically
            if self.frame_count % 100 == 0:
                gc.collect()
                
        # Add the last movement sequence if exists
        if current_movement_sequence:
            significant_changes.append({
                'start_time': str(timedelta(seconds=int(last_movement_time))),
                'end_time': time_str,
                'movements': current_movement_sequence
            })
                
        cap.release()
        cv2.destroyAllWindows()
        pbar.close()
        
        # After video processing, analyze the collected data
        logger.info("Video processing complete. Analyzing collected data...")
        self.time_series_data = significant_changes  # Use significant changes instead of all frames
        
        # Add repetitive movements, stimming behaviors, and meltdown precursors to the analysis
        self.repetitive_movements = repetitive_movements
        self.stimming_behaviors = stimming_behaviors
        self.meltdown_precursors = meltdown_precursors
        
        # Add facial expressions to the analysis
        self.facial_expressions = facial_expressions
        
        return 
    
    def analyze_video(self, video_path, description=""):
        # Get the analysis
        analysis = self.analyze_time_series_data(description)
        
        # Extract final summary from the analysis
        final_summary = ""
        
        # Use the instance variable for spinning detection
        spinning_detected = getattr(self, 'spinning_detected', False)
        
        # Parse the analysis to extract final summary
        if analysis:
            # Split the analysis into sections
            sections = analysis.split('#')
            for section in sections:
                if '7. FINAL SUMMARY' in section:
                    # Extract the entire final summary section
                    final_summary = section.strip()
                    
                    # If spinning was detected, modify the final summary
                    if spinning_detected:
                        # Split the summary into lines
                        summary_lines = final_summary.split('\n')
                        modified_lines = []
                        
                        for line in summary_lines:
                            if '**Primary Concerns:**' in line:
                                # Replace "None" with spinning as primary concern
                                if 'None' in line:
                                    modified_lines.append('**Primary Concerns:** Spinning behavior (definitive indicator of stimming)')
                                else:
                                    # If there are other concerns, add spinning as the first one
                                    modified_lines.append('**Primary Concerns:** Spinning behavior (definitive indicator of stimming), ' + line.split(':', 1)[1].strip())
                            else:
                                modified_lines.append(line)
                        
                        # Update the final summary with the modified lines
                        final_summary = '\n'.join(modified_lines)
        
        # Save analysis to file
        with open('body_language_analysis.txt', 'w') as f:
            f.write(analysis)
        logger.info("Analysis saved to 'body_language_analysis.txt'")
        
        # Display analysis in console
        logger.info("Final Analysis:")
        logger.info("=" * 80)
        logger.info(analysis)
        logger.info("=" * 80)
        logger.info(f"Final Summary: {final_summary}")
        print("description : ", description)
        
        # Return the analysis result with final summary as a single field
        return {
            'filename': Path(video_path).stem,
            'facial_emotion': self.facial_expressions,
            'combined_description': self.time_series_data,
            'transcribed_text': "",  # Will be filled by transcribe_audio_with_timestamps
            'audio_emotions': "",    # Will be filled by use_audio_text_emotion
            'text_emotions': "",     # Will be filled by use_audio_text_emotion
            'loudness': "",          # Will be filled by analyze_audio
            'visual_patterns': {},   # Will be filled by detect_visual_patterns
            'final_analysis': {
                'frame_analysis': analysis,
                'final_summary': final_summary,  # Final summary as a single field
                'spinning_detected': spinning_detected  # Use the instance variable
            },
            'timings': {},
            'video_context': description
        }

    def analyze_time_series_data(self, description=""):
        """Analyze the collected time series data using GPT."""
        if not self.time_series_data:
            return "No pose data collected."
            
        # Create a summary of the movements
        summary = {
            'total_sequences': len(self.time_series_data),
            'movement_sequences': [
                {
                    'time_period': f"{seq['start_time']} - {seq['end_time']}",
                    'movements': seq['movements']
                }
                for seq in self.time_series_data
            ]
        }
        
        # Add repetitive movements, stimming behaviors, and meltdown precursors
        if hasattr(self, 'repetitive_movements') and self.repetitive_movements:
            summary['repetitive_movements'] = [
                {
                    'movement': movement['movement'],
                    'count': movement['count'],
                    'frequency': movement['frequency'],
                    'time_period': f"{str(timedelta(seconds=int(movement['start_time'])))} - {str(timedelta(seconds=int(movement['end_time'])))}"
                }
                for movement in self.repetitive_movements
            ]
            
        if hasattr(self, 'stimming_behaviors') and self.stimming_behaviors:
            summary['stimming_behaviors'] = [
                {
                    'type': behavior['type'],
                    'movement': behavior['movement'],
                    'frequency': behavior['frequency'],
                    'time_period': f"{str(timedelta(seconds=int(behavior['start_time'])))} - {str(timedelta(seconds=int(behavior['end_time'])))}"
                }
                for behavior in self.stimming_behaviors
            ]
            
        if hasattr(self, 'meltdown_precursors') and self.meltdown_precursors:
            summary['meltdown_precursors'] = [
                {
                    'type': precursor['type'],
                    'movement': precursor.get('movement', 'N/A'),
                    'timestamp': str(timedelta(seconds=int(precursor.get('timestamp', 0))))
                }
                for precursor in self.meltdown_precursors
            ]
            
        # Add facial expressions
        if hasattr(self, 'facial_expressions') and self.facial_expressions:
            summary['facial_expressions'] = [
                {
                    'expression': expr['expression'],
                    'confidence': expr['confidence'],
                    'timestamp': str(timedelta(seconds=int(expr['timestamp'])))
                }
                for expr in self.facial_expressions
            ]
            
        # Build the final prompt using the structured format
        if not description:
            description = "This video shows a person whose body language and facial expressions should be analyzed with special attention to behaviors relevant to autistic children, including stimming, meltdown precursors, and emotional states."
        
        final_prompt = self.build_final_prompt(
            description=description,
            movement_sequences=self.time_series_data,
            facial_expressions=self.facial_expressions,
            repetitive_movements=self.repetitive_movements,
            stimming_behaviors=self.stimming_behaviors,
            meltdown_precursors=self.meltdown_precursors
        )
        
        try:
            logger.info("\nSending data to GPT for structured analysis...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in body language and facial expression analysis, with special expertise in recognizing behaviors in autistic children. Analyze the given data and provide a structured analysis following the exact format specified in the prompt."},
                    final_prompt
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            if not response or not response.choices:
                return "Error: No response from GPT"
                
            analysis = response.choices[0].message.content
            logger.info("\nGPT Analysis completed successfully")
            return analysis
        except Exception as e:
            error_msg = f"Error in GPT analysis: {str(e)}"
            logger.error(error_msg)
            return error_msg
