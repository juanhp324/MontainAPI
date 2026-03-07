import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("La variable de entorno MONGO_URI no está definida")

client = MongoClient(MONGO_URI)
db = client["MountainDB"]

users_col = db["users"]
bookings_col = db["bookings"]