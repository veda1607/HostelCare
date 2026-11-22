
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("hostel.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create database and students table
def create_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            room TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Student Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        room = request.form.get("room", "").strip()

        # Input validation
        if not name or not email or not password or not room:
            message = "Please fill in all fields."

        elif len(password) < 8:
            message = "Password must contain at least 8 characters."

        else:
            conn = get_db_connection()

            try:
                hashed_password = generate_password_hash(password)

                conn.execute("""
                    INSERT INTO students
                    (name, email, password, room)
                    VALUES (?, ?, ?, ?)
                """, (name, email, hashed_password, room))

                conn.commit()

                message = "Registration successful! You can now log in."

            except sqlite3.IntegrityError:
                message = "This email is already registered."

            finally:
                conn.close()

    return render_template("register.html", message=message)


# Start application
if __name__ == "__main__":
    create_database()
    app.run(debug=True)





