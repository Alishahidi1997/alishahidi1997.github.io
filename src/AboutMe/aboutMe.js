import React from "react";
import ResumePath from "../Assets/AliShahidiResume.pdf";

function AboutMe() {
    return (
        <div className="col-8 align-self-center">
           <h2 style={{ fontWeight: 'bold', marginBottom: '1.5rem' }}>About Me</h2>
    <div className="lead text-muted" style={{ fontSize: '1.05rem', lineHeight: '1.7' }}>
        <p>
            I am a <strong>junior-to-mid Software Developer</strong> based in Calgary with a
            <strong> Master of Software Engineering (4.0 GPA)</strong> from the University of Calgary.
            My core focus is building practical software with <strong>ASP.NET Core, C#, Python, Unity, and SQL</strong>.
        </p>
        
        <p>
            Most recently at <strong>ETHEREAL Research Group</strong>, I built backend-integrated VR systems for
            accessible training, where my optimization work contributed to a <strong>98% reduction in third-party API costs</strong>,
            <strong> 90% faster video processing</strong>, and <strong>83% higher analysis accuracy</strong>.
            I also worked across <strong>ELIXR & Illumia</strong> and <strong>Telus</strong>, delivering Unity/WebXR features,
            RAG pipelines with Llama 3 + Ollama, and multiplayer AR systems supporting up to 50 users.
        </p>

        <p style={{ fontWeight: 'bold', color: '#b6babd', marginTop: '1.5rem' }}>Recent Project Work:</p>
        <ul style={{ listStyleType: 'none', paddingLeft: '0' }}>
            <li>🔐 <strong>Social Networking API:</strong> Built REST APIs in ASP.NET Core with JWT auth, role-based access, Dapper, and Entity Framework.</li>
            <li>☕ <strong>Coffee Shop Simulation (ETHEREAL):</strong> Connected Unity + .NET backend with GPT dialogue and ElevenLabs voice for adaptive NPC interaction.</li>
            <li>🧠 <strong>Multi-Modal Behaviour Analysis:</strong> Implemented Python pipelines for real-time vision/audio/text processing.</li>
            <li>🎙️ <strong>ATC Simulation (ELIXR & Illumia):</strong> Developed RAG + speech-to-action workflows to reduce trainee manual workload.</li>
        </ul>

        <p style={{ fontWeight: 'bold', color: '#b6babd', marginTop: '1.5rem' }}>Technical Stack:</p>
        <ul className="list-unstyled">
            <li><strong>Languages:</strong> C#, Python, JavaScript, SQL, C/C++</li>
            <li><strong>Backend:</strong> ASP.NET Core, MVC, REST APIs, JWT, Dapper, Entity Framework</li>
            <li><strong>XR/Realtime:</strong> Unity, NetCode Multiplayer, Meta Quest SDK, Spatial Anchors, WebXR</li>
            <li><strong>AI/Infra:</strong> RAG pipelines, Llama 3, Ollama, OpenAI APIs, Docker, Git, Agent</li>
        </ul>

        <p className="mt-4" style={{ fontStyle: 'italic' }}>
            I am currently targeting <strong>junior to mid-level software roles</strong> where I can keep growing
            in backend engineering while contributing to production-ready XR and AI-enabled systems.
        </p>
</div>
            <a href={ResumePath} role="button" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                Download Resume
            </a>
        </div>
    );
}


export default AboutMe;
