import React from "react";
// import profilePic from "../Assets/"; 
import ResumePath from "../Assets/AliShahidiResume.pdf";

function showPdf(){
    // You can implement this if needed later
}
function AboutMe() {
    const summaryAboutMe = `I am a multidisciplinary software developer with a Master's in Software Engineering from the University of Calgary and over 5 years of experience in Unity, C#, XR, and AR/VR technologies. I have led projects including immersive VR simulations, interactive AR educational apps, and multiplayer systems, integrating AI-driven avatars and real-time data processing. 
    While I enjoy building applications across AR/VR and interactive experiences, I am especially passionate about gaming development, creating narrative-driven games, engaging mechanics, and high-performance gameplay. 
    I am proficient in Unity 3D, C#, Python, C/C++, and full-stack web development (HTML, CSS, JavaScript, React.js, Node.js, Express.js, PostgreSQL). I hold multiple Unity and web development certifications and am eager to bring my skills and creativity to innovative gaming projects.`;

    return (
        <div className="col-8 align-self-center">
            <h2 style={{ fontWeight: 'bold' }}>About Me</h2>
            <div className="lead text-muted">
            <p>
    I’m a multidisciplinary software developer passionate about creating immersive games and interactive experiences using <strong>Unreal Engine 5</strong>, <strong>Unity</strong>, <strong>C++</strong>, and <strong>C#</strong>. Over the past five years, I’ve built narrative-driven games, VR simulations, and real-time multiplayer systems, with a focus on performance, scalability, and player engagement.
</p>
<p>
    My expertise spans <strong>AI-driven gameplay systems</strong>, <strong>GPT-powered avatars</strong>, <strong>real-time data pipelines</strong>, and <strong>cross-platform optimization</strong>. I’ve extended engine functionality through <strong>custom plugins</strong>, <strong>Control Rig</strong>, <strong>PCG</strong>, and <strong>Editor Utility Widgets</strong>, while also designing reusable frameworks to streamline development across PC, mobile, and VR.
</p>
<p>
    I’ve contributed to high-impact projects at <strong>ETHEREAL Research Group</strong>, <strong>Telus</strong>, <strong>ELIXR</strong>, and <strong>Illumia</strong>—leading assistive XR research, developing commercial AR/VR solutions, and delivering polished applications with measurable performance improvements.
</p>
<p>I hold certifications in:</p>
<ul>
    <li><strong>Programming Design Patterns for Unity</strong> (2024)</li>
    <li><strong>Animation in Unity</strong> (2024)</li>
    <li><strong>The Complete Web Development Bootcamp</strong> (2023)</li>
    <li><strong>Unity Mobile Game Development</strong> (2023)</li>
    <li><strong>Unity 3D Game Development</strong> (2023)</li>
</ul>
<p>
    I’m driven by the challenge of blending creativity and engineering to push the boundaries of real-time interaction. Whether developing scalable gameplay systems in Unreal or building cross-platform AR/VR experiences in Unity, my goal is to craft engaging, high-performance projects that inspire and immerse players.
</p>
</div>
            <a href={ResumePath} role="button" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                Download Resume
            </a>
        </div>
    );
}


export default AboutMe;
