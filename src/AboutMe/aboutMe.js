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
            <h2 style={{ fontWeight: 'bold' }}>About Me</h2>
            <div className="lead text-muted">
    <p>
        I’m a multidisciplinary software developer passionate about creating immersive games, interactive experiences, and scalable backend systems using <strong>Python</strong>, <strong>ASP.NET</strong>, <strong>Unity</strong>, <strong>C++</strong>, and <strong>C#</strong>. Over the past five years, I’ve built narrative-driven games, VR simulations, real-time multiplayer systems, and robust backend applications, with a focus on <strong>performance, scalability, and user engagement</strong>.
    </p>
    <p>
        My expertise spans <strong>AI-driven gameplay systems</strong>, <strong>GPT/LLM-powered applications</strong>, <strong>real-time data pipelines</strong>, <strong>REST APIs</strong>, and <strong>cross-platform optimization</strong>. I’ve extended engine functionality through <strong>custom plugins</strong>, <strong>Control Rig</strong>, <strong>PCG</strong>, and <strong>Editor Utility Widgets</strong>, while designing reusable frameworks to streamline development across PC, mobile, VR, and web platforms.
    </p>
    <p>
        I’ve contributed to high-impact projects at <strong>ETHEREAL Research Group</strong>, <strong>Telus</strong>, <strong>ELIXR</strong>, and <strong>Illumia</strong>, leading assistive XR research, developing commercial AR/VR solutions, and delivering polished applications with measurable performance improvements.
    </p>
    <p>I hold certifications in:</p>
    <ul>
        <li><strong>C# .NET with MS SQL Complete Beginner to Master 2026</strong> (2026)</li>
        <li><strong>Programming Design Patterns for Unity</strong> (2024)</li>
        <li><strong>Animation in Unity</strong> (2024)</li>
        <li><strong>The Complete Web Development Bootcamp</strong> (2023)</li>
        <li><strong>Unity Mobile Game Development</strong> (2023)</li>
        <li><strong>Unity 3D Game Development</strong> (2023)</li>
    </ul>
    <p>
        I’m driven by the challenge of blending creativity and engineering to build <strong>high-performance, real-time systems</strong>. Experienced in <strong>Python and .NET backend development</strong>, designing and implementing <strong>REST APIs</strong>, and integrating <strong>large language models (LLMs)</strong> for intelligent, data-driven applications. Whether creating <strong>scalable AR/VR experiences in Unity</strong>, developing <strong>gameplay systems in Unreal</strong>, or building <strong>robust backend services</strong>, my goal is to deliver <strong>engaging, reliable, and innovative solutions</strong> across platforms.
    </p>
</div>
            <a href={ResumePath} role="button" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                Download Resume
            </a>
        </div>
    );
}


export default AboutMe;
