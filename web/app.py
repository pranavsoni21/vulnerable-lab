from flask import Flask, request, render_template, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for flashing messages

def get_db_connection():
    conn = sqlite3.connect("user.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please provide both username and password")
            return render_template("login.html")

        conn = get_db_connection()
        cursor = conn.cursor()
        # ❌ intentionally vulnerable to SQL injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"Welcome, {username}! 🎉<br>FLAG{{phase1_sql_injection}}"
        else:
            flash("Invalid username or password")
            return render_template("login.html")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
