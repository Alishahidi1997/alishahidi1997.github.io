import React from "react";
import ResumePath from "../Assets/AliShahidiResume.pdf";

function AboutMe() {
    return (
        <div className="col-8 align-self-center">
            <h2 style={{ fontWeight: 'bold', marginBottom: '1.5rem' }}>About Me</h2>
            <div className="lead text-muted" style={{ fontSize: '1.05rem', lineHeight: '1.7' }}>
                <p>
                    I&apos;m a software developer based in Calgary focused on <strong>backend engineering</strong>,{' '}
                    <strong>XR systems</strong>, and <strong>applied AI</strong>. I build production-ready APIs,
                    multiplayer AR/VR systems, and LLM-powered applications, focusing on performance, system reliability,
                    and practical deployment.
                </p>

                <p>
                    My work sits at the intersection of <strong>real-time systems</strong>, <strong>AI-driven interaction</strong>,
                    and <strong>scalable backend services</strong>.
                </p>

                <p>
                    Credentials include a <strong>Master of Software Engineering</strong> from the University of Calgary and a{' '}
                    <strong>B.Sc. in Computer Engineering</strong> from the University of Tehran.
                </p>

                <p>
                    At <strong>ETHEREAL Research Group</strong>, work centered on accessible VR training and backend services
                    powering real-time multimodal AI interactions. Performance improved and API costs dropped through optimized
                    pipelines and structured integrations.
                </p>

                <p>
                    At <strong>ELIXR &amp; Illumia</strong>, shipped XR applications and LLM-powered systems agent-based simulators
                    and retrieval pipelines; with emphasis on runtime performance and scalable backend integration.
                </p>

                <p>
                    At <strong>Telus</strong>, led development of a multiplayer AR application supporting{' '}
                    <strong>real-time synchronization for up to 50 concurrent users</strong>.
                </p>

                <p>
                    At the <strong>University of Calgary</strong>, served as a graduate research and teaching assistant-supporting
                    software engineering courses and building research prototypes for assistive technology.
                </p>

                <p className="mb-2">
                    <strong>Tech:</strong> Python, C#, FastAPI, ASP.NET Core, Unity, RAG systems, REST APIs, SQL
                </p>

                <p className="mt-3 mb-2" style={{ fontSize: '1rem' }}>
                    Self-directed builds are in the{' '}
                    <a href="#Portfolio" className="link-secondary">portfolio</a>; my resume lists research and professional work in depth.
                </p>

                <p className="mt-4" style={{ fontStyle: 'italic' }}>
                    Open to <strong>software engineering/developer roles</strong> where I can contribute to production systems and continue
                    growing as a backend and AI engineer.
                </p>
            </div>
            <a href={ResumePath} role="button" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                Download Resume
            </a>
        </div>
    );
}

export default AboutMe;
