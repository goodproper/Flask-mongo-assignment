from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import json
from pymongo import MongoClient, errors

app = Flask(__name__)

# Load API data from a backend file (data.json)
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# MongoDB connection: read URI from environment variable for safety
MONGO_URI = os.environ.get("MONGO_URI")  # set this before running
DB_NAME = os.environ.get("DB_NAME", "student_db")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "submissions")

def get_db_collection():
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI environment variable not set")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Test connection quickly
    client.server_info()
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

@app.route("/api")
def api_list():
    """Return JSON list read from data.json"""
    data = load_data()
    # ensure we return a list
    if isinstance(data, list):
        return jsonify(data)
    # if file contains a dict, return its values or list wrapped
    return jsonify([data])

@app.route("/", methods=["GET"])
def home():
    """Simple home page redirect to the form"""
    return redirect(url_for("show_form"))

@app.route("/form", methods=["GET"])
def show_form():
    return render_template("form.html", error=None)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    comment = request.form.get("comment", "").strip()

    # basic validation
    if not name or not email:
        return render_template("form.html", error="Name and email are required.")

    # prepare document to insert
    doc = {"name": name, "email": email, "comment": comment}

    try:
        coll = get_db_collection()
        coll.insert_one(doc)
        # on success redirect to a success page
        return redirect(url_for("success"))
    except errors.PyMongoError as e:
        # On error, render the same form and show the error (no redirect)
        return render_template("form.html", error=f"Database error: {e}")
    except RuntimeError as e:
        return render_template("form.html", error=str(e))

@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")

if __name__ == "__main__":
    # For local testing only. Use production server for deployment.
    app.run(debug=True, host="0.0.0.0", port=5000)
