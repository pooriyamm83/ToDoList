# todo_list_app/config.py
from dotenv import load_dotenv
import os

load_dotenv()
# from phase 1
MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 10))
MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK", 50))

# phase2: database
DB_USER = os.getenv("DB_USER", "todolist_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "todolist_db")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"