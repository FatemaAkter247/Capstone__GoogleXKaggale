import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='127.0.0.1', port=5000)
