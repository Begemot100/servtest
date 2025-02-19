from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/<scope_id>", methods=["POST"])
def webhook(scope_id):
    headers = dict(request.headers)  # Логируем заголовки
    print(f"📩 Заголовки запроса: {headers}")

    # Проверяем Content-Type
    content_type = headers.get("Content-Type", "")
    if "application/json" not in content_type:
        return jsonify({"error": "Unsupported Content-Type", "received_headers": headers}), 415

    try:
        data = request.json  # Пробуем разобрать JSON
        print(f"📩 Тело запроса: {data}")
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "exception": str(e)}), 400

    return jsonify({"status": "success", "message": "Webhook received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # Railway работает на порту 8080