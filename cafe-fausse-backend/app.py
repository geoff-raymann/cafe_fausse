from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import OperationalError
import re
from html import escape
import random
import jwt
import hashlib
from datetime import datetime, timedelta
from functools import wraps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database connection details
DB_HOST = "localhost"
DB_NAME = "cafe_fausse_db"
DB_USER = "postgres"
DB_PASS = "Pass123"

# Email Configuration from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
CAFE_NAME = os.getenv('CAFE_NAME', 'Café Fausse')
CAFE_PHONE = os.getenv('CAFE_PHONE', '(202) 555-4567')
CAFE_ADDRESS = os.getenv('CAFE_ADDRESS', '123 Quantum Street, Digital District')

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Successfully connected to database!")
        return conn
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check:")
        print("1. Is PostgreSQL running?")
        print("2. Is the database name correct?")
        print("3. Are the username and password correct?")
        return None

def create_tables():
    """Create the necessary tables if they don't exist"""
    conn = get_db_connection()
    if conn is None:
        print("❌ Cannot create tables - no database connection")
        return False
    
    try:
        cur = conn.cursor()
        
        # Create Customers table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                newsletter BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Reservations table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(id),
                time_slot TIMESTAMP NOT NULL,
                table_number INTEGER NOT NULL,
                guests INTEGER NOT NULL,
                special_requests TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if created_at column exists in customers table, if not add it
        cur.execute('''
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='customers' and column_name='created_at'
        ''')
        
        if not cur.fetchone():
            print("➡️ Adding 'created_at' column to customers table...")
            cur.execute('ALTER TABLE customers ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;')
            print("✅ Added 'created_at' column to customers table!")
        
        # Check if created_at column exists in reservations table, if not add it
        cur.execute('''
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='reservations' and column_name='created_at'
        ''')
        
        if not cur.fetchone():
            print("➡️ Adding 'created_at' column to reservations table...")
            cur.execute('ALTER TABLE reservations ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;')
            print("✅ Added 'created_at' column to reservations table!")
        
        # Check if guests column exists in reservations table, if not add it
        cur.execute('''
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='reservations' and column_name='guests'
        ''')
        
        if not cur.fetchone():
            print("➡️ Adding 'guests' column to reservations table...")
            cur.execute('ALTER TABLE reservations ADD COLUMN guests INTEGER NOT NULL DEFAULT 2;')
            print("✅ Added 'guests' column to reservations table!")
            
        # Check if special_requests column exists in reservations table, if not add it
        cur.execute('''
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='reservations' and column_name='special_requests'
        ''')
        
        if not cur.fetchone():
            print("➡️ Adding 'special_requests' column to reservations table...")
            cur.execute('ALTER TABLE reservations ADD COLUMN special_requests TEXT;')
            print("✅ Added 'special_requests' column to reservations table!")
        
        conn.commit()
        print("✅ Database tables are ready!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Test route to check database status
@app.route('/api/db-status')
def db_status():
    """Check if database is working"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': '✅ Database is connected and working!'})
    else:
        return jsonify({'status': '❌ Database connection failed!'}), 500

# Create tables when the app starts
print("🚀 Starting Café Fausse Backend...")
create_tables()

@app.route('/')
def home():
    return """
    <h1>🍽️ Café Fausse Backend is Running!</h1>
    <p>Check these endpoints:</p>
    <ul>
        <li><a href="/api/db-status">/api/db-status</a> - Check database connection</li>
        <li>POST /api/reservations - Make a reservation</li>
    </ul>
    """

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return text
    # Remove HTML tags and escape special characters
    text = re.sub(r'<[^>]+>', '', str(text))
    return escape(text).strip()

def send_booking_confirmation(customer_name, customer_email, booking_details):
    """Send booking confirmation email to customer"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🎉 Reservation Confirmed at {CAFE_NAME}"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = customer_email

        # Create HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 15px;
                    padding: 30px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }}
                .details-box {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    border-left: 5px solid #ffd700;
                }}
                .detail-item {{
                    margin: 10px 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .label {{
                    color: #ffd700;
                    font-weight: bold;
                }}
                .value {{
                    color: white;
                }}
                .special-requests {{
                    background: rgba(255, 215, 0, 0.1);
                    border-radius: 8px;
                    padding: 15px;
                    margin: 15px 0;
                    border-left: 3px solid #ffd700;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: rgba(255, 255, 255, 0.8);
                }}
                .contact-info {{
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 8px;
                    padding: 15px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🍰 {CAFE_NAME}</div>
                    <h2>Your Reservation is Confirmed!</h2>
                    <p>Dear {customer_name}, thank you for choosing our digital dining experience.</p>
                </div>

                <div class="details-box">
                    <h3 style="color: #ffd700; text-align: center; margin-bottom: 20px;">📋 Reservation Details</h3>
                    
                    <div class="detail-item">
                        <span class="label">📅 Date & Time:</span>
                        <span class="value">{booking_details['formatted_datetime']}</span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="label">🍽️ Table Number:</span>
                        <span class="value">#{booking_details['table_number']}</span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="label">👥 Number of Guests:</span>
                        <span class="value">{booking_details['guests']}</span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="label">🆔 Reservation ID:</span>
                        <span class="value">#{booking_details['reservation_id']}</span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="label">👤 Customer ID:</span>
                        <span class="value">#{booking_details['customer_id']}</span>
                    </div>
                </div>

                {f'''
                <div class="special-requests">
                    <h4 style="color: #ffd700; margin: 0 0 10px 0;">📝 Special Requests</h4>
                    <p style="margin: 0; line-height: 1.5;">{booking_details['special_requests']}</p>
                </div>
                ''' if booking_details.get('special_requests') else ''}

                <div class="contact-info">
                    <h4 style="color: #ffd700; margin: 0 0 10px 0;">📞 Contact Information</h4>
                    <p style="margin: 5px 0;"><strong>Phone:</strong> {CAFE_PHONE}</p>
                    <p style="margin: 5px 0;"><strong>Address:</strong> {CAFE_ADDRESS}</p>
                    <p style="margin: 5px 0;"><strong>Email:</strong> {EMAIL_ADDRESS}</p>
                </div>

                <div class="footer">
                    <h4 style="color: #ffd700;">🎊 What to Expect</h4>
                    <p>• Please arrive 10 minutes before your reservation time</p>
                    <p>• Your table will be held for 15 minutes past reservation time</p>
                    <p>• Experience our quantum-inspired digital menu</p>
                    <p>• Enjoy our immersive cyber atmosphere</p>
                    
                    <p style="margin-top: 20px;">
                        <strong>Need to modify or cancel?</strong><br>
                        Call us at {CAFE_PHONE} at least 2 hours in advance.
                    </p>
                    
                    <p style="margin-top: 30px; color: rgba(255, 255, 255, 0.6);">
                        Thank you for choosing {CAFE_NAME}!<br>
                        We look forward to serving you.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        # Create plain text version
        text_content = f"""
        🍰 {CAFE_NAME} - Reservation Confirmed!
        
        Dear {customer_name},
        
        Your reservation has been confirmed! Here are the details:
        
        📋 RESERVATION DETAILS:
        📅 Date & Time: {booking_details['formatted_datetime']}
        🍽️ Table Number: #{booking_details['table_number']}
        👥 Number of Guests: {booking_details['guests']}
        🆔 Reservation ID: #{booking_details['reservation_id']}
        👤 Customer ID: #{booking_details['customer_id']}
        
        {f"📝 Special Requests: {booking_details['special_requests']}" if booking_details.get('special_requests') else ''}
        
        📞 CONTACT INFORMATION:
        Phone: {CAFE_PHONE}
        Address: {CAFE_ADDRESS}
        Email: {EMAIL_ADDRESS}
        
        🎊 WHAT TO EXPECT:
        • Please arrive 10 minutes before your reservation time
        • Your table will be held for 15 minutes past reservation time
        • Experience our quantum-inspired digital menu
        • Enjoy our immersive cyber atmosphere
        
        Need to modify or cancel? Call us at {CAFE_PHONE} at least 2 hours in advance.
        
        Thank you for choosing {CAFE_NAME}!
        We look forward to serving you.
        """

        # Attach parts
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    print("📨 Received reservation data:", data)

    # Sanitize inputs
    name = sanitize_input(data.get('name'))
    email = sanitize_input(data.get('email'))
    phone = sanitize_input(data.get('phone'))
    special_requests = sanitize_input(data.get('special_requests'))
    time_slot = data.get('time_slot')
    guests = data.get('guests')

    # Validation
    if not all([name, email, time_slot, guests]):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()

        # 1. Insert or get the customer
        cur.execute(
            """INSERT INTO customers (name, email, phone) 
               VALUES (%s, %s, %s) 
               ON CONFLICT (email) DO UPDATE 
               SET name = EXCLUDED.name, phone = EXCLUDED.phone 
               RETURNING id;""",
            (name, email, phone)
        )
        customer_id = cur.fetchone()[0]
        print(f"👤 Customer ID: {customer_id}")

        # 2. Check availability
        TOTAL_TABLES = 30
        cur.execute("SELECT COUNT(*) FROM reservations WHERE time_slot = %s;", (time_slot,))
        reservation_count = cur.fetchone()[0]
        print(f"📊 Reservations for {time_slot}: {reservation_count}/{TOTAL_TABLES}")

        if reservation_count >= TOTAL_TABLES:
            return jsonify({'error': 'Sorry, that time slot is fully booked!'}), 400

        # 3. Assign a random available table
        all_tables = list(range(1, TOTAL_TABLES + 1))
        cur.execute("SELECT table_number FROM reservations WHERE time_slot = %s;", (time_slot,))
        booked_tables = [row[0] for row in cur.fetchall()]
        available_tables = [t for t in all_tables if t not in booked_tables]

        if not available_tables:
            return jsonify({'error': 'Sorry, no tables available!'}), 400

        assigned_table = random.choice(available_tables)
        print(f"🎯 Assigned table: {assigned_table}")

        # 4. Create the reservation
        cur.execute(
            "INSERT INTO reservations (customer_id, time_slot, table_number, guests, special_requests) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (customer_id, time_slot, assigned_table, guests, special_requests)
        )
        
        reservation_id = cur.fetchone()[0]
        conn.commit()
        
        # 5. Format datetime for display
        try:
            datetime_obj = datetime.fromisoformat(time_slot.replace('Z', '+00:00'))
            formatted_datetime = datetime_obj.strftime("%A, %B %d, %Y at %I:%M %p")
        except:
            formatted_datetime = time_slot

        # 6. Prepare booking details for email
        booking_details = {
            'reservation_id': reservation_id,
            'customer_id': customer_id,
            'table_number': assigned_table,
            'guests': guests,
            'formatted_datetime': formatted_datetime,
            'special_requests': special_requests
        }

        # 7. Send confirmation email
        email_sent = send_booking_confirmation(name, email, booking_details)
        
        # 8. Prepare response message
        confirmation_message = f'🎉 Your reservation for {guests} guests on {formatted_datetime} is confirmed!\n\n'
        confirmation_message += f'📋 Reservation Details:\n'
        confirmation_message += f'• Table Number: #{assigned_table}\n'
        confirmation_message += f'• Reservation ID: #{reservation_id}\n'
        confirmation_message += f'• Customer ID: #{customer_id}\n\n'
        
        if special_requests:
            confirmation_message += f'📝 Special Requests: {special_requests}\n\n'
        
        if email_sent:
            confirmation_message += f'📧 A detailed confirmation has been sent to {email}\n\n'
        else:
            confirmation_message += f'⚠️ Reservation confirmed but email notification failed. Please save these details:\n\n'
        
        confirmation_message += f'📞 Questions? Call us at {CAFE_PHONE}'
        
        return jsonify({
            'success': True,
            'message': confirmation_message,
            'reservation_details': booking_details
        })

    except Exception as e:
        conn.rollback()
        print(f"❌ Database error: {e}")
        return jsonify({'error': 'A database error occurred.'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Newsletter signup endpoint
@app.route('/api/newsletter', methods=['POST'])
def newsletter_signup():
    data = request.get_json()
    print("📧 Newsletter signup:", data)

    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Simple email validation
    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Please enter a valid email address'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()

        # Check if email already exists
        cur.execute("SELECT id FROM customers WHERE email = %s;", (email,))
        existing_customer = cur.fetchone()

        if existing_customer:
            # Update existing customer to subscribe to newsletter
            cur.execute(
                "UPDATE customers SET newsletter = TRUE WHERE email = %s;",
                (email,)
            )
            message = "You're already in our system! We've updated your newsletter preference."
        else:
            # Create new customer with newsletter subscription
            cur.execute(
                "INSERT INTO customers (email, newsletter) VALUES (%s, TRUE);",
                (email,)
            )
            message = "Thank you for subscribing to our newsletter!"

        conn.commit()
        return jsonify({'success': True, 'message': message})

    except Exception as e:
        conn.rollback()
        print(f"❌ Newsletter error: {e}")
        return jsonify({'error': 'Subscription failed. Please try again.'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Admin credentials (in production, store these securely in environment variables)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("CafeFausse2025!".encode()).hexdigest()  # Change this password!
SECRET_KEY = "your-super-secret-jwt-key-here"  # Change this!

def generate_token(username):
    """Generate JWT token for admin authentication"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=8),  # Token expires in 8 hours
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to require authentication for admin endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authorization header required'}), 401
        
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
            username = verify_token(token)
            if not username:
                return jsonify({'error': 'Invalid or expired token'}), 401
        except (IndexError, ValueError):
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Hash the provided password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Check credentials
    if username == ADMIN_USERNAME and password_hash == ADMIN_PASSWORD_HASH:
        token = generate_token(username)
        return jsonify({
            'success': True,
            'token': token,
            'username': username,
            'message': 'Login successful'
        })
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Update admin endpoints to require authentication
@app.route('/api/admin/bookings', methods=['GET'])
@require_auth
def get_all_bookings():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT r.id, r.customer_id, r.time_slot, r.table_number, r.guests, r.special_requests, r.created_at,
                   c.name, c.email, c.phone 
            FROM reservations r 
            JOIN customers c ON r.customer_id = c.id 
            ORDER BY r.time_slot DESC
        ''')
        bookings = cur.fetchall()
        
        # Convert to list of dictionaries with proper datetime handling
        booking_list = []
        for booking in bookings:
            booking_dict = {
                'id': booking[0],
                'customer_id': booking[1],
                'time_slot': booking[2].isoformat() if hasattr(booking[2], 'isoformat') else str(booking[2]),
                'table_number': booking[3],
                'guests': booking[4],
                'special_requests': booking[5],
                'created_at': booking[6].isoformat() if hasattr(booking[6], 'isoformat') else str(booking[6]),
                'name': booking[7],
                'email': booking[8],
                'phone': booking[9]
            }
            booking_list.append(booking_dict)
        
        return jsonify({'bookings': booking_list})
        
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        return jsonify({'error': 'Failed to fetch bookings'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/api/admin/subscribers', methods=['GET'])
@require_auth
def get_all_subscribers():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()
        
        # First check if created_at column exists
        cur.execute('''
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='customers' and column_name='created_at'
        ''')
        
        has_created_at = cur.fetchone() is not None
        
        if has_created_at:
            cur.execute('''
                SELECT id, name, email, created_at 
                FROM customers 
                WHERE newsletter = TRUE 
                ORDER BY created_at DESC
            ''')
        else:
            cur.execute('''
                SELECT id, name, email, NULL as created_at 
                FROM customers 
                WHERE newsletter = TRUE 
                ORDER BY id DESC
            ''')
            
        subscribers = cur.fetchall()
        
        subscriber_list = []
        for sub in subscribers:
            subscriber_dict = {
                'id': sub[0],
                'name': sub[1] if sub[1] else 'Newsletter Subscriber',
                'email': sub[2],
                'created_at': sub[3].isoformat() if sub[3] and hasattr(sub[3], 'isoformat') else (str(sub[3]) if sub[3] else None)
            }
            subscriber_list.append(subscriber_dict)
        
        return jsonify({'subscribers': subscriber_list})
        
    except Exception as e:
        print(f"Error fetching subscribers: {e}")
        return jsonify({'error': 'Failed to fetch subscribers'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/api/admin/bookings/<int:booking_id>', methods=['DELETE'])
@require_auth
def cancel_booking(booking_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()
        
        # Check if booking exists
        cur.execute('SELECT id FROM reservations WHERE id = %s', (booking_id,))
        booking = cur.fetchone()
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Delete the booking
        cur.execute('DELETE FROM reservations WHERE id = %s', (booking_id,))
        conn.commit()
        
        return jsonify({'message': 'Booking cancelled successfully'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error cancelling booking: {e}")
        return jsonify({'error': 'Failed to cancel booking'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
if __name__ == '__main__':
    print("🌐 Server starting on http://127.0.0.1:5000")
    app.run(debug=True)