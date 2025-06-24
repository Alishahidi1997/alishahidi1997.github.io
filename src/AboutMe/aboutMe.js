import React from "react";
// import profilePic from "../Assets/"; 
import ResumePath from "../Assets/AliShahidiResume.pdf";

function showPdf(){
    // You can implement this if needed later
}

function AboutMe(){
    const summaryAboutMe = `I am a dedicated grad research/teaching assistant at the University of Calgary, pursuing a master's in computer software engineering. Leading an AR education app project for non-speaking autistic individuals. With 4+ years in Unity and C#, and a Udemy certification, I'm proficient in C#, AR, Unity 3D, Python, and game development.
    Having recently completed "The Complete 2023 Web Development Bootcamp," I've acquired an extensive skill set encompassing Front-End technologies such as HTML, CSS, JavaScript, and React.js, alongside Backend proficiency in Node.js, Express.js, and PostgreSQL.
    My training has equipped me to excel in both web development and game development, offering expertise in building dynamic and scalable applications. As I pursue opportunities, I am eager to contribute my robust skills to innovative projects and bring valuable insights to the team.`;

    return(
        <div className="col-8 align-self-center">
            <h2 style={{ fontWeight: 'bold' }}>About Me</h2>
            <div className="lead text-muted"> 
                <p>
                    I’m a multidisciplinary software developer passionate about building immersive digital experiences using Unity, C#, and XR technologies. With over five years of hands-on experience, I’ve developed interactive AR/VR applications, cross-platform software, and narrative-driven games that prioritize performance, usability, and impact.
                </p>
                <p>
                    Alongside my development work, I have strong expertise in real-time data processing, AI-driven systems, and data analytics. I’ve designed and optimized data pipelines, performed statistical analysis, and implemented automation to enhance system efficiency and user experience. My background includes building multiplayer architecture and applying data-driven insights to improve gameplay mechanics and user engagement across mobile, WebXR, and VR platforms.
                </p>
                <p>
                    I’ve contributed to high-impact projects at ETHEREAL Research Group, Telus, ELIXR, and Illumia—leading research in assistive XR, developing commercial AR solutions, and shipping polished gameplay experiences supported by data analytics and performance tuning.
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
                    Whether it’s building engaging AR tools, multiplayer systems, or leveraging data to deliver meaningful game experiences, I’m always excited to collaborate. Let’s connect!
                </p>
            </div>
            <a href={ResumePath} role="button" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">Download Resume</a>
        </div>
    );
}

export default AboutMe;
