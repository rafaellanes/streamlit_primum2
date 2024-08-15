import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')

print(DB_USER)


