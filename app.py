import time
import json
from datetime import datetime
from pymongo import MongoClient

VERSION = "1.0.1.0"

MONGO_URI = "mongodb+srv://tlsrudtj_db_user:o4wn3ARES791laWo@hr-test.o2lrhyi.mongodb.net/?appName=HR-Test"

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["r5_cafe"]
orders_collection = db["orders"]

print(f"[MongoDB] 연결 성공 VER{VERSION}")

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc = {
        "version": VERSION,
        "timestamp": now,
        "status": "running",
        "manager_id": "AZ.RM1"
    }
    result = orders_collection.insert_one(doc)
    print(f"[MongoDB] 저장 성공 | id: {result.inserted_id} | {now}")
    time.sleep(30)