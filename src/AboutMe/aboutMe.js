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
       
<p>I am a software developer at Telus, specializing in developing cross-platform augmented reality applications for iOS and Meta Quest 2. With over four years of experience in Unity and C#, I have expertise in AR development, game development, and multiplayer functionalities.
At Telus, I contributed to our application's multiplayer version using NetCode and spatial anchor functionality. I have also led projects like HoloType, a 3D interactive educational app using HoloLens 2.</p>

<p>I hold certifications in:</p>
<ul>
    <li><strong>Programming Design Patterns For Unity: Write Better Code</strong> (July 2024)</li>
    <li><strong>The Beginner’s Guide to Animation in Unity</strong> (June 2024)</li>
    <li><strong>The Complete 2023 Web Development Bootcamp</strong> (January 2024)</li>
    <li><strong>Unity C# Mobile Game Development: Make 3 Games From Scratch</strong> (October 2023)</li>
    <li><strong>Complete C# Unity Game Developer 3D</strong> (September 2023)</li>
</ul>

<p>These certifications have expanded my skills in front-end technologies (HTML, CSS, JavaScript, React.js) and backend technologies (Node.js, Express.js, PostgreSQL). Additionally, I have enhanced my abilities in mobile gaming and VR/AR development using Unity.</p>

<p>I am eager to apply my skills to innovative projects and contribute valuable insights to any team.</p>
</div>
        <a href={ResumePath} role="button" class="btn btn-secondary" target="_blank">Download Resume</a>
         </div>

    )
}

export default AboutMe;