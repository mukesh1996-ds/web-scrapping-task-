import os

from dotenv import load_dotenv
load_dotenv()

# Complete these 2 fields

USERNAME = os.environ.get('INSTA_USER')
PASSWORD = os.environ.get('INSTA_PASS')

print(USERNAME)
print(PASSWORD)