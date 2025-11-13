import React, { useState } from 'react';

function ReservationsPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    time_slot: '',
    guests: 2,
    special_requests: ''
  });
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('Processing your reservation...');

    // Validate required fields
    if (!formData.name || !formData.email || !formData.time_slot) {
      setMessage('Please fill in all required fields.');
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/reservations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(result.message);
        // Clear the form
        setFormData({ 
          name: '', 
          email: '', 
          phone: '', 
          time_slot: '', 
          guests: 2,
          special_requests: '' 
        });
      } else {
        setMessage(`Error: ${result.error}`);
      }
    } catch (error) {
      setMessage('Unable to process reservation. Please try again or call us directly.');
      console.error('Reservation error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Generate time slots
  const generateTimeSlots = () => {
    const slots = [];
    const startHour = 17; // 5 PM
    const endHour = 22; // 10 PM
    
    for (let hour = startHour; hour <= endHour; hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const timeString = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
        slots.push(timeString);
      }
    }
    return slots;
  };

  const getNextTwoWeeks = () => {
    const dates = [];
    const today = new Date();
    
    for (let i = 1; i <= 14; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(date.toISOString().split('T')[0]);
    }
    return dates;
  };

  const handleDateChange = (e) => {
    const timePart = formData.time_slot.split('T')[1] || '18:00';
    const timeSlot = `${e.target.value}T${timePart}`;
    setFormData({ ...formData, time_slot: timeSlot });
  };

  const handleTimeChange = (e) => {
    const datePart = formData.time_slot.split('T')[0] || getNextTwoWeeks()[0];
    const timeSlot = `${datePart}T${e.target.value}`;
    setFormData({ ...formData, time_slot: timeSlot });
  };

  return (
    <div className="reservations-page">
      <div className="page-header">
        <h1 className="page-title">Make a Reservation</h1>
        <p className="page-subtitle">Secure your table for an unforgettable dining experience</p>
      </div>

      <div className="reservation-layout">
        <div className="reservation-sidebar">
          <div className="sidebar-card">
            <div className="card-icon">📞</div>
            <h3>Need Immediate Assistance?</h3>
            <p>Call us directly at</p>
            <p className="phone-number">(202) 555-4567</p>
          </div>

          <div className="sidebar-card">
            <div className="card-icon">⏰</div>
            <h3>Dining Hours</h3>
            <p><strong>Monday–Saturday:</strong><br />5:00PM – 11:00 PM</p>
            <p><strong>Sunday:</strong><br />5:00 PM – 9:00 PM</p>
          </div>

          <div className="sidebar-card">
            <div className="card-icon">🎉</div>
            <h3>Special Occasions?</h3>
            <p>Mention any celebrations in the special requests field for a complimentary surprise.</p>
          </div>
        </div>

        <div className="reservation-main">
          <form onSubmit={handleSubmit} className="reservation-form">
            <div className="form-section">
              <h3 className="section-title">Personal Information</h3>
              <div className="form-grid">
                <div className="form-group full-width">
                  <label htmlFor="name">Full Name *</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="form-control"
                    placeholder="Enter your full name"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="email">Email Address *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="form-control"
                    placeholder="your.email@example.com"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="form-control"
                    placeholder="(555) 123-4567"
                  />
                </div>
              </div>
            </div>

            <div className="form-section">
              <h3 className="section-title">Reservation Details</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="guests">Number of Guests *</label>
                  <select
                    id="guests"
                    name="guests"
                    value={formData.guests}
                    onChange={handleChange}
                    className="form-control"
                    required
                  >
                    {[1, 2, 3, 4, 5, 6, 7, 8].map(num => (
                      <option key={num} value={num}>
                        {num} {num === 1 ? 'Person' : 'People'}
                      </option>
                    ))}
                    <option value="10">10+ People (Large Party)</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label htmlFor="date">Date *</label>
                  <select
                    id="date"
                    name="date"
                    value={formData.time_slot.split('T')[0] || ''}
                    onChange={handleDateChange}
                    className="form-control"
                    required
                  >
                    <option value="">Select a date</option>
                    {getNextTwoWeeks().map(date => (
                      <option key={date} value={date}>
                        {new Date(date).toLocaleDateString('en-US', { 
                          weekday: 'short', 
                          month: 'short', 
                          day: 'numeric' 
                        })}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div className="form-group">
                  <label htmlFor="time">Time *</label>
                  <select
                    id="time"
                    name="time"
                    value={formData.time_slot.split('T')[1] || ''}
                    onChange={handleTimeChange}
                    className="form-control"
                    required
                  >
                    <option value="">Select a time</option>
                    {generateTimeSlots().map(time => (
                      <option key={time} value={time}>
                        {new Date(`2000-01-01T${time}`).toLocaleTimeString('en-US', { 
                          hour: 'numeric', 
                          minute: '2-digit',
                          hour12: true 
                        })}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="form-section">
              <h3 className="section-title">Additional Information</h3>
              <div className="form-group full-width">
                <label htmlFor="special_requests">Special Requests</label>
                <textarea
                  id="special_requests"
                  name="special_requests"
                  value={formData.special_requests}
                  onChange={handleChange}
                  className="form-control"
                  placeholder="Any dietary restrictions, allergies, or special occasion notes..."
                  rows="4"
                />
              </div>
            </div>

            <button 
              type="submit" 
              className={`submit-button ${isSubmitting ? 'submitting' : ''}`}
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="loading-spinner"></span>
                  Processing...
                </>
              ) : (
                'Reserve Your Table'
              )}
            </button>

            {message && (
              <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
                {message}
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

export default ReservationsPage;