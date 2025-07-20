import React from 'react';
import './airline.css';

const Navbar = () => {
  return (
    <nav className="navbar">
        <div className="nav-container">
            <div className="logo">✈️ Skyline Airways</div>
            <ul className="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#destinations">Destinations</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>
  );
};

export default Navbar;
