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
        "irctc-api2.p.rapidapi.com"
}

# =========================================
# SEARCH TRAINS BETWEEN STATIONS
# =========================================

def search_trains(

    from_station,
    to_station

):

    url = (
        "https://irctc-api2.p.rapidapi.com/"
        "trainBetweenStations"
    )

    querystring = {

        "fromStationCode":
            from_station,

        "toStationCode":
            to_station,

        "dateOfJourney":
            "2026-05-10"
    }

    response = requests.get(

        url,

        headers=HEADERS,

        params=querystring
    )

    return response.json()

# =========================================
# LIVE TRAIN STATUS
# =========================================

def live_status(train_no):

    url = (
        "https://irctc-api2.p.rapidapi.com/"
        "liveTrainStatus"
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

    return response.json()

# =========================================
# TRAIN SCHEDULE
# =========================================

def train_schedule(train_no):

    url = (
        "https://irctc-api2.p.rapidapi.com/"
        "trainSchedule"
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

    return response.json()