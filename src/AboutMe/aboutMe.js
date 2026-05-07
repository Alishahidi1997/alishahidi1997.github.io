import React from "react";
import ResumePath from "../Assets/AliShahidiResume.pdf";

function AboutMe() {
    return (
        <div className="col-8 align-self-center">
            <h2 style={{ fontWeight: 'bold', marginBottom: '1.5rem' }}>
                About Me
            </h2>

            <div
                className="lead text-muted"
                style={{ fontSize: '1.05rem', lineHeight: '1.7' }}
            >

                <p>
                    I&apos;m a software developer based in Calgary specializing in{" "}
                    <strong>backend engineering</strong> and{" "}
                    <strong>applied AI</strong>. I build scalable API-first
                    services, RAG pipelines, and real-time systems with an
                    emphasis on production-grade reliability.
                </p>

                <p>
                    At <strong>ETHEREAL Research Group</strong> and{" "}
                    <strong>ELIXR</strong>, I engineered backend architectures
                    for multimodal AI and real-time interactive systems,
                    optimizing data pipelines to reduce API costs and improve
                    system performance. My recent work includes developing AI
                    middleware with <strong>RBAC</strong>, audit logging, and{" "}
                    <strong>LLM tool-calling</strong> for secure Slack-based
                    automation.
                </p>

                <p>
                    Previously, I contributed to distributed multiplayer systems
                    at <strong>TELUS</strong>, focusing on low-latency
                    synchronization across mobile and immersive platforms.
                </p>

                <p>
                    I hold a <strong>Master of Software Engineering</strong>{" "}
                    from the University of Calgary and a{" "}
                    <strong>B.Sc. in Computer Engineering</strong> from the
                    University of Tehran.
                </p>

                <p className="mb-2">
                    <strong>Tech Stack:</strong> Python (FastAPI), C# (.NET
                    Core), SQL, Docker, LLM orchestration, REST APIs, and Unity.
                </p>

                <p
                    className="mt-3 mb-2"
                    style={{ fontSize: '1rem' }}
                >
                    Self-directed projects are available in the{" "}
                    <a href="#Portfolio" className="link-secondary">
                        portfolio
                    </a>
                    ; my resume covers research and professional experience in
                    greater detail.
                </p>

                <p
                    className="mt-4"
                    style={{ fontStyle: 'italic' }}
                >
                    Open to <strong>backend software engineering</strong>,{" "}
                    <strong>applied AI</strong>, and{" "}
                    <strong>AI platform engineering</strong> opportunities.
                </p>

            </div>

            <a
                href={ResumePath}
                role="button"
                className="btn btn-secondary"
                target="_blank"
                rel="noopener noreferrer"
            >
                Download Resume
            </a>
        </div>
    );
}

export default AboutMe;