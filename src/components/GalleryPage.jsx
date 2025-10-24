import React, { useState } from 'react';

function GalleryPage() {
  const [selectedImage, setSelectedImage] = useState(null);

  // Sample gallery images - you can replace these with actual images
  const galleryImages = [
    { id: 1, type: 'interior', title: 'Main Dining Room', description: 'Our elegant main dining area' },
    { id: 2, type: 'interior', title: 'Private Booth', description: 'Intimate dining experience' },
    { id: 3, type: 'interior', title: 'Wine Cellar', description: 'Extensive wine selection' },
    { id: 4, type: 'dish', title: 'Grilled Salmon', description: 'Our signature grilled salmon dish' },
    { id: 5, type: 'dish', title: 'Ribeye Steak', description: 'Prime cut with garlic mashed potatoes' },
    { id: 6, type: 'dish', title: 'Tiramisu', description: 'Classic Italian dessert' },
    { id: 7, type: 'event', title: 'Wine Tasting', description: 'Monthly wine tasting events' },
    { id: 8, type: 'event', title: 'Chef Table', description: 'Exclusive chef table experience' },
  ];

  const openLightbox = (image) => {
    setSelectedImage(image);
  };

  const closeLightbox = () => {
    setSelectedImage(null);
  };

  return (
    <div className="gallery-page">
      <h2>Gallery</h2>
      
      {/* Awards Section */}
      <section className="awards-section">
        <h3>Our Awards & Recognition</h3>
        <div className="awards-grid">
          <div className="award-card">
            <div className="trophy">🏆</div>
            <h4>Culinary Excellence Award</h4>
            <p>2022</p>
          </div>
          <div className="award-card">
            <div className="trophy">⭐</div>
            <h4>Restaurant of the Year</h4>
            <p>2023</p>
          </div>
          <div className="award-card">
            <div className="trophy">🍽️</div>
            <h4>Best Fine Dining Experience</h4>
            <p>Foodie Magazine, 2023</p>
          </div>
        </div>
      </section>

      {/* Customer Reviews */}
      <section className="reviews-section">
        <h3>What Our Guests Say</h3>
        <div className="reviews-grid">
          <div className="review-card">
            <p>"Exceptional ambiance and unforgettable flavors. Every visit is a culinary journey!"</p>
            <cite>– Gourmet Review</cite>
          </div>
          <div className="review-card">
            <p>"A must-visit restaurant for food enthusiasts. The attention to detail is remarkable."</p>
            <cite>– The Daily Bite</cite>
          </div>
          <div className="review-card">
            <p>"The perfect blend of traditional Italian and modern innovation. Simply outstanding!"</p>
            <cite>– Food & Wine Magazine</cite>
          </div>
        </div>
      </section>

      {/* Image Gallery */}
      <section className="image-gallery">
        <h3>Visual Journey</h3>
        <div className="gallery-grid">
          {galleryImages.map((image) => (
            <div 
              key={image.id} 
              className="gallery-item"
              onClick={() => openLightbox(image)}
            >
              <div className="image-placeholder">
                <span>{image.title}</span>
              </div>
              <div className="image-info">
                <h4>{image.title}</h4>
                <p>{image.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Lightbox Modal */}
      {selectedImage && (
        <div className="lightbox" onClick={closeLightbox}>
          <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={closeLightbox}>×</button>
            <div className="lightbox-image-placeholder">
              <span>{selectedImage.title}</span>
            </div>
            <div className="lightbox-info">
              <h3>{selectedImage.title}</h3>
              <p>{selectedImage.description}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default GalleryPage;