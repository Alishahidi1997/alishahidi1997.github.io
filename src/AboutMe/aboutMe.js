import React from "react";
// import profilePic from "../Assets/"; 
import ResumePath from "../Assets/AliShahidiResume.pdf";
function showPdf(){
    
}
function AboutMe(){
    const pdfPath = "../Assets/AliShahidiResume.pdf";
    const summaryAboutMe = "Dedicated grad research/teaching assistant at the University of Calgary, pursuing a master's in computer software engineering. Leading an AR education app project for non-speaking autistic individuals. With 3+ years in Unity and C#, and a Udemy certification, I'm proficient in C#, AR, Unity 3D, Python, and game development.\
    Having recently completed \"The Complete 2023 Web Development Bootcamp,\" I've acquired an extensive skill set encompassing Front-End technologies such as HTML, CSS, JavaScript, and React.js, alongside Backend proficiency in Node.js, Express.js, and PostgreSQL.\
    My training has equipped me to excel in both web development and game development, offering expertise in building dynamic and scalable applications. As I pursue opportunities, I am eager to contribute my robust skills to innovative projects and bring valuable insights to the team."
    return(
        <div class="col-8 align-self-center">
        <h2 style={{ fontWeight: 'bold' }}>About Me</h2>
        <p class="lead text-muted "> {summaryAboutMe} </p>
        <a href={ResumePath} role="button" class="btn btn-secondary" target="_blank">Download Resume</a>
         </div>

    )
}

export default AboutMe;