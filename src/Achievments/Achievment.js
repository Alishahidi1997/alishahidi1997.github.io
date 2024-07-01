import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Carousel, Container, Row, Col } from 'react-bootstrap';
import UnityCertificate from "../Assets/Achievments/UnityCertificate.png";
import WebCertificate from "../Assets/Achievments/WebCertificate.jpg";
import AnimationCertificate from "../Assets/Achievments/AnimationCertificate.png";
import UnityMobile from "../Assets/Achievments/UnityMobile.jpg";
// import CarouselItem from './CarouselItem'; // Import your new CarouselItem component

let certificates = [
    {
        src: WebCertificate, 
        name: "The Complete 2023 Web Development Bootcamp"
    },
    {
    src: UnityCertificate,
    name: "Complete C# Unity Game Developer 3D",
    },
    {
      src: AnimationCertificate,
      name: "The Beginner's Guide to Animation in Unity",
    },
    {
      src: UnityMobile,
      name: "Unity C# Mobile Game Development: Make 3 Games From Scratch",
    }
]

let certificate = certificates.map(function(item) {
    return (
        <Carousel.Item>
        <img className="d-block w-100" src={item.src} alt="Slide" />
        <Carousel.Caption>
            <p>{item.name}</p>
        </Carousel.Caption>
        </Carousel.Item>
    )
  });
  

const Achievment = () => {
  return (
    <div class="bg-dark bg-gradient" id="Achievment">
    <h3 class="py-5 text-center" style={{ fontWeight: 'bold' }}>Certificates</h3>
    <Container fluid>
      <Row className="justify-content-center align-items-center ">
        <Col xs={12} md={9} lg={6}>
          <Carousel style={{ width: '100%' }}>
          {certificate}
          </Carousel>
        </Col>
      </Row>
    </Container>
    </div>
  );
};

export default Achievment;