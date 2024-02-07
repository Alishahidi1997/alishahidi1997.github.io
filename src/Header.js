import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import ResumePath from "./Assets/AliShahidiResume.pdf";
import AboutMe from './AboutMe/aboutMe';

const NavBar = () => (
  <nav class=" navbar navbar-expand-md navbar-dark bg-dark fixed-top border-bottom" >
  <a class="ms-4 navbar-brand" href="#">    </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="d-flex justify-content-end">
  <ul class="navbar-nav">
    <li class="nav-item active">
      <a class="nav-link" href="#" style={{color:"white"}}>Home <span class="sr-only">(current)</span></a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#" style={{color:"white"}}>Portfolio</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#" style={{color:"white"}}>Achievements</a>
    </li>
  </ul>
</div>

</nav>

)

export default NavBar;