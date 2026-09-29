from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host="mysql",
        user="root",
        password="rootpassword",
        database="taskmanager",
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

        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()

    connection.close()

    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)