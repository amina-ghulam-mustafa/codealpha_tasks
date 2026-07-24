from flask import Flask, request, redirect, jsonify
from pymongo import MongoClient
import string
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client.url_shortener
urls_collection = db.urls

def generate_short_code():
    """Generates a 6-character random string."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('original_url')
    
    if not original_url:
        return jsonify({"error": "URL is required"}), 400
        
    short_code = generate_short_code()
    
    # Save to MongoDB
    urls_collection.insert_one({
        "original_url": original_url,
        "short_code": short_code
    })
    
    return jsonify({
        "original_url": original_url,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    url_data = urls_collection.find_one({"short_code": short_code})
    
    if url_data:
        return redirect(url_data['original_url'])
    else:
        return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
