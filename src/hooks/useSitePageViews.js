import { useEffect, useState } from 'react';
import {
  doc,
  onSnapshot,
  runTransaction,
} from 'firebase/firestore';
import { getFirestoreDb, isFirebaseConfigured } from '../firebaseClient';

const STATS_PATH = ['site', 'stats'];

let incrementScheduledForSession = false;

/**
 * Increments a Firestore counter once per browser session (avoids double-count
 * from React Strict Mode in development). Shows live total in the UI.
 *
 * Firestore rules (paste in Firebase Console → Firestore → Rules):
 *
 * rules_version = '2';
 * service cloud.firestore {
 *   match /databases/{database}/documents {
 *     match /site/stats {
 *       allow read: if true;
 *       allow create: if request.resource.data.keys().hasOnly(['pageViews'])
 *         && request.resource.data.pageViews == 1;
 *       allow update: if request.resource.data.keys().hasOnly(['pageViews'])
 *         && request.resource.data.pageViews == resource.data.pageViews + 1;
 *     }
 *   }
 * }
 */
export function useSitePageViews() {
  const configured = isFirebaseConfigured();
  const [count, setCount] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!configured) return undefined;

    const db = getFirestoreDb();
    if (!db) return undefined;

    const ref = doc(db, ...STATS_PATH);

    const unsubscribe = onSnapshot(
      ref,
      (snap) => {
        if (snap.exists()) {
          setCount(snap.data().pageViews ?? 0);
        }
      },
      (e) => {
        setError(e);
      }
    );

    if (!incrementScheduledForSession) {
      incrementScheduledForSession = true;
      runTransaction(db, async (transaction) => {
        const snap = await transaction.get(ref);
        if (!snap.exists()) {
          transaction.set(ref, { pageViews: 1 });
        } else {
          const prev = snap.data().pageViews ?? 0;
          transaction.update(ref, { pageViews: prev + 1 });
        }
      }).catch((e) => {
        setError(e);
      });
    }

    return () => unsubscribe();
  }, [configured]);

  return {
    configured,
    count,
    loading: configured && count === null && !error,
    error,
  };
}
