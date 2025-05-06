import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
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
  <Navbar expand="md" className="navbar-dark bg-dark fixed-top border-bottom">
    <Container fluid>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="me-auto">
          <Nav.Link href="#Information" style={{color:"white"}}>About</Nav.Link>
          <Nav.Link href="#Portfolio" style={{color:"white"}}>Portfolio</Nav.Link>
          <Nav.Link href="#Achievment" style={{color:"white"}}>Certificates</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default NavBar;
export {ScrollToSection};