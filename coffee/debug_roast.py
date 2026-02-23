import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="coffee_user",
        password="TakkBerlin520",
        database="coffee_app"
    )

def check_roasts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, roast_level FROM recipes")
    recipes = cursor.fetchall()
    
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

    print(f"{'ID':<5} | {'Roast Level (DB)':<20} | {'Mapped Key'}")
    print("-" * 50)

    for r in recipes:
        rl = r["roast_level"]
        # Check for EXACT match
        mapped = roast_map.get(rl, "MISSING")
        
        # Check for whitespace match
        if mapped == "MISSING" and rl:
             if rl.strip() in roast_map:
                 mapped = "WHITESPACE_ISSUE"
        
        print(f"{r['id']:<5} | '{rl}' | {mapped}")

    conn.close()

if __name__ == "__main__":
    check_roasts()
