from flask import Flask, request, render_template, flash, redirect, url_for
import sqlite3
import logging
import os

app = Flask(__name__)
app.secret_key = "supersecret"  # keep for flash messages

# basic logging of suspicious attempts
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vuln-lab")

DB_PATH = "user.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def naive_filter(s: str) -> bool:
    """Return True if input contains blacklisted tokens (simple heuristic)."""
    if not s:
        return False
    # naive blacklist (intentionally incomplete)
    blacklist = [
        "--", ";", "/*", "*/", "drop ", "insert ", "update ", "delete ",
        "union ", "select ", "alter ", "exec ", "xp_", " and ", "or"
        "0x", "char(", "cast(", "convert("
    ]
    low = s.lower()
    for token in blacklist:
        if token in low:
            return True
    return False


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please provide both username and password", "error")
            return redirect(url_for("login"))

        # Apply naive blacklist to both fields
        if naive_filter(username) or naive_filter(password):
            # Log the blocked input (helpful for teaching)
            logger.info("Blocked suspicious input. username=%s password=%s", username, password)
            flash("Suspicious input detected!", "error")
            return redirect(url_for("login"))

        conn = get_db_connection()
        cursor = conn.cursor()

        # "Partially-protected" - parameterized username, but vulnerable password check
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            # Intentionally vulnerable: string concatenation with password
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            try:
                cursor.execute(query)
                user_with_pass = cursor.fetchone()
            except Exception as e:
                # Show DB error for learning purposes
                logger.exception("DB error while executing query: %s", query)
                flash(f"Database error: {e}", "error")
                conn.close()
                return redirect(url_for("login"))

            conn.close()
            if user_with_pass:
                return f"Welcome, {username}! 🎉<br>FLAG{{phase1_sql_injection}}"
            else:
                flash("Invalid username or password", "error")
                return redirect(url_for("login"))
        else:
            flash("Invalid username or password", "error")
            conn.close()
            return redirect(url_for("login"))

    return render_template("login.html")


if __name__ == "__main__":
    # ensure DB is present
    if not os.path.exists(DB_PATH):
        # hint: tell user to run db_init.py first
        logger.warning("%s not found. Run db_init.py to initialize the database.", DB_PATH)
    app.run(debug=True, host="0.0.0.0", port=5000)
