import os
import time
import streamlit as st

def initialize_directories():
    """Create upload directories if they don't exist."""
    os.makedirs("uploads/front", exist_ok=True)
    os.makedirs("uploads/back", exist_ok=True)

def save_uploaded_file(uploaded_file, category, student_phone):
    """
    Save the uploaded file on disk and return its relative file path.
    """
    if uploaded_file is None:
        return ""

    # 1. Clean category string
    if "front" in category.lower():
        folder = "uploads/front"
        cat_name = "front"
    else:
        folder = "uploads/back"
        cat_name = "back"

    # Make sure target folder exists
    initialize_directories()

    # 2. Get file extension (like .png or .jpg)
    _, ext = os.path.splitext(uploaded_file.name)
    
    # 3. Create unique filename using student phone and timestamp
    timestamp = int(time.time())
    filename = f"{student_phone}_{timestamp}{ext}"
    
    # 4. Save path
    save_path = os.path.join(folder, filename)

    # 5. Write the file bytes to disk
    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Return path formatted with forward slashes
        return f"uploads/{cat_name}/{filename}"
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return ""