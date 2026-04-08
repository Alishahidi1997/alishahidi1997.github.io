import React from "react";
// import profilePic from "../Assets/"; 
import ResumePath from "../Assets/AliShahidiResume.pdf";

function showPdf(){
    // You can implement this if needed later
}
function AboutMe() {
    const summaryAboutMe = `I am a multidisciplinary software developer with a Master's in Software Engineering from the University of Calgary and over 5 years of experience in Unity, C#, ASP.NET, XR, and AR/VR technologies. I have led projects including immersive VR simulations, interactive AR educational apps, and multiplayer systems, integrating AI-driven avatars and real-time data processing. 
    While I enjoy building applications across AR/VR and interactive experiences, I am especially passionate about gaming development, creating narrative-driven games, engaging mechanics, and high-performance gameplay. 
    I am proficient in ASP.NET, Unity 3D, C#, Python, C/C++, and full-stack web development (HTML, CSS, JavaScript, React.js, Node.js, Express.js, PostgreSQL). I hold multiple Unity and web development certifications and am eager to bring my skills and creativity to innovative gaming projects.`;

    return (
        <div className="col-8 align-self-center">
           <h2 style={{ fontWeight: 'bold', marginBottom: '1.5rem' }}>About Me</h2>
    <div className="lead text-muted" style={{ fontSize: '1.1rem', lineHeight: '1.7' }}>
        <p>
            I am a <strong>Systems-Focused Software Developer</strong> specializing in 
            <strong> ASP.NET Core, Python AI integration, and Spatial Computing</strong>. 
            With a Master’s in Software Engineering and a 4.0 GPA, I focus on building high-performance 
            applications that solve complex infrastructure and interaction challenges.
        </p>
        
        <p>
            My work is defined by <strong>measurable technical impact</strong>. At <strong>ETHEREAL Research Group</strong>, 
            I architected backend systems that achieved a <strong>98% reduction in third-party API costs</strong> 
            and a <strong>90% boost in video processing speed</strong>. From engineering <strong>Retrieval-Augmented Generation (RAG) </strong> 
            pipelines with Llama 3 to scaling <strong>multiplayer AR environments at Telus</strong>, 
            I bridge the gap between backend stability and immersive frontend experiences.
        </p>

        <p style={{ fontWeight: 'bold', color: '#4ba1da', marginTop: '1.5rem' }}>Core Competencies:</p>
        <ul style={{ listStyleType: 'none', paddingLeft: '0' }}>
            <li>🛠️ <strong>Backend & Cloud:</strong> ASP.NET Core, JWT Architectures, Dapper, Entity Framework, Azure.</li>
            <li>🤖 <strong>AI & Automation:</strong> RAG Pipelines (Llama 3/Ollama), Multimodal Inference, GPT-driven Systems.</li>
            <li>🎮 <strong>XR & Real-Time:</strong> Unity (C#), NetCode Multiplayer, Meta Quest SDK, Spatial Anchors.</li>
            <li>⚡ <strong>Performance:</strong> System Profiling, GPU Instancing, Batching, and API Optimization.</li>
        </ul>

        <p style={{ fontWeight: 'bold', color: '#4ba1da', marginTop: '1.5rem' }}>Professional Credentials:</p>
        <ul className="list-unstyled">
            <li>🎓 <strong>Master of Software Engineering</strong> — University of Calgary (GPA: 4.0/4.0)</li>
            <li>📜 <strong>Advanced .NET & SQL Systems</strong> — Specialized Certification (2026)</li>
            <li>📜 <strong>Software Design Patterns & Architecture</strong> — Unity/Systems (2024)</li>
        </ul>

        <p className="mt-4" style={{ fontStyle: 'italic' }}>
            I am driven by the challenge of delivering clean, testable code and scalable architectures 
            for complex, data-intensive applications across web, desktop, and XR platforms.
        </p>
</div>
            <a href={ResumePath} role="button" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                Download Resume
            </a>
        </div>
    );
}


export default AboutMe;
