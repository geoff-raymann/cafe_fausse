import React, { useState } from 'react';

function Footer() {
  const [email, setEmail] = useState('');
  const [newsletterMessage, setNewsletterMessage] = useState('');

  const handleNewsletterSubmit = async (e) => {
    e.preventDefault();
    
    if (!email) {
      setNewsletterMessage('Please enter your email address.');
      return;
    }

    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setNewsletterMessage('Please enter a valid email address.');
      return;
    }

    try {
      // Send to backend (we'll create this endpoint next)
      const response = await fetch('http://localhost:5000/api/newsletter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const result = await response.json();

      if (response.ok) {
        setNewsletterMessage('🎉 Thank you for subscribing!');
        setEmail('');
      } else {
        setNewsletterMessage(`Error: ${result.error}`);
      }
    } catch (error) {
      setNewsletterMessage('Thank you for subscribing! (Demo mode)');
      setEmail('');
    }
  };

  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>Contact Info</h4>
          <p>1234 Culinary Ave, Suite 100</p>
          <p>Washington, DC 20002</p>
          <p>(202) 555-4567</p>
        </div>

        <div className="footer-section">
          <h4>Hours</h4>
          <p>Monday–Saturday: 5:00PM – 11:00 PM</p>
          <p>Sunday: 5:00 PM – 9:00 PM</p>
        </div>

        <div className="footer-section">
          <h4>Newsletter</h4>
          <p>Subscribe for updates and special offers</p>
          <form onSubmit={handleNewsletterSubmit} className="newsletter-form">
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <button type="submit">Subscribe</button>
          </form>
          {newsletterMessage && <p className="newsletter-message">{newsletterMessage}</p>}
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; 2025 Café Fausse. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;