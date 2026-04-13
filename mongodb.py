from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv('MONGODB_URI')
if not uri:
  raise ValueError("MONGODB_URI is required")

client = MongoClient(uri)

try:
  database = client.get_database("")

except Exception as e:
  raise Exception("Unable to find the document. ", e)