from flask import (Flask,render_template,request,redirect,url_for,session,send_file)
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from database.mongodb import users_collection, files_collection
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

FILE_ENCRYPTION_KEY = os.getenv("FILE_ENCRYPTION_KEY")

fernet = Fernet(FILE_ENCRYPTION_KEY)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = os.getenv("SECRET_KEY")


# =========================
# Home
# =========================

@app.route("/")
def home():

    if "user_id" in session:
        return "Welcome to PrivateVault!"

    return redirect(url_for("login"))


# =========================
# Register
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = users_collection.find_one({
            "email": email
        })

        if existing_user:
            return "Email already registered!"

        # Hash password
        hashed_password = generate_password_hash(password)

        # Save user
        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# Login
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = users_collection.find_one({
            "email": email
        })

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]
            session["email"] = user["email"]

            return redirect(url_for("dashboard"))

        return "Invalid email or password!"

    return render_template("login.html")


# =========================
# Dashboard
# =========================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_files = list(files_collection.find({
        "user_id": session["user_id"]
    }).sort("uploaded_at", -1))

    # Total files
    total_files = len(user_files)

    # Storage
    total_storage = 0

    # File type counters
    images = 0
    videos = 0
    pdfs = 0
    documents = 0
    other_files = 0

    for file in user_files:

        file_path = file.get("file_path")

        if file_path and os.path.exists(file_path):
            total_storage += os.path.getsize(file_path)

        filename = file.get("filename", "").lower()

        if filename.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            images += 1

        elif filename.endswith((".mp4", ".avi", ".mkv", ".mov", ".webm")):
            videos += 1

        elif filename.endswith(".pdf"):
            pdfs += 1

        elif filename.endswith((".doc", ".docx", ".txt")):
            documents += 1

        else:
            other_files += 1

    storage_mb = round(
        total_storage / (1024 * 1024),
        2
    )

    recent_files = user_files[:5]

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        total_files=total_files,
        storage_mb=storage_mb,
        recent_files=recent_files,
        images=images,
        videos=videos,
        pdfs=pdfs,
        documents=documents,
        other_files=other_files
    )

# =========================
# UPLOAD ROUTE 
# =========================

@app.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if "file" not in request.files:
        return "No file selected!"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected!"

    filename = secure_filename(file.filename)

    # Read original file
    file_data = file.read()

    # Encrypt file
    encrypted_data = fernet.encrypt(file_data)

    # Create encrypted filename
    encrypted_filename = filename + ".enc"

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        encrypted_filename
    )

    # Save encrypted file
    with open(file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    # Save metadata
    files_collection.insert_one({
        "user_id": session["user_id"],
        "user_email": session["email"],
        "filename": filename,
        "encrypted_filename": encrypted_filename,
        "file_path": file_path,
        "uploaded_at": datetime.now()
    })

    return "File encrypted and uploaded successfully!"


# =========================
# MY FILES
# =========================

@app.route("/my-files")
def my_files():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()

    query = {
        "user_id": session["user_id"]
    }

    if search:
        query["filename"] = {
            "$regex": search,
            "$options": "i"
        }

    user_files = files_collection.find(query).sort(
        "uploaded_at",
        -1
    )

    return render_template(
        "my_files.html",
        files=user_files,
        search=search
    )

# =========================
# DOWNLOAD FILE
# =========================

@app.route("/download/<file_id>")
def download_file(file_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    from bson import ObjectId

    file_info = files_collection.find_one({
        "_id": ObjectId(file_id),
        "user_id": session["user_id"]
    })

    if not file_info:
        return "File not found!"

    encrypted_path = file_info["file_path"]

    if not os.path.exists(encrypted_path):
        return "Encrypted file not found!"

    # Read encrypted file
    with open(encrypted_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Decrypt file
    decrypted_data = fernet.decrypt(encrypted_data)

    # Temporary decrypted file
    temp_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "temp_" + file_info["filename"]
    )

    with open(temp_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

    from flask import send_file

    return send_file(
        temp_path,
        as_attachment=True,
        download_name=file_info["filename"]
    )



# =========================
# DELETE FILE
# =========================

@app.route("/delete/<file_id>")
def delete_file(file_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    from bson import ObjectId

    file_info = files_collection.find_one({
        "_id": ObjectId(file_id),
        "user_id": session["user_id"]
    })

    if not file_info:
        return "File not found!"

    # Delete encrypted file from uploads folder
    encrypted_path = file_info["file_path"]

    if os.path.exists(encrypted_path):
        os.remove(encrypted_path)

    # Delete file metadata from MongoDB
    files_collection.delete_one({
        "_id": ObjectId(file_id),
        "user_id": session["user_id"]
    })

    return redirect(url_for("my_files"))


# =========================
# Logout
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# Run Application
# =========================

if __name__ == "__main__":
    app.run(debug=True)


