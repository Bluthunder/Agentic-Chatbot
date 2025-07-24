import React from 'react';
import './airline.css';

const Destinations = () => {
  return (
    <section id="destinations" className="destinations">
        <div className="container">
            <h2 className="section-title">Popular Destinations</h2>
            <div className="destinations-grid">
                <div className="destination-card">
                    <div className="destination-image">🗽</div>
                    <div className="destination-content">
                        <h3>New York</h3>
                        <p>The city that never sleeps awaits you with its iconic skyline and endless possibilities.</p>
                        <div className="price">From $299</div>
                    </div>
                </div>
                <div className="destination-card">
                    <div className="destination-image">🗼</div>
                    <div className="destination-content">
                        <h3>Paris</h3>
                        <p>Experience the magic of the City of Light with its art, culture, and romance.</p>
                        <div className="price">From $399</div>
                    </div>
                </div>
                <div className="destination-card">
                    <div className="destination-image">🏛️</div>
                    <div className="destination-content">
                        <h3>Rome</h3>
                        <p>Discover ancient history and modern charm in the Eternal City.</p>
                        <div className="price">From $349</div>
                    </div>
                </div>
                <div className="destination-card">
                    <div className="destination-image">🏯</div>
                    <div className="destination-content">
                        <h3>Tokyo</h3>
                        <p>Immerse yourself in the perfect blend of tradition and innovation.</p>
                        <div className="price">From $599</div>
                    </div>
                </div>
                <div className="destination-card">
                    <div className="destination-image">🏖️</div>
                    <div className="destination-content">
                        <h3>Bali</h3>
                        <p>Paradise found with pristine beaches, lush landscapes, and spiritual tranquility.</p>
                        <div className="price">From $249</div>
                    </div>
                </div>
                <div className="destination-card">
                    <div className="destination-image">🏔️</div>
                    <div className="destination-content">
                        <h3>Switzerland</h3>
                        <p>Alpine adventures and breathtaking scenery in the heart of Europe.</p>
                        <div className="price">From $449</div>
                    </div>
                </div>
            </div>
        </div>
    </section>
  );
};

export default Destinations;
