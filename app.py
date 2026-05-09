from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS

from mongo_db import train_collection

from services.groq_service import ask_groq
from services.railway_api import search_trains
from services.railway_api import live_status
from services.railway_api import train_schedule

import os

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
# SEARCH TRAINS BETWEEN STATIONS
# =========================================

@app.route("/api/search")

def search_api():

    try:

        from_station = request.args.get("from")
        to_station = request.args.get("to")

        data = search_trains(
            from_station,
            to_station
        )

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# =========================================
# LIVE TRAIN STATUS
# =========================================

@app.route("/api/live/<train_no>")

def live_api(train_no):

    try:

        data = live_status(train_no)

        train_collection.insert_one({
            "trainNo": train_no,
            "data": data
        })

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# =========================================
# TRAIN SCHEDULE
# =========================================

@app.route("/api/schedule/<train_no>")

def schedule_api(train_no):

    try:

        data = train_schedule(train_no)

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

            item["_id"] = str(item["_id"])

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
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )