# 🔐 PrivateVault

**PrivateVault** is a secure file storage web application built using **Python Flask** and **MongoDB**.

It allows users to securely log in, upload files, manage stored files, and download them through a simple web interface.

## 🚀 Live Demo

👉 **[Open PrivateVault Website](https://privatevault-z2a5.onrender.com)**

---

## ✨ Features

* 🔐 Secure user login and authentication
* 📁 File upload
* ⬇️ File download
* 🗑️ File management
* 🕒 File history
* 📊 Dashboard
* 🚪 Secure logout
* 🗄️ MongoDB database integration
* 🌐 Responsive web interface
* ☁️ Deployed on Render

---

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* Gunicorn

### Database

* MongoDB
* PyMongo
* MongoDB Atlas

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

### Security

* Python Cryptography
* Environment variables using `.env`

### Deployment & Tools

* Git
* GitHub
* Render
* Visual Studio Code

---

## 📂 Project Structure

```text
PrivateVault/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── database/
│   └── mongodb.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── history.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── ...
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/gauravrede96k/PrivateVault.git
```

### 2. Open the project

```bash
cd PrivateVault
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
```

**Never upload your `.env` file to GitHub.**

Make sure `.env` is included in `.gitignore`.

---

## ▶️ Run Locally

Start the Flask application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## ☁️ Deployment

PrivateVault is deployed using **Render**.

### Deployment Flow

```text
GitHub
   ↓
Render
   ↓
Flask + Gunicorn
   ↓
MongoDB Atlas
```

Every new update pushed to the `main` branch can be deployed through Render.

---

## 🔐 Security

PrivateVault uses:

* Environment variables for sensitive configuration
* MongoDB Atlas for database storage
* Flask session-based authentication
* Cryptography for secure file handling
* `.gitignore` to prevent sensitive files from being committed

> Never expose your MongoDB password, secret key, API keys, or `.env` file publicly.

---

## 📸 Application

### Login

Users can securely log in to access their PrivateVault dashboard.

### Dashboard

The dashboard provides access to stored files and application features.

### File Management

Users can upload and manage their files through the application.

---

## 🎯 Future Improvements

* 📱 Android application
* 🔎 File search
* 📂 Folder management
* 👤 User profile
* 🔔 Notifications
* 🔐 Two-factor authentication
* 📈 Storage analytics
* 🌙 Improved dark mode
* 🛡️ Advanced file encryption

---

## 👨‍💻 Developer

**Gaurav Dattatray Rede**

Python | Flask | MongoDB | Web Development | AI/ML

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**PrivateVault — Your files, your privacy. 🔐**
