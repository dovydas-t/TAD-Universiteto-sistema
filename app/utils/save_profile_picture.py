import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

def save_profile_picture(file, username):
    """Save uploaded profile picture and return filename"""
    # Get file extension
    filename = secure_filename(file.filename)
    file_ext = os.path.splitext(filename)[1].lower()
    
    # Create unique filename to avoid conflicts
    unique_filename = f"{username}_{uuid.uuid4().hex[:8]}{file_ext}"
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'static/uploads'), 'profiles')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)
    
    # Return relative path for storing in database
    return f"uploads/profiles/{unique_filename}"