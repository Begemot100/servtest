import os
import json
import psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)

# Подключение к PostgreSQL на Railway
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:KpoILsSduSWZjmMzjMyGGVvqHYAAODXz@postgres-q5my.railway.internal:5432/railway")

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

@app.route("/webhook/<scope_id>", methods=["POST"])
def webhook(scope_id):
    if request.content_type != "application/json":
        return jsonify({"status": "error", "message": "Unsupported Media Type"}), 415

    try:
        data = request.get_json()
        if data is None:
            raise ValueError("Пустое тело запроса")

        # Сохраняем Webhook в PostgreSQL
        cur.execute("INSERT INTO webhooks (scope_id, payload) VALUES (%s, %s)", (scope_id, json.dumps(data)))
        conn.commit()

        print(f"📩 Получен Webhook от {scope_id}: {data}")

        return jsonify({"status": "success", "message": "Webhook saved"}), 200

    except Exception as e:
        print(f"❌ Ошибка при обработке Webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)