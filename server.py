from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/webhook/<scope_id>", methods=["POST"])
def webhook(scope_id):
    # Проверяем Content-Type
    if request.content_type != "application/json":
        return jsonify({"status": "error", "message": "Unsupported Media Type"}), 415

    data = request.json  # Получаем JSON из запроса
    print(f"📩 Получен Webhook от {scope_id}: {data}")

    return jsonify({"status": "success", "message": "Webhook received"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)