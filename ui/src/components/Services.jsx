import React from 'react';
import './airline.css';

const Services = () => {
  return (
    <section id="services" className="services">
        <div className="container">
            <h2 className="section-title">Our Services</h2>
            <div className="services-grid">
                <div className="service-card">
                    <div className="service-icon">✈️</div>
                    <h3 style={{color: 'black'}}>Flight Booking</h3>
                    <p style={{color: 'black'}}>Book domestic and international flights with ease. Get the best deals and flexible options.</p>
                </div>
                <div className="service-card">
                    <div className="service-icon">🏨</div>
                    <h3 style={{ccolor: 'black'}}>Hotel Reservations</h3>
                    <p style={{color: 'black'}}>Find and book the perfect accommodation for your stay with our curated selection.</p>
                </div>
                <div className="service-card">
                    <div className="service-icon">🚗</div>
                    <h3 style={{color: 'black'}}>Car Rentals</h3>
                    <p style={{color: 'black'}}>Explore your destination with our reliable car rental service and competitive rates.</p>
                </div>
                <div className="service-card">
                    <div className="service-icon">🎫</div>
                    <h3 style={{color: 'black'}}>Travel Insurance</h3>
                    <p style={{color: 'black'}}>Travel with peace of mind with our comprehensive insurance coverage options.</p>
                </div>
                <div className="service-card">
                    <div className="service-icon">🎯</div>
                    <h3 style={{color: 'black'}}>Travel Packages</h3>
                    <p style={{color: 'black'}}>All-inclusive packages that combine flights, hotels, and activities for the perfect trip.</p>
                </div>
                <div className="service-card">
                    <div className="service-icon">📞</div>
                    <h3 style={{color: 'black'}}>24/7 Support</h3>
                    <p style={{color: 'black'}}>Round-the-clock Barry to assist you with any travel-related queries.</p>
                </div>
            </div>
        </div>
    </section>
  );
};

export default Services;
