from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS

from mongo_db import train_collection

from services.groq_service import ask_groq
from services.train_service import get_train_data

app = Flask(__name__)

CORS(app)

# =========================================
# HOME ROUTE
# =========================================

@app.route("/")

def home():

    return jsonify({
        "message":
        "Where Is My Train API Running"
    })

# =========================================
# LIVE TRAIN STATUS
# =========================================

@app.route("/api/live/<train_no>")

def live_status(train_no):

    try:

        data = get_train_data(train_no)

        # Save into MongoDB
        result = train_collection.insert_one(data)

        # Convert ObjectId to string
        data["_id"] = str(
            result.inserted_id
        )

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# =========================================
# TRAIN HISTORY
# =========================================

@app.route("/api/history")

def history():

    try:

        history_data = []

        for item in train_collection.find():

            # Convert ObjectId
            item["_id"] = str(
                item["_id"]
            )

            history_data.append(item)

        return jsonify(history_data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# =========================================
# GROQ AI CHAT
# =========================================

@app.route(
    "/api/groq",
    methods=["POST"]
)

def groq_chat():

    try:

        body = request.json

        question = body.get(
            "question"
        )

        reply = ask_groq(question)

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )