import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import ResumePath from "./Assets/AliShahidiResume.pdf";
import AboutMe from './AboutMe/aboutMe';
import { Link, animateScroll as scroll } from 'react-scroll';
import App from './App';
import Portfolio from './Portfolio/Portfolio';
import Footer from './Footer';
import Achievment from './Achievments/Achievment';
import Information from './AboutMe/Information';
const ScrollToSection = () => {
  const scrollToTop = () => {
    scroll.scrollToTop();
  };};




const NavBar = () => (
  <nav class=" navbar navbar-expand-md navbar-dark bg-dark fixed-top border-bottom" >
  <a class="ms-4 navbar-brand" href="#">    </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="d-flex justify-content-end">
  <ul class="navbar-nav">
    <li class="nav-item active">
      <a class="nav-link" href="#Information" style={{color:"white"}}>About </a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#Portfolio" style={{color:"white"}}>Portfolio</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#Achievment" style={{color:"white"}}>Certificates</a>
    </li>
  </ul>
</div>

</nav>
)

export default NavBar;
export {ScrollToSection};