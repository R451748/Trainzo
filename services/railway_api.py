import requests
import os

from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv(
    "RAPID_API_KEY"
)

HEADERS = {

    "x-rapidapi-key":
        RAPID_API_KEY,

    "x-rapidapi-host":
        "irctc1.p.rapidapi.com"
}

# =========================================
# SEARCH TRAINS
# =========================================

def search_trains(

    from_station,
    to_station

):

    url = (
        "https://irctc1.p.rapidapi.com/"
        "api/v3/trainBetweenStations"
    )

    querystring = {

        "fromStationCode":
            from_station,

        "toStationCode":
            to_station
    }

    response = requests.get(

        url,

        headers=HEADERS,

        params=querystring
    )

    print(response.text)

    return response.json()

# =========================================
# LIVE STATUS
# =========================================

def live_status(train_no):

    url = (
        "https://irctc1.p.rapidapi.com/"
        "api/v1/liveTrainStatus"
    )

    querystring = {

        "trainNo":
            train_no,

        "startDay":
            "1"
    }

    response = requests.get(

        url,

        headers=HEADERS,

        params=querystring
    )

    print(response.text)

    return response.json()

# =========================================
# TRAIN SCHEDULE
# =========================================

def train_schedule(train_no):

    url = (
        "https://irctc1.p.rapidapi.com/"
        "api/v1/getTrainSchedule"
    )

    querystring = {

        "trainNo":
            train_no
    }

    response = requests.get(

        url,

        headers=HEADERS,

        params=querystring
    )

    print(response.text)

    return response.json()