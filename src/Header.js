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
  };
};

const NavBar = () => (
  <nav className="navbar navbar-expand-md navbar-dark bg-dark fixed-top border-bottom">
    <div className="container-fluid">
      <a className="navbar-brand" href="#">Ali Shahidi</a>
      <button 
        className="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav" 
        aria-controls="navbarNav" 
        aria-expanded="false" 
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav ms-auto">
          <li className="nav-item">
            <a className="nav-link" href="#Information">About</a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#Portfolio">Portfolio</a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#Achievment">Certificates</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
);

export default NavBar;
export {ScrollToSection};