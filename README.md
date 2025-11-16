# 🧠 EmotionIQ – AI Emotion Detection System

EmotionIQ is an advanced AI-powered emotion recognition system that analyzes facial expressions using deep learning models and delivers personalized recommendations in real time.  
Built with **Flask, Python, FER, OpenCV, TailwindCSS, and MongoDB Atlas**, EmotionIQ brings scientific-grade affective computing to everyday users, researchers, and organizations.

## ✔ Project Overview
EmotionIQ captures or receives an uploaded image, detects the user’s emotional state using a deep learning model, and generates smart recommendations tailored to that emotion.  
It includes user authentication, cloud storage, and a modern, responsive UI.

## ✔ Features
- 🎭 Real-Time Emotion Detection using deep learning  
- 📸 Upload or capture image for instant analysis  
- 🤖 AI-powered recommendations based on detected mood  
- 🔐 User authentication (Register/Login)  
- ☁️ MongoDB Atlas cloud database  
- 🎨 Fully responsive UI created with TailwindCSS  
- 🧰 Clean, modular structure  
- 🔍 High accuracy and fast inference  

## ✔ Tech Stack
### Frontend
- HTML5  
- TailwindCSS  
- Vanilla JavaScript  

### Backend
- Python  
- Flask  
- OpenCV  
- FER (Facial Emotion Recognition Model)  

### Database
- MongoDB Atlas  
- Flask-PyMongo  

## ✔ Directory Structure
```
EmotionIQ/
│── app.py
│── emotion_detector.py
│── recommender.py
│── requirements.txt
│
├── templates/
│     ├── landing.html
│     ├── login.html
│     ├── register.html
│     └── index.html
│
├── static/
│     ├── uploads/
│     ├── emotion.jpg
│     └── about.jpg
│
└── venv/
```

## ✔ Installation Guide
### 1️⃣ Clone the repository
```
git clone https://github.com/bkit-solutions/Emotion_IQ.git
cd EmotionIQ
```

### 2️⃣ Create & activate virtual environment
**Windows**
```
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**
```
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install required packages
```
pip install -r requirements.txt
```

## ✔ Setup Instructions
### Configure MongoDB Atlas
Inside `app.py`, replace:
```
app.config['MONGO_URI'] = "your-mongodb-url"
```

### Ensure FER works
```
pip install fer==22.4.0
```


MONGO_URI="your_mongodb_url"
SECRET_KEY="your_secret_key"
PORT=8080
```

## ✔ How to Run
```
python app.py
```

Visit:
http://127.0.0.1:8080

## ✔ Future Enhancements
- 🎥 Real-time webcam streaming  
- 🔊 Voice-based sentiment analysis  
- 📊 Analytics dashboard  
- 🧬 Custom CNN model  
- 🌍 Multi-language support  
- 📱 Mobile app version  

## ✔ License
Licensed under the MIT License.
