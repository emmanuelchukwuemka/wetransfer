#!/usr/bin/env python3
"""
WSGI entry point for Render deployment
This file exists because Render auto-detects and tries to import 'app:app'
"""

# Import the Flask app from index.py
from index import app

# This makes the app available as 'app' for gunicorn
if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)