from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/<scope_id>", methods=["POST"])
def webhook(scope_id):
    data = request.json
    print(f"📩 Webhook от amoCRM: {data}")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)