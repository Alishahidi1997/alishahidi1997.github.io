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
                    I’m a multidisciplinary software developer passionate about creating immersive games and interactive digital experiences using Unity and C#. Over five years, I’ve built narrative-driven games, educational AR apps, and real-time multiplayer systems, prioritizing performance, accessibility, and player engagement.
                </p>
                <p>
                    My expertise includes AI-driven systems, GPT-powered avatars, real-time data processing, and cross-platform optimization. I’ve designed server pipelines, implemented analytics, and optimized gameplay mechanics to enhance user experience across mobile, WebXR, and VR platforms.
                </p>
                <p>
                    I have contributed to high-impact projects at ETHEREAL Research Group, Telus, ELIXR, and Illumia—leading assistive XR research, developing commercial AR solutions, and shipping polished applications with measurable performance improvements.
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
    I’m passionate about creating innovative gaming and AR/VR experiences on PC, mobile, and immersive platforms. Leveraging my experience with VR simulations, AR apps, and multiplayer systems, I combine storytelling, gameplay mechanics, and technology to deliver engaging and polished player experiences.
</p>     </div>
            <a href={ResumePath} role="button" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                Download Resume
            </a>
        </div>
    );
}


export default AboutMe;
