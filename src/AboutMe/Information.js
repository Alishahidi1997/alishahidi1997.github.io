import React, { useState, useEffect } from 'react';
import profilePic from "../Assets/Ali.jpg"; 
import { Linkedin, Github, EnvelopeFill } from 'react-bootstrap-icons';
import 'bootstrap/dist/css/bootstrap.min.css';
import Icons from './icons';
import AboutMe from './aboutMe';
import userData from '../userInfo.json';


function Information(){
    const [userInfo, setUserData] = useState(userData);
    
return(
        <section class="py-sm-5 ms-5 ">
                <div class="row">
                    <div class="col-lg-4 text-center">
                        <img class="rounded mx-auto " height={300} width={300} src={profilePic} alt="Profile Picture" />
                        {/* <h2 class="jumbotron-heading m-2">{name}</h2> */}
                        <p style={{color:'gray'}}>{userInfo.city}</p>
                        <div class="container">
                            <Icons icon={EnvelopeFill} link={`mailto: ${userInfo.mail}`} altText="Email"/>
                            <Icons icon={Github} link={userInfo.github} altText="Github" />
                            <Icons icon={Linkedin} link={userInfo.linkedin} altText="Linkdin" />
                        </div>        
                    </div>
                    <div class="col-lg-8">
                    <AboutMe /> 
                    </div>
                </div>
            </section>
)
}

export default Information; 
