# 🛠️ Project Setup Instructions
Welcome! Follow these steps to get the project running locally on your machine.

## 1. 📥 Clone the Repository
git clone https://github.com/dovydas-t/TAD-Universiteto-sistema.git
cd TAD-Universiteto-sistema

## 2. 🌱 Switch to the Development Branch
git checkout dev
Make sure you are working on the correct branch for development.


## 3. 🐍 Create and Activate Virtual Environment
### Windows:
python -m venv venv
venv\Scripts\activate
### macOS/Linux:
python3 -m venv venv
source venv/bin/activate


## 4. 📦 Install Project Requirements
pip install -r requirements.txt


## 5. ⚙️ Create Your Own `.env` File
Create a `.env` file in the root directory with the following content (replace values with your own):
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://
FLASK_APP=run.py
FLASK_ENV=development

## 6. 🛢️ Create the Database in MySQL
Log into MySQL and run:
CREATE DATABASE universiteto_sistema CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

## 7. 🔄 Run Database Migrations with Alembic
flask db upgrade
or
flask db upgrade head

## 9. 🌿 Git Workflow (Feature Branches)
# Create a new feature branch:
git checkout -b feature/your-feature-name
# After work is done:
git add .
git commit -m "Add: meaningful message"
git push origin feature/your-feature-name
# Then open a Pull Request (PR) to merge into dev.
# Important: Never commit directly to dev or main. Always work on your own feature branch.

## 7. 🚀 Run the App
Use the appropriate command, depending on your project setup:
flask run
or
python run.py

## ✅ You're Done!
Check that:
* MySQL is running.
* `.env` is correctly configured.
* You’re on the `dev` branch.
* Requirements are installed.
