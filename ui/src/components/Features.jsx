import React from 'react';
import './airline.css';

const Features = () => {
  return (
    <section className="features">
        <div className="container">
            <h2 className="section-title">Why Choose Skyline Airways?</h2>
            <div className="features-grid">
                <div className="feature-card">
                    <div className="feature-icon">🤖</div>
                    <h3>AI-Powered Assistant</h3>
                    <p>Get instant help with booking, flight status, and travel queries through our intelligent chatbot.</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon">⚡</div>
                    <h3>Instant Booking</h3>
                    <p>Book your flights in seconds with our streamlined booking process and real-time availability.</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon">🌍</div>
                    <h3>Global Coverage</h3>
                    <p>Access flights to over 500 destinations worldwide with competitive prices and flexible schedules.</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon">🛡️</div>
                    <h3>Secure & Reliable</h3>
                    <p>Your data is protected with industry-leading security measures and 24/7 customer support.</p>
                </div>
            </div>
        </div>
    </section>
  );
};

export default Features;
