import React from "react";
// import profilePic from "../Assets/"; 
import ResumePath from "../Assets/AliShahidiResume.pdf";
function showPdf(){
    
}
function AboutMe(){
    const pdfPath = "../Assets/AliShahidiResume.pdf";
    const summaryAboutMe = "I am a dedicated grad research/teaching assistant at the University of Calgary, pursuing a master's in computer software engineering. Leading an AR education app project for non-speaking autistic individuals. With 4+ years in Unity and C#, and a Udemy certification, I'm proficient in C#, AR, Unity 3D, Python, and game development.\
    Having recently completed \"The Complete 2023 Web Development Bootcamp,\" I've acquired an extensive skill set encompassing Front-End technologies such as HTML, CSS, JavaScript, and React.js, alongside Backend proficiency in Node.js, Express.js, and PostgreSQL.\
    My training has equipped me to excel in both web development and game development, offering expertise in building dynamic and scalable applications. As I pursue opportunities, I am eager to contribute my robust skills to innovative projects and bring valuable insights to the team."
    return(
        <div class="col-8 align-self-center">
        <h2 style={{ fontWeight: 'bold' }}>About Me</h2>
        <div class="lead text-muted "> 
       
<p>I am a multidisciplinary software developer specializing in Unity, C#, and XR technologies, creating immersive AR/VR applications, games, and cross-platform solutions. With over five years of hands-on experience, I have contributed to high-impact projects in augmented reality, game development, and interactive simulations. My expertise spans real-time data processing, AI-driven systems, multiplayer functionality, and performance optimization.</p>

<p>From academia to industry, I have led research in assistive XR technologies, collaborated on innovative AR projects, and developed applications for mobile, VR, and WebXR platforms. During my time at ETHEREAL Research Group, Telus, ELIXR, and Illumia, I focused on delivering scalable, high-performance applications that prioritize user engagement and cutting-edge innovation.</p>

<p>I hold certifications in:</p>
<ul>
    <li><strong>Programming Design Patterns For Unity: Write Better Code</strong> (July 2024)</li>
    <li><strong>The Beginner’s Guide to Animation in Unity</strong> (June 2024)</li>
    <li><strong>The Complete 2023 Web Development Bootcamp</strong> (January 2024)</li>
    <li><strong>Unity C# Mobile Game Development: Make 3 Games From Scratch</strong> (October 2023)</li>
    <li><strong>Complete C# Unity Game Developer 3D</strong> (September 2023)</li>
</ul>

<p>These certifications have broadened my expertise in front-end technologies (HTML, CSS, JavaScript, React.js), back-end technologies (Node.js, Express.js, PostgreSQL), and Unity-based mobile and VR/AR development.</p>

<p>If you're looking for collaboration opportunities in AR/VR or software development, feel free to send me a message!</p>
</div>
        <a href={ResumePath} role="button" class="btn btn-secondary" target="_blank">Download Resume</a>
         </div>

    )
}

export default AboutMe;
