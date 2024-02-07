import React,{useState} from "react";
import Icons from "./AboutMe/icons";
import { Linkedin, Github, EnvelopeFill } from 'react-bootstrap-icons';
import userData from './userInfo.json';


function Footer(){

  const [userInfo, setUserData] = useState(userData);

    return(
        <div class="container">
  <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
    <div class="col-md-4 d-flex align-items-center">
      <a href="/" class="mb-3 me-2 mb-md-0 text-muted text-decoration-none lh-1">
        {/* <svg class="bi" width="30" height="24"><use xlink:href="#bootstrap"></use></svg> */}
      </a>
      <span class="text-muted">© 2024, Ali Shahidi</span>
    </div>

    <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
      <li class="ms-3"><Icons icon={EnvelopeFill} link={`mailto: ${userInfo.mail}`} altText="Email"/></li>
      <li class="ms-3"><Icons icon={Github} link={userInfo.github} altText="Github" /></li>
      <li class="ms-3"><Icons icon={Linkedin} link={userInfo.linkedin} altText="Linkdin" /></li>
    </ul>
  </footer>
</div>
    )
}

export default Footer; 