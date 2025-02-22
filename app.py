from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import requests
import os

app = Flask(__name__)
CORS(app)

# Load your API key from api_key.txt
with open('api_key.txt', 'r') as file:
    API_KEY = file.read().strip()

# Function to ask Gemini a question
def query_gemini(prompt):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'
    headers = {'Content-Type': 'application/json'}
    data = {
        'contents': [{'parts': [{'text': prompt}]}]
    }
    print(f"Sending request to Gemini with prompt: {prompt}")
    response = requests.post(url, json=data, headers=headers)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Sorry, I couldn’t get an answer right now. Status: {response.status_code}"

# Welcome page
@app.route('/')
def home():
    return "Welcome to Tutor App!"

# Chat route for questions
@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    response = query_gemini(message)
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chats (message, response) VALUES (?, ?)', (message, response))
    # Add 1 point for each question
    cursor.execute('INSERT INTO progress (points) VALUES (1) ON CONFLICT(id) DO UPDATE SET points = points + 1')
    # Get total points
    cursor.execute('SELECT SUM(points) FROM progress')
    total_points = cursor.fetchone()[0] or 0
    # Decide badge based on points
    badge = "Beginner" if total_points < 5 else "Star" if total_points < 10 else "Master"
    conn.commit()
    conn.close()
    return jsonify({'response': response, 'points': total_points, 'badge': badge})

# Image upload route (placeholder for now)
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('uploaded_image.jpg')
    prompt = "Solve this problem from the image."
    response = query_gemini(prompt)
    os.remove('uploaded_image.jpg')
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chats (message, response) VALUES (?, ?)', ('Image uploaded', response))
    # Add 1 point for each upload
    cursor.execute('INSERT INTO progress (points) VALUES (1) ON CONFLICT(id) DO UPDATE SET points = points + 1')
    cursor.execute('SELECT SUM(points) FROM progress')
    total_points = cursor.fetchone()[0] or 0
    badge = "Beginner" if total_points < 5 else "Star" if total_points < 10 else "Master"
    conn.commit()
    conn.close()
    return jsonify({'response': response, 'points': total_points, 'badge': badge})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)