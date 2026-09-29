from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/", methods=["GET", "POST"])
def home():

    connection = get_db_connection()

    with connection.cursor() as cursor:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task VARCHAR(255) NOT NULL
            )
        """)

        if request.method == "POST":
            task = request.form.get("task")

            if task:
                cursor.execute(
                    "INSERT INTO tasks (task) VALUES (%s)",
                    (task,)
                )
                connection.commit()

            connection.close()

            return redirect(url_for("home"))

        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()

    connection.close()

    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)