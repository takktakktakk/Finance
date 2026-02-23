import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="coffee_user",
        password="TakkBerlin520",
        database="coffee_app"
    )

# 全件取得
def get_all_recipes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recipes ORDER BY created_at DESC, id DESC")
    recipes = cursor.fetchall()
    cursor.close()
    conn.close()
    return recipes

# 1件取得
def get_recipe_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recipes WHERE id=%s", (id,))
    recipe = cursor.fetchone()
    cursor.close()
    conn.close()
    return recipe

# 追加
def insert_recipe(data):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        INSERT INTO recipes
        (bean_type, country, farm, altitude, variety, process,
         roast_level, roast_day, bean_amount, grind, water_amount,
         ratio, water_temp, brew_time, dripper, filter_type,
         favorite, memo, acidity, sweetness, bitterness, flavor,
         aroma, body, after_taste, balance)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, data)

    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id

# 更新
def update_recipe(id, data):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        UPDATE recipes
        SET bean_type=%s, country=%s, farm=%s, altitude=%s, variety=%s, process=%s,
            roast_level=%s, roast_day=%s, bean_amount=%s, grind=%s, water_amount=%s,
            ratio=%s, water_temp=%s, brew_time=%s, dripper=%s, filter_type=%s,
            favorite=%s, memo=%s, acidity=%s, sweetness=%s, bitterness=%s, flavor=%s,
            aroma=%s, body=%s, after_taste=%s, balance=%s
        WHERE id=%s
    """, (*data, id))

    conn.commit()
    cursor.close()
    conn.close()

# 削除
def delete_recipe(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

def toggle_favorite(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        UPDATE recipes
        SET favorite = NOT favorite
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

def search_recipes(keyword):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM recipes
        WHERE bean_type LIKE %s
        OR country LIKE %s
        ORDER BY created_at DESC
    """

    like_keyword = f"%{keyword}%"
    cursor.execute(sql, (like_keyword, like_keyword))

    rows = cursor.fetchall()
    conn.close()

    return rows

def filter_recipes(keyword, roast):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM recipes WHERE 1=1"
    params = []

    if keyword:
        sql += " AND (bean_type LIKE %s OR country LIKE %s)"
        like_keyword = f"%{keyword}%"
        params.extend([like_keyword, like_keyword])

    if roast:
        sql += " AND roast_level = %s"
        params.append(roast)

    sql += " ORDER BY created_at DESC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    return rows