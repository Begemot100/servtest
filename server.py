import os
import psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Подключение к БД PostgreSQL на Railway
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:KpoILsSduSWZjmMzjMyGGVvqHYAAODXz@postgres-q5my.railway.internal:5432/railway")

# Подключаемся к БД
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Создаём таблицу, если её нет
cur.execute("""
    CREATE TABLE IF NOT EXISTS webhooks (
        id SERIAL PRIMARY KEY,
        scope_id TEXT,
        payload JSONB,
        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Запускаем Flask сервер
app = Flask(__name__)

@app.route("/webhook/<scope_id>", methods=["POST"])
def webhook(scope_id):
    data = request.json  # Получаем JSON из запроса
    print(f"📩 Получен Webhook от {scope_id}: {data}")

    # Сохраняем в БД
    cur.execute("INSERT INTO webhooks (scope_id, payload) VALUES (%s, %s)", (scope_id, json.dumps(data)))
    conn.commit()

    return jsonify({"status": "success", "message": "Webhook received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)