
import React from 'react';
import { Carousel } from 'react-bootstrap';

const CarouselItem = ({ src, captionTitle, captionText }) => {
  return (
    <Carousel.Item>
    <img className="d-block w-100" src="https://placekitten.com/800/400" alt="Slide" />
    <Carousel.Caption>
        <h3>First Slide</h3>
        <p>This is the first slide's content.</p>
    </Carousel.Caption>
    </Carousel.Item>
  );
};

export default CarouselItem;