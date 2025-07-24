import React from 'react';
import './airline.css';
import './ChatWidget.css';



const Footer = () => {

  return (
    <footer className="footer">
      <div className="container">
           <p>© {new Date().getFullYear()} Skyline Airways. All rights reserved.</p>
      </div>
      
    </footer>
  );
};

export default Footer;