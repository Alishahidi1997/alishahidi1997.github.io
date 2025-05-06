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
       
        <p>I’m a multidisciplinary software developer passionate about building immersive digital experiences using Unity, C#, and XR technologies. With over five years of hands-on experience, I’ve developed interactive AR/VR applications, cross-platform software, and narrative-driven games that prioritize performance, usability, and impact.</p>

<p>My core strengths include real-time data processing, AI-driven systems, multiplayer architecture, and optimization for mobile, WebXR, and VR platforms. From designing gamified learning tools to creating engaging gameplay mechanics, I bring both creative and technical depth to every project.</p>

<p>I’ve contributed to high-impact work at ETHEREAL Research Group, Telus, ELIXR, and Illumia—leading research in assistive XR, developing commercial AR solutions, and shipping polished gameplay experiences across platforms.</p>

<p>I hold certifications in:</p>
<ul>
    <li><strong>Programming Design Patterns for Unity</strong> (2024)</li>
    <li><strong>Animation in Unity</strong> (2024)</li>
    <li><strong>The Complete Web Development Bootcamp</strong> (2023)</li>
    <li><strong>Unity Mobile Game Development</strong> (2023)</li>
    <li><strong>Unity 3D Game Development</strong> (2023)</li>
</ul>

<p>Whether it’s building engaging AR tools, multiplayer systems, or meaningful game experiences, I’m always excited to collaborate. Let’s connect!</p>

</div>
        <a href={ResumePath} role="button" class="btn btn-secondary" target="_blank">Download Resume</a>
         </div>

    )
}

export default AboutMe;
