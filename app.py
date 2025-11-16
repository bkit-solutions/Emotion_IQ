from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_pymongo import PyMongo
import cv2
import os
import time
from emotion_detector import detect_emotion
from recommender import get_recommendations
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# ================================
# MongoDB Configuration (UPDATED TO emotdb)
# ================================
app.config['MONGO_URI'] = (
    "mongodb+srv://dharmarajucaleb4_db_user:8EwSyeRs3vApljGg"
    "@cluster0.oqnc6uj.mongodb.net/emotdb?"
    "retryWrites=true&w=majority&appName=Cluster0"
)
mongo = PyMongo(app)

# Authentication collection
auth_collection = mongo.db.auth  

# ================================
# File Upload Folder
# ================================
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================================
# Helper Function to Resize Image
# ================================
def resize_image(image_path):
    try:
        img = cv2.imread(image_path)
        img = cv2.resize(img, (300, 300))  # Reduce size
        cv2.imwrite(image_path, img)
    except Exception as e:
        print(f"Error resizing image: {e}")

# ================================
# Routes
# ================================
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def index():
    # Clear old image if stored in session
    if 'image_path' in session:
        try:
            os.remove(session['image_path'])
            print(f"Deleted old image: {session['image_path']}")
        except Exception as e:
            print(f"Error deleting old image: {e}")
        session.pop('image_path', None)
    return render_template('index.html')

# ================================
# USER REGISTRATION
# ================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        existing_user = auth_collection.find_one({'email': email})
        if existing_user:
            flash('Email already exists. Please log in.', 'warning')
            return redirect(url_for('login'))
        
        hashed_password = generate_password_hash(password)
        auth_collection.insert_one({
            'email': email,
            'username': username,
            'password': hashed_password
        })

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# ================================
# USER LOGIN
# ================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = auth_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

# ================================
# USER LOGOUT
# ================================
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# ================================
# EMOTION DETECTION
# ================================
@app.route('/detect_emotion', methods=['POST'])
def detect():
    print("Request received at /detect_emotion")
    print("Request headers:", request.headers)
    print("Request files:", request.files)

    if 'image' not in request.files or request.files['image'].filename == '':
        print("No image found in request")
        return jsonify({'error': 'No image uploaded'}), 400

    # Save uploaded image
    image = request.files['image']
    timestamp = int(time.time())
    image_path = os.path.join(UPLOAD_FOLDER, f'captured_{timestamp}.jpg')

    image.save(image_path)
    resize_image(image_path)
    session['image_path'] = image_path  

    # Detect emotion
    emotion = detect_emotion(image_path)
    if not emotion:
        os.remove(image_path)
        session.pop('image_path', None)
        return jsonify({'error': 'No face detected or emotion recognition failed'}), 400

    # Get recommendations
    recommendations = get_recommendations(emotion)
    response = jsonify({
        'emotion': emotion,
        'recommendations': recommendations,
        'image_url': image_path
    })

    # Remove image after use
    try:
        os.remove(image_path)
        session.pop('image_path', None)
    except Exception as e:
        print(f"Error deleting processed image: {e}")

    return response

# ================================
# RUN SERVER
# ================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
