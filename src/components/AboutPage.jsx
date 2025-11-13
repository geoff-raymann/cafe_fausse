import React from 'react';

function AboutPage() {
  return (
    <div className="about-page">
      <div className="about-hero">
        <h2>Our Story</h2>
        <p>Where tradition meets innovation</p>
      </div>
      
      <div className="about-content">
        <section className="about-history">
          <h3>About Café Fausse</h3>
          <p>
            Founded in 2010 by Chef Antonio Rossi and restaurateur Maria Lopez, 
            Café Fausse blends traditional Italian flavors with modern culinary innovation. 
            Our mission is to provide an unforgettable dining experience that reflects 
            both quality and creativity.
          </p>
        </section>

        <div className="founders-grid">
          <div className="founder-card">
            <div className="founder-image-placeholder">
              <span>Chef Antonio Rossi</span>
            </div>
            <h4>Chef Antonio Rossi</h4>
            <p>
              With over 20 years of culinary experience trained in Milan, 
              Chef Rossi brings authentic Italian techniques combined with 
              innovative flavor combinations that surprise and delight our guests.
            </p>
          </div>

          <div className="founder-card">
            <div className="founder-image-placeholder">
              <span>Maria Lopez</span>
            </div>
            <h4>Maria Lopez</h4>
            <p>
              A visionary restaurateur with a passion for creating memorable 
              experiences. Maria ensures every aspect of Café Fausse, from 
              ambiance to service, exceeds expectations.
            </p>
          </div>
        </div>

        <section className="mission-section">
          <h3>Our Commitment</h3>
          <div className="commitment-points">
            <div className="point">
              <h4>🌱 Locally Sourced</h4>
              <p>We partner with local farms and producers to bring you the freshest ingredients.</p>
            </div>
            <div className="point">
              <h4>✨ Unforgettable Dining</h4>
              <p>Every dish is crafted to create lasting memories and exceptional flavors.</p>
            </div>
            <div className="point">
              <h4>🍝 Traditional Excellence</h4>
              <p>Honoring Italian culinary traditions while embracing modern techniques.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default AboutPage;