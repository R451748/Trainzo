from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS

from mongo_db import train_collection

from services.groq_service import ask_groq
from services.train_service import get_train_data

app = Flask(__name__)

CORS(app)

@app.route("/")

def home():

    return jsonify({
        "message":
        "Where Is My Train API Running"
    })

@app.route("/api/live/<train_no>")

def live_status(train_no):

    data = get_train_data(train_no)

    train_collection.insert_one(data)

    return jsonify(data)

@app.route("/api/history")

def history():

    history = list(

        train_collection.find(
            {},
            {"_id": 0}
        )
    )

    return jsonify(history)

@app.route(
    "/api/groq",
    methods=["POST"]
)

def groq_chat():

    body = request.json

    question = body.get(
        "question"
    )

    reply = ask_groq(question)

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )