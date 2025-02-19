from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/<scope_id>", methods=["POST"])
def webhook(scope_id):
    print(f"📩 Заголовки запроса: {dict(request.headers)}")  # Логируем заголовки
    print(f"📩 Тело запроса: {request.data}")  # Логируем тело запроса

    if request.content_type != "application/json":
        return jsonify({"error": "Unsupported Media Type"}), 415  # Возвращаем 415

    data = request.json
    print(f"📩 Получен Webhook от {scope_id}: {data}")

    return jsonify({"status": "success", "message": "Webhook received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)