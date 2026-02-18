from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL接続
db = mysql.connector.connect(
    host="localhost",
    user="coffee_user",
    password="TakkBerlin520",
    database="coffee_app"
)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        return "保存しました！"

    return render_template("form.html")


@app.route("/save", methods=["POST"])
def save():
    data = request.form

    cursor = db.cursor()

    sql = """
    INSERT INTO recipes
    (bean_type, country, process, roast_level,
     acidity, aroma, sweetness, bitterness, body,
     water_temp, grind)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["bean_type"],
        data["country"],
        data["process"],
        data["roast_level"],
        data["acidity"],
        data["aroma"],
        data["sweetness"],
        data["bitterness"],
        data["body"],
        data["water_temp"],
        data["grind"]
    )

    cursor.execute(sql, values)
    db.commit()

    recipe_id = cursor.lastrowid

    return redirect(f"/recipe/{recipe_id}")


@app.route("/recipe/<int:id>")
def recipe(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recipes WHERE id=%s", (id,))
    recipe = cursor.fetchone()

    return render_template("result.html", recipe=recipe)

@app.route("/recipes")
def recipes():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM recipes ORDER BY created_at DESC")
    recipes = cursor.fetchall()

    return render_template("recipes.html", recipes=recipes)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)