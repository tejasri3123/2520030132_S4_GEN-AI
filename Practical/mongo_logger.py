
# mongo_logger.py

from pymongo import MongoClient
from datetime import datetime, timezone


class MongoLogger:

    def __init__(self):

        self.client = MongoClient(
            "mongodb://localhost:27017/",
            serverSelectionTimeoutMS=5000
        )

        # Verify MongoDB connection
        self.client.admin.command("ping")

        self.db = self.client["llm_monitoring"]

        self.collection = self.db["call_logs"]

        print("MongoDB connected successfully!")

    def log_call(self, log_data):

        # Add timestamp to each record
        log_data["timestamp"] = datetime.now(timezone.utc)

        # Store the record in MongoDB
        self.collection.insert_one(log_data)

        print("Call details saved in MongoDB!")

    def close(self):

        self.client.close()

        print("MongoDB connection closed.")
