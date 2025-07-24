import React from 'react';
import './airline.css';

const Hero = () => {
  return (
    <section id="home" className="hero">
        <div className="hero-content">
            <h1>Connecting Continents</h1>
            <p>Travel the world with us, experience the culture </p>
            <a href="#destinations" className="cta-button">Explore Destinations</a>
        </div>
    </section>
  );
};

export default Hero;
