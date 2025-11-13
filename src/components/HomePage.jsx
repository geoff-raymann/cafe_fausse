import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <p className="hero-subtitle">Fine Dining Experience</p>
          <h1 className="hero-title">Where Culinary Art Meets Elegance</h1>
          <p className="hero-description">
            Experience the perfect blend of traditional Italian flavors and modern culinary innovation in an intimate, sophisticated setting.
          </p>
          <Link to="/reservations" className="cta-button">Reserve Your Table</Link>
        </div>
      </section>

      {/* Info Cards */}
      <div className="info-cards">
        <div className="info-card">
          <h3>Visit Us</h3>
          <p><strong>Address:</strong><br />1234 Culinary Ave, Suite 100<br />Washington, DC 20002</p>
          <p><strong>Phone:</strong><br />(202) 555-4567</p>
        </div>
        
        <div className="info-card">
          <h3>Hours</h3>
          <p><strong>Monday–Saturday:</strong><br />5:00PM – 11:00 PM</p>
          <p><strong>Sunday:</strong><br />5:00 PM – 9:00 PM</p>
        </div>
        
        <div className="info-card">
          <h3>Awards</h3>
          <p>🍽️ Restaurant of the Year 2023</p>
          <p>⭐ Culinary Excellence Award 2022</p>
          <p>🏆 Best Fine Dining Experience 2023</p>
        </div>
      </div>
    </div>
  );
}

export default HomePage;