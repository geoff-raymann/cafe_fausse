from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import OperationalError
import os
import random

app = Flask(__name__)
CORS(app)

# Database connection details - UPDATE THESE FOR YOUR SYSTEM!
DB_HOST = "localhost"
DB_NAME = "cafe_fausse_db"
DB_USER = "postgres"  # Your PostgreSQL username
DB_PASS = "Pass123"  # Your PostgreSQL password

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
                name VARCHAR(100) NOT NULL,
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    print("📨 Received reservation data:", data)

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
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
            "INSERT INTO reservations (customer_id, time_slot, table_number, guests) VALUES (%s, %s, %s, %s);",
            (customer_id, time_slot, assigned_table, guests)
        )

        conn.commit()
        
        return jsonify({
            'success': True,
            'message': f'🎉 Your reservation for {guests} guests on {time_slot} is confirmed! Your table number is {assigned_table}.'
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
            
if __name__ == '__main__':
    print("🌐 Server starting on http://127.0.0.1:5000")
    app.run(debug=True)