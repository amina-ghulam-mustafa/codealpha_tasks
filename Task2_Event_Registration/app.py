from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client.event_registration  
events_collection = db.events
registrations_collection = db.registrations


if events_collection.count_documents({}) == 0:
    events_collection.insert_many([
        {"title": "Backend Bootcamp", "date": "2026-08-10", "location": "Online"},
        {"title": "AI & Data Science Workshop", "date": "2026-08-15", "location": "Lahore"}
    ])

@app.route('/events', methods=['GET'])
def get_events():
    """Sare events dekhne ke liye API"""
    events = []
    for event in events_collection.find():
        event['_id'] = str(event['_id'])  
        events.append(event)
    return jsonify(events), 200

@app.route('/register', methods=['POST'])
def register_event():
    """Event mein register karne ke liye API"""
    data = request.get_json()
    event_id = data.get('event_id')
    user_name = data.get('user_name')
    user_email = data.get('user_email')
    
    if not event_id or not user_name or not user_email:
        return jsonify({"error": "Missing required fields"}), 400
        
    registration = {
        "event_id": event_id,
        "user_name": user_name,
        "user_email": user_email
    }
    result = registrations_collection.insert_one(registration)
    
    return jsonify({"message": "Registration successful!", "registration_id": str(result.inserted_id)}), 201

@app.route('/registrations/<email>', methods=['GET'])
def get_registrations(email):
    """Ek user ki sari registrations dekhne ke liye API"""
    regs = []
    for reg in registrations_collection.find({"user_email": email}):
        reg['_id'] = str(reg['_id'])
        regs.append(reg)
    return jsonify(regs), 200

if __name__ == '__main__':
    
    app.run(debug=True, port=5001)
