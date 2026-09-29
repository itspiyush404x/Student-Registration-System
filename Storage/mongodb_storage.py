import pymongo
from secrets_config import MONGO_URI

# 1. Connect to local MongoDB instance
client = pymongo.MongoClient(MONGO_URI)
db = client["student_db"]
collection = db["students"]

def init_db():
    """Verify that MongoDB is running and we can connect to it."""
    client.admin.command("ping")

def register_student(student_data):
    """
    Save student dictionary to MongoDB.
    Returns the string ID of the inserted document.
    """
    # Clean up optional fields so they are not missing
    if "qualification" not in student_data:
        student_data["qualification"] = ""
    if "passing_year" not in student_data:
        student_data["passing_year"] = 0
    if "college" not in student_data:
        student_data["college"] = ""
    if "company" not in student_data:
        student_data["company"] = ""
    if "experience" not in student_data:
        student_data["experience"] = 0.0

    # Insert into the database collection
    result = collection.insert_one(student_data)
    
    # Return string representation of MongoDB's unique ID
    return str(result.inserted_id)











