from appwrite.client import Client
from appwrite.services.databases import Databases
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env into environment

client = Client()
client.set_endpoint(os.getenv("APPWRITE_ENDPOINT"))
client.set_project(os.getenv("APPWRITE_PROJECT_ID"))
client.set_key(os.getenv("APPWRITE_API_KEY"))

database = Databases(client)
