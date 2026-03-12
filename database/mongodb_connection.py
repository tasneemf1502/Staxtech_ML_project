from pymongo import MongoClient

# MongoDB Atlas Cloud Connection
client = MongoClient("mongodb+srv://tasneemfathima1502_db_user:<db_password>@tasneem.63kvud8.mongodb.net/?appName=Tasneem")

# Database
db = client["internship_ml_system"]

# Collection
students_collection = db["students"]