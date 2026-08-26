import sys
import os

# Insert the project root directory at the very beginning of sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import the Flask instance from app.py (change to 'main' if your file is main.py)
from main import app