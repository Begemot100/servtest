from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/<scope_id>", methods=["POST"])
def webhook(scope_id):
    headers = dict(request.headers)  # Сохраняем заголовки
    print(f"📩 Заголовки запроса: {headers}")  # Логируем заголовки

    if "Content-Type" not in headers or headers["Content-Type"] != "application/json":
        return jsonify({"error": "Unsupported Media Type", "received_headers": headers}), 415  # Возвращаем 415

    try:
        data = request.json  # Пробуем разобрать JSON
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "exception": str(e)}), 400  # Ошибка JSON

    print(f"📩 Тело запроса: {data}")  # Логируем тело

    return jsonify({"status": "success", "message": "Webhook received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)