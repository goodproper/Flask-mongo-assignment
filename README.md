# Flask + MongoDB Atlas Example

This small app shows:
1. `/api` route: reads `data.json` and returns a JSON list.
2. A simple frontend form that inserts form data into MongoDB Atlas. On success user is redirected to a success page; on error the form redisplays with the error.

## Setup

1. Install Python 3 and pip.
2. Create a Python virtual environment (recommended):
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\\Scripts\\activate    # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Create a MongoDB Atlas database and get the connection string:
   - Go to https://www.mongodb.com/cloud/atlas and create a free cluster.
   - Create a database user and allow your IP in Network Access (or use 0.0.0.0/0 for testing).
   - Get the connection string URI (it looks like mongodb+srv://USER:PASS@cluster0...).

5. Set environment variables (replace with your values):
   On Linux/macOS:
     export MONGO_URI="mongodb+srv://USER:PASSWORD@cluster0.example.mongodb.net/?retryWrites=true&w=majority"
     export DB_NAME="student_db"
     export COLLECTION_NAME="submissions"

   On Windows (PowerShell):
     $env:MONGO_URI="mongodb+srv://USER:PASSWORD@cluster0.example.mongodb.net/?retryWrites=true&w=majority"
     $env:DB_NAME="student_db"
     $env:COLLECTION_NAME="submissions"

6. Run the app:
   python app.py

7. Open in browser:
   - Form: http://localhost:5000/form
   - API JSON: http://localhost:5000/api
