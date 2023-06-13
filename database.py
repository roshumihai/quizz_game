import mysql.connector


def update_players_table(username, high_score):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Loveandsex1",
        database="players"
    )
    cursor = db.cursor()
    sql = "INSERT INTO players (names, high_score) VALUES (%s, %s) ON DUPLICATE KEY UPDATE high_score = VALUES(high_score)"
    val = (username, high_score)
    try:
        cursor.execute(sql, val)
        db.commit()
    except mysql.connector.IntegrityError as e:
        print(f"Error: Duplicate key {e}")
    finally:
        db.close()