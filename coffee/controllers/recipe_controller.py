from flask import Blueprint, render_template, request, redirect, jsonify
from models.recipe_model import get_all_recipes, get_recipe_by_id, insert_recipe, update_recipe, delete_recipe, toggle_favorite, search_recipes, filter_recipes

recipe_bp = Blueprint('recipe', __name__)

# ✅ トップページ（新規登録フォーム）
@recipe_bp.route("/")
def form():
    query = request.args.get("q", "")
    roast = request.args.get("roast", "")

    recipes = filter_recipes(query, roast)

    # ✅ 焙煎度を英語キーに変換
    roast_map = {
        "ライトロースト": "light",
        "シナモンロースト": "cinnamon",
        "ミディアムロースト": "medium",
        "ハイロースト": "high",
        "シティロースト": "city",
        "フルシティロースト": "fullcity",
        "フレンチロースト": "french",
        "イタリアンロースト": "italian"
    }

    for r in recipes:
        r["roast_key"] = roast_map.get(r["roast_level"], "default")

    return render_template("form.html", recipes=recipes)

@recipe_bp.route("/add", methods=["POST"])
def add_recipe():
    def get_val(key, convert_to=None):
        val = request.form.get(key)
        if val == "":
            val = None
        if val is not None and convert_to:
            try:
                val = convert_to(val)
            except ValueError:
                val = None
        return val

    data = (
        request.form.get("bean_type"),
        request.form.get("country"),
        request.form.get("farm"),
        request.form.get("altitude"),
        request.form.get("variety"),
        request.form.get("process"),
        request.form.get("roast_level"),
        get_val("roast_day"),
        get_val("bean_amount", float),
        request.form.get("grind"),
        get_val("water_amount", float),
        get_val("ratio", float),
        get_val("water_temp", int),
        request.form.get("brew_time"),
        request.form.get("dripper"),
        request.form.get("filter_type"),
        1 if request.form.get("favorite") else 0,
        request.form.get("memo"),
        get_val("acidity", int),
        get_val("sweetness", int),
        get_val("bitterness", int),
        get_val("flavor", int),
        get_val("aroma", int),
        get_val("body", int),
        get_val("after_taste", int),
        get_val("balance", int)
    )

    new_id = insert_recipe(data)

    return redirect(f"/result/{new_id}")

# ✅ レシピ一覧
@recipe_bp.route("/list")
def recipes():
    query = request.args.get("q", "")
    roast = request.args.get("roast", "")

    recipes = filter_recipes(query, roast)

    # ✅ 焙煎度を英語キーに変換
    roast_map = {
        "ライトロースト": "light",
        "シナモンロースト": "cinnamon",
        "ミディアムロースト": "medium",
        "ハイロースト": "high",
        "シティロースト": "city",
        "フルシティロースト": "fullcity",
        "フレンチロースト": "french",
        "イタリアンロースト": "italian"
    }

    for r in recipes:
        r["roast_key"] = roast_map.get(r["roast_level"], "default")

    return render_template("list.html", recipes=recipes)

# ✅ 編集ページ
@recipe_bp.route("/edit/<int:id>")
def edit_recipe(id):
    recipe = get_recipe_by_id(id)
    return render_template("edit.html", recipe=recipe)

# ✅ 更新処理
@recipe_bp.route("/update/<int:id>", methods=["POST"])
def update_recipe_route(id):
    def get_val(key, convert_to=None):
        val = request.form.get(key)
        if val == "":
            val = None
        if val is not None and convert_to:
            try:
                val = convert_to(val)
            except ValueError:
                val = None
        return val

    data = (
        request.form.get("bean_type"),
        request.form.get("country"),
        request.form.get("farm"),
        request.form.get("altitude"),
        request.form.get("variety"),
        request.form.get("process"),
        request.form.get("roast_level"),
        get_val("roast_day"),
        get_val("bean_amount", float),
        request.form.get("grind"),
        get_val("water_amount", float),
        get_val("ratio", float),
        get_val("water_temp", int),
        request.form.get("brew_time"),
        request.form.get("dripper"),
        request.form.get("filter_type"),
        1 if request.form.get("favorite") else 0,
        request.form.get("memo"),
        get_val("acidity", int),
        get_val("sweetness", int),
        get_val("bitterness", int),
        get_val("flavor", int),
        get_val("aroma", int),
        get_val("body", int),
        get_val("after_taste", int),
        get_val("balance", int)
    )

    update_recipe(id, data)

    return redirect(f"/result/{id}")

@recipe_bp.route("/result/<int:id>")
def recipe_detail(id):
    # 1件だけ取得
    recipe = get_recipe_by_id(id)

    # ✅ 焙煎度マップ
    roast_map = {
        "ライトロースト": "light",
        "シナモンロースト": "cinnamon",
        "ミディアムロースト": "medium",
        "ハイロースト": "high",
        "シティロースト": "city",
        "フルシティロースト": "fullcity",
        "フレンチロースト": "french",
        "イタリアンロースト": "italian"
    }

    # ✅ roast_key を追加
    recipe["roast_key"] = roast_map.get(recipe["roast_level"], "default")

    return render_template("result.html", recipe=recipe)

# ✅ 削除処理
@recipe_bp.route("/delete/<int:id>", methods=["POST"])
def delete_recipe_route(id):
    delete_recipe(id)
    return redirect("/list")

from flask import jsonify

@recipe_bp.route("/toggle_favorite/<int:id>", methods=["POST"])
def toggle_favorite_route(id):
    toggle_favorite(id)
    return jsonify({"success": True})