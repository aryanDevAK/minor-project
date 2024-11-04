from datetime import datetime, date
from flask_jwt_extended import jwt_required, get_jwt_identity
import tempfile
import pytesseract
import cv2
from PIL import Image
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Setup Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'.\tesseract-ocr-w64-setup-5.4.0.20240606.exe'

# Initialize the Gemini API
api_key = os.getenv("GENAI_API_KEY")
genai.configure(api_key=api_key)

def prescription_processing(image):
    _, buffer = cv2.imencode('.jpeg', image)
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_file.write(buffer)
        temp_file_path = temp_file.name

    try:
        myfile = genai.upload_file(temp_file_path)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = ("what is written there?")
        response = model.generate_content([myfile, "\n\n", prompt])
        return response.text if response.text else {"error": "No response from Gemini."}
    except Exception as e:
        return {"error": str(e)}

def str_to_date(birth_date):
    try:
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        return birth_date
    except ValueError:
        return jsonify({"error": "Invalid birth_date format. Use YYYY-MM-DD."}), 400

def has_required_role(required_roles):
    identity = get_jwt_identity()  
    if isinstance(identity, dict):
        user_id = identity.get("id")
        user_role = identity.get("role")

        if user_id is None or user_role is None:
            return False

        return user_role in required_roles
    
    return False
