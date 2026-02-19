"""
WSGI entry point for KitchenSync API.

This module serves as the entry point for running the application
in production (with gunicorn/uwsgi) or development mode.
"""

import os

from app import create_app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Run the development server
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)  # nosec
