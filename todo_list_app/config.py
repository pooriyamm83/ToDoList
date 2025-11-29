from dotenv import load_dotenv
import os

load_dotenv()

MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 10))
MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK", 50))