from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv('MONGODB_URI')
if not uri:
    raise ValueError("MONGODB_URI is required")

client = MongoClient(uri)

def insert_conversation_line(role, content):
    try:
        database = client.get_database("EntropyBot")
        collection = database.get_collection("conversations")

        collection.insert_one({ "role": role, "content": content })

    except Exception as e:
        raise Exception("Unable to save this conversation line: ", e)