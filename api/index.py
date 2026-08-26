# api/index.py
from app import app

# Vercel's Python runtime requires the WSGI callable named 'app'
app = app