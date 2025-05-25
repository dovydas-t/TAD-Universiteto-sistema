---

# 🛠️ Project Setup Instructions

Welcome! Follow these steps to get the project running locally on your machine.

---

## 1. 📥 Clone the Repository

```bash
git clone https://github.com/dovydas-t/TAD-Universiteto-sistema.git
cd TAD-Universiteto-sistema
```

---

## 2. 🌱 Switch to the Development Branch

```bash
git checkout dev
```

Always base your work on the `dev` branch unless told otherwise.

---

## 3. 🐍 Create and Activate Virtual Environment

### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. 📦 Install Project Requirements

```bash
pip install -r requirements.txt
```

---

## 5. ⚙️ Create Your Own `.env` File

Create a `.env` file in the root directory with this content:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=universiteto_sistema
```

---

## 6. 🛢️ Create the Database in MySQL

Log in to MySQL and create the database:

```sql
CREATE DATABASE universiteto_sistema CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 7. 🔄 Run Database Migrations with Alembic

If using Alembic for schema migrations:

### Run existing migrations:

```bash
alembic upgrade head
```

### Make a new migration after model changes:

```bash
alembic revision --autogenerate -m "Your message here"
alembic upgrade head
```

> Make sure your database URL is correctly set in `alembic.ini` or fetched from your `.env`.

---

## 8. 🎨 Code Formatting & Linting

We recommend using **Black** for formatting and **Flake8** for linting.

### Format code with Black:

```bash
black .
```

### Check code style with Flake8:

```bash
flake8 .
```

---

## 9. 🌿 Git Workflow (Feature Branches)

### Create a new feature branch:

```bash
git checkout -b feature/your-feature-name
```

### After work is done:

```bash
git add .
git commit -m "Add: meaningful message"
git push origin feature/your-feature-name
```

### Then open a Pull Request (PR) to merge into `dev`.

> **Important:** Never commit directly to `dev` or `main`. Always work on your own feature branch.

---

## 10. 🚀 Run the App

Depending on how your app is started, use one of the following:

```bash
flask run
```

or

```bash
python main.py
```

---

## ✅ You're Ready!

* ✅ You're on `dev`
* ✅ Virtual environment activated
* ✅ Requirements installed
* ✅ `.env` configured
* ✅ Database created
* ✅ Alembic migrations applied

---