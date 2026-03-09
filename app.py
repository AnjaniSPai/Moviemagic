# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# import uuid
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from pymongo import MongoClient

# app = Flask(__name__)
# app.secret_key = 'moviemagic_secret_key_2024'

# # MongoDB Configuration
# try:
#     client = MongoClient('localhost', 27017)
#     db = client['moviemagic']
#     users_collection = db['users']
#     bookings_collection = db['bookings']
#     print("✅ MongoDB connected successfully!")
# except Exception as e:
#     print(f"❌ MongoDB connection error: {e}")
#     client = None
#     db = None

# # ============================================
# # EMAIL CONFIGURATION - UPDATE THESE VALUES
# # ============================================
# # To enable email tickets, replace the values below:
# # 1. SMTP_EMAIL: Your Gmail address (e.g., yourname@gmail.com)
# # 2. SMTP_PASSWORD: Gmail App Password (16 characters)
# #    Get it from: Google Account → Security → App Passwords

# SMTP_EMAIL = ''  # Leave empty to disable email
# SMTP_PASSWORD = ''  # Leave empty to disable email
# SMTP_SERVER = 'smtp.gmail.com'
# SMTP_PORT = 587

# def send_ticket_email(user_email, booking_data):
#     """Send ticket confirmation email"""
#     if not SMTP_EMAIL or not SMTP_PASSWORD:
#         print("⚠️ Email not configured - skipping email send")
#         return False
    
#     try:
#         # Create message
#         msg = MIMEMultipart('alternative')
#         msg['Subject'] = f'🎬 MovieMagic - Your Ticket: {booking_data["movie_name"]}'
#         msg['From'] = f'MovieMagic <{SMTP_EMAIL}>'
#         msg['To'] = user_email
        
#         # HTML Email Template
#         html_content = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <style>
#                 body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f0f1a; color: #ffffff; padding: 20px; }}
#                 .container {{ max-width: 600px; margin: 0 auto; background: linear-gradient(145deg, #1a1a2e, #16213e); border-radius: 20px; overflow: hidden; border: 2px solid #6366f1; }}
#                 .header {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); padding: 30px; text-align: center; }}
#                 .header h1 {{ color: white; margin: 0; font-size: 28px; }}
#                 .body {{ padding: 30px; }}
#                 .movie-title {{ color: #6366f1; font-size: 24px; text-align: center; margin-bottom: 25px; font-weight: bold; }}
#                 .details {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 25px; }}
#                 .detail-box {{ background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; text-align: center; }}
#                 .detail-label {{ color: #888; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }}
#                 .detail-value {{ color: white; font-size: 16px; font-weight: bold; }}
#                 .price-box {{ background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(6,182,212,0.1)); padding: 20px; border-radius: 10px; text-align: center; border: 1px solid rgba(6,182,212,0.3); margin-bottom: 25px; }}
#                 .price-label {{ color: #888; font-size: 14px; }}
#                 .price-value {{ color: #06b6d4; font-size: 32px; font-weight: bold; }}
#                 .footer {{ background: rgba(0,0,0,0.3); padding: 20px; text-align: center; color: #666; font-size: 12px; }}
#                 .ticket-id {{ background: rgba(99,102,241,0.2); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <div class="header">
#                     <h1>🎬 MovieMagic</h1>
#                 </div>
#                 <div class="body">
#                     <div class="movie-title">🎬 {booking_data['movie_name']}</div>
                    
#                     <div class="ticket-id">
#                         <div class="detail-label">Booking ID</div>
#                         <div class="detail-value" style="color: #6366f1;">#{booking_data['booking_id']}</div>
#                     </div>
                    
#                     <div class="details">
#                         <div class="detail-box">
#                             <div class="detail-label">📅 Date</div>
#                             <div class="detail-value">{booking_data['date']}</div>
#                         </div>
#                         <div class="detail-box">
#                             <div class="detail-label">⏰ Time</div>
#                             <div class="detail-value">{booking_data['time']}</div>
#                         </div>
#                         <div class="detail-box">
#                             <div class="detail-label">🏠 Theater</div>
#                             <div class="detail-value">{booking_data['theater']}</div>
#                         </div>
#                         <div class="detail-box">
#                             <div class="detail-label">💺 Seats</div>
#                             <div class="detail-value">{booking_data['seats']}</div>
#                         </div>
#                     </div>
                    
#                     <div class="price-box">
#                         <div class="price-label">Total Amount Paid</div>
#                         <div class="price-value">₹{booking_data['amount_paid']}</div>
#                     </div>
#                 </div>
#                 <div class="footer">
#                     <p>Thank you for choosing MovieMagic! 🎬</p>
#                     <p>Please show this email at the theater entrance.</p>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
        
#         # Plain text version
#         text_content = f"""
#         🎬 MovieMagic - Booking Confirmation
        
#         Movie: {booking_data['movie_name']}
#         Booking ID: {booking_data['booking_id']}
#         Date: {booking_data['date']}
#         Time: {booking_data['time']}
#         Theater: {booking_data['theater']}
#         Seats: {booking_data['seats']}
#         Amount Paid: ₹{booking_data['amount_paid']}
        
#         Thank you for choosing MovieMagic!
#         """
        
#         # Attach both versions
#         part1 = MIMEText(text_content, 'plain')
#         part2 = MIMEText(html_content, 'html')
        
#         msg.attach(part1)
#         msg.attach(part2)
        
#         # Send email
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_EMAIL, SMTP_PASSWORD)
#         server.sendmail(SMTP_EMAIL, user_email, msg.as_string())
#         server.quit()
        
#         print(f"✅ Ticket email sent to {user_email}")
#         return True
        
#     except Exception as e:
#         print(f"❌ Email sending failed: {str(e)}")
#         return False

# # --- Authentication Routes ---

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'])
        
#         # Check if user already exists in MongoDB
#         existing_user = users_collection.find_one({'email': email})
        
#         if existing_user:
#             flash('Email already registered!', 'danger')
#             return redirect(url_for('signup'))
        
#         # Create new user in MongoDB
#         user_data = {
#             '_id': str(uuid.uuid4()),
#             'name': name,
#             'email': email,
#             'password': password,
#             'created_at': datetime.now()
#         }
        
#         users_collection.insert_one(user_data)
        
#         flash('Registration successful! Please login.', 'success')
#         return redirect(url_for('login'))
            
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         # Find user in MongoDB
#         user = users_collection.find_one({'email': email})
        
#         if user and check_password_hash(user['password'], password):
#             session['user'] = {
#                 'id': user['_id'],
#                 'name': user['name'],
#                 'email': user['email']
#             }
#             return redirect(url_for('home1'))
        
#         flash('Invalid email or password', 'danger')
            
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     flash('You have been logged out!', 'info')
#     return redirect(url_for('index'))

# # --- Application Routes ---

# @app.route('/home1')
# def home1():
#     if 'user' not in session:
#         return redirect(url_for('login'))
#     return render_template('home1.html')

# @app.route('/profile')
# def profile():
#     if 'user' not in session:
#         return redirect(url_for('login'))
    
#     # Get user info from MongoDB
#     user = users_collection.find_one({'_id': session['user']['id']})
    
#     # Get user's booking history
#     user_bookings = list(bookings_collection.find({'booked_by': session['user']['email']}))
    
#     return render_template('profile.html', user=user, bookings=user_bookings)

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/contact_us')
# def contact():
#     return render_template('contact_us.html')

# @app.route('/b1', methods=['GET'], endpoint='b1')
# def booking_page():
#     if 'user' not in session:
#         return redirect(url_for('login'))

#     return render_template('b1.html',
#         movie=request.args.get('movie'),
#         theater=request.args.get('theater'),
#         address=request.args.get('address'),
#         price=request.args.get('price')
#     )

# @app.route('/tickets', methods=['POST'])
# def tickets():
#     if 'user' not in session:
#         return redirect(url_for('login'))
        
#     try:
#         # Extract booking details from form
#         booking_id = f"MVM-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
#         # Get user email from session
#         user_email = session['user']['email']
        
#         # Insert booking into MongoDB
#         booking_data = {
#             'booking_id': booking_id,
#             'movie_name': request.form.get('movie'),
#             'date': request.form.get('date'),
#             'time': request.form.get('time'),
#             'theater': request.form.get('theater'),
#             'address': request.form.get('address'),
#             'booked_by': user_email,
#             'user_name': session['user']['name'],
#             'seats': request.form.get('seats'),
#             'amount_paid': request.form.get('amount'),
#             'booking_time': datetime.now()
#         }
        
#         bookings_collection.insert_one(booking_data)
        
#         # Try to send email
#         email_sent = send_ticket_email(user_email, booking_data)
        
#         if email_sent:
#             flash('Booking successful! Ticket sent to your email!', 'success')
#         else:
#             flash('Booking successful!', 'success')
        
#         # Prepare booking data for display
#         booking = {
#             'booking_id': booking_id,
#             'movie_name': request.form.get('movie'),
#             'date': request.form.get('date'),
#             'time': request.form.get('time'),
#             'theater': request.form.get('theater'),
#             'address': request.form.get('address'),
#             'seats': request.form.get('seats'),
#             'amount_paid': request.form.get('amount'),
#             'user_name': session['user']['name'],
#             'user_email': user_email
#         }
        
#         return render_template('tickets.html', booking=booking)
        
#     except Exception as e:
#         print(f"Error processing booking: {str(e)}")
#         flash('Error processing booking', 'danger')
#         return redirect(url_for('home1'))

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)

from xml.dom.minidom import Attr

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import os
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = 'moviemagic_secret_key_2024'

from decimal import Decimal

def replace_decimals(obj):
    if isinstance(obj, list):
        return [replace_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: replace_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

# ============================================
# AWS CONFIGURATION - MATCH YOUR CONSOLE
# ============================================
# Ensure you attach an IAM Role to your EC2 with DynamoDB & SNS access [cite: 846, 847]
AWS_REGION = "us-east-1"  # Update to your region [cite: 172]
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:203918855127:MovieMagic"

#"arn:aws:sns:us-east-1:651200362301:MovieTicketNotifications:e452f8d2-01ff-40d7-93b4-e8c3602f2fd7" # Paste your ARN here [cite: 174]
#   arn:aws:sns:us-east-1:203918855127:MovieMagic
# Initialize AWS resources [cite: 201, 202]
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
users_table = dynamodb.Table('MovieMagic_Users') # Partition Key: 'email' [cite: 500]
bookings_table = dynamodb.Table('MovieMagic_Bookings') # Partition Key: 'booking_id' [cite: 564]
sns_client = boto3.client('sns', region_name=AWS_REGION)

def send_booking_confirmation(booking_data):
    """Send ticket confirmation using AWS SNS [cite: 213]"""
    try:
        message = f"""
        🎬 MovieMagic Booking Confirmation!
        
        Booking ID: {booking_data['booking_id']}
        Movie: {booking_data['movie_name']}
        Theater: {booking_data['theater']}
        Seats: {booking_data['seats']}
        Amount Paid: ₹{booking_data['amount_paid']}
        
        Please show this notification at the entrance.
        """
        
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"MovieMagic - Your Ticket: {booking_data['movie_name']}",
            Message=message,
            MessageAttributes={
                'email': {'DataType': 'String', 'StringValue': booking_data['booked_by']}
            }
        )
        print(f"✅ SNS notification sent to {booking_data['booked_by']}")
        return True
    except Exception as e:
        print(f"❌ SNS failed: {str(e)}")
        return False

# --- Authentication Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        try:
            # Check if user exists in DynamoDB [cite: 264]
            response = users_table.get_item(Key={'email': email})
            if 'Item' in response:
                flash('Email already registered!', 'danger')
                return redirect(url_for('signup'))
            
            # Save new user to DynamoDB [cite: 268]
            user_data = {
                'id': str(uuid.uuid4()),
                'name': name,
                'email': email,
                'password': password,
                'created_at': datetime.now().isoformat()
            }
            users_table.put_item(Item=user_data)
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except ClientError as e:
            print(f"Error: {e}")
            flash('Database error during signup', 'danger')
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Fetch user from DynamoDB [cite: 307]
            response = users_table.get_item(Key={'email': email})
            if 'Item' in response:
                user = response['Item']
                if check_password_hash(user['password'], password):
                    session['user'] = {
                        'id': user['id'],
                        'name': user['name'],
                        'email': user['email']
                    }
                    return redirect(url_for('home1'))
            
            flash('Invalid email or password', 'danger')
        except ClientError as e:
            print(f"Error: {e}")
            flash('Database connection error', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))

# --- Application Routes ---

@app.route('/home1')
def home1():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home1.html')

# @app.route('/profile')
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    try:
        email = session['user']['email']
        response = users_table.get_item(Key={'email': email})
        user = response.get('Item')
        
        if user:
            # Pass the user data directly. 
            # If you had date formatting here, remove it to stop the 'strftime' error.
            booking_response = bookings_table.scan(
                FilterExpression=Attr('booked_by').eq(email))
            # FilterExpression=Attr('email').eq(email))
            user_bookings = replace_decimals(booking_response.get('Items', []))
            return render_template('profile.html', user=user, bookings=user_bookings)
        else:
            session.clear()
            return redirect(url_for('login'))
    
            
    except Exception as e:
        print(f"Profile Error: {e}") # This is where the 'strftime' error was caught
        return redirect(url_for('home1'))
# def profile():
#     if 'user' not in session:
#         return redirect(url_for('login'))
    
#     try:
#         # Note: In DynamoDB, fetching all user bookings typically requires a Scan or GSI [cite: 511]
#         # For simplicity in testing, we fetch current session user info
#         response = users_table.get_item(Key={'email': session['user']['email']})
#         user = response.get('Item')
#         return render_template('profile.html', user=user, bookings=[]) 
#     except:
#         return render_template('profile.html', user=None, bookings=[])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')

@app.route('/b1', methods=['GET'])
def booking_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('b1.html',
        movie=request.args.get('movie'),
        theater=request.args.get('theater'),
        address=request.args.get('address'),
        price=request.args.get('price')
    )

@app.route('/tickets', methods=['POST'])
def tickets():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    try:
        booking_id = f"MVM-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        user_email = session['user']['email']
        
        booking_data = {
            'booking_id': booking_id,
            'movie_name': request.form.get('movie'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'theater': request.form.get('theater'),
            'address': request.form.get('address'),
            'booked_by': user_email,
            'user_name': session['user']['name'],
            'seats': request.form.get('seats'),
            'amount_paid': str(request.form.get('amount')),  # DynamoDB expects strings for numbers
            'booking_time': datetime.now().isoformat()
        }
        
        # Save to DynamoDB [cite: 389]
        bookings_table.put_item(Item=booking_data)
        
        # Send Cloud Notification [cite: 391]
        send_booking_confirmation(booking_data)
        
        flash('Booking successful! Confirmation sent via AWS SNS.', 'success')
        return render_template('tickets.html', booking=booking_data)
        
    except Exception as e:
        print(f"Error processing booking: {str(e)}")
        flash('Error processing booking', 'danger')
        return redirect(url_for('home1'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
