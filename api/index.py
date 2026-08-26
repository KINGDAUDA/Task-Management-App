# api/index.py
import sys
import os

# Ensure the root directory is on the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Vercel needs the WSGI variable 'app'
app = app