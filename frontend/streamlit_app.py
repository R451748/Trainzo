import streamlit as st
import requests
import folium

from streamlit_folium import st_folium

# =========================================
# BACKEND API URL
# =========================================

API_URL = "https://trainzo-backend-9umr.onrender.com"

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Where Is My Train",
    layout="wide"
)

# =========================================
# TITLE
# =========================================

st.title("🚆 Where Is My Train")

st.markdown(
    "Live Train Tracking System"
)

# =========================================
# SESSION STATE
# =========================================

if "trains" not in st.session_state:
    st.session_state.trains = []

if "selected_train" not in st.session_state:
    st.session_state.selected_train = None

if "ai_reply" not in st.session_state:
    st.session_state.ai_reply = ""

# =========================================
# SEARCH STATIONS
# =========================================

col1, col2 = st.columns(2)

with col1:

    from_station = st.text_input(
        "From Station Code",
        placeholder="SBC"
    )

with col2:

    to_station = st.text_input(
        "To Station Code",
        placeholder="MAS"
    )

if st.button("🚆 Find Trains"):

    try:

        response = requests.get(

            f"{API_URL}/api/search",

            params={
                "from": from_station,
                "to": to_station
            }
        )

        if response.status_code == 200:

            data = response.json()

            if "data" in data:

                st.session_state.trains = data["data"]

            else:

                st.error(
                    "No trains found"
                )

        else:

            st.error(
                "Search failed"
            )

    except Exception as e:

        st.error(
            f"Search Error: {e}"
        )

# =========================================
# TRAIN LIST
# =========================================

if st.session_state.trains:

    st.subheader(
        "🚉 Available Trains"
    )

    for train in st.session_state.trains:

        with st.container(border=True):

            col1, col2, col3 = st.columns([5, 3, 2])

            col1.markdown(

                f"""
                ### {train.get('train_number')}
                {train.get('train_name')}
                """
            )

            col2.markdown(

                f"""
                ⏰ {train.get('from_std')}
                →
                {train.get('to_std')}
                """
            )

            if col3.button(

                "Track",

                key=train.get(
                    "train_number"
                )
            ):

                st.session_state.selected_train = (
                    train.get(
                        "train_number"
                    )
                )

# =========================================
# LIVE TRACKING
# =========================================

if st.session_state.selected_train:

    train_no = (
        st.session_state.selected_train
    )

    st.divider()

    st.subheader(
        f"🚆 Live Tracking - {train_no}"
    )

    # =====================================
    # LIVE STATUS API
    # =====================================

    try:

        live_response = requests.get(
            f"{API_URL}/api/live/{train_no}"
        )

        live_data = (
            live_response.json()
        )

    except Exception as e:

        st.error(
            f"Live API Error: {e}"
        )

        live_data = {}

    # =====================================
    # SCHEDULE API
    # =====================================

    try:

        schedule_response = requests.get(
            f"{API_URL}/api/schedule/{train_no}"
        )

        schedule_data = (
            schedule_response.json()
        )

    except Exception as e:

        st.error(
            f"Schedule API Error: {e}"
        )

        schedule_data = {}

    # =====================================
    # LIVE INFO
    # =====================================

    current_station = (
        live_data.get(
            "current_station_name",
            "Unknown"
        )
    )

    next_station = (
        live_data.get(
            "next_station_name",
            "Unknown"
        )
    )

    delay = (
        live_data.get(
            "delay",
            "0"
        )
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Current Station",
        current_station
    )

    col2.metric(
        "Next Station",
        next_station
    )

    col3.metric(
        "Delay",
        f"{delay} min"
    )

    # =====================================
    # MAP
    # =====================================

    st.subheader(
        "🗺️ Live Train Map"
    )

    latitude = 12.9716
    longitude = 77.5946

    m = folium.Map(

        location=[
            latitude,
            longitude
        ],

        zoom_start=6
    )

    folium.Marker(

        [
            latitude,
            longitude
        ],

        popup=f"🚆 Train {train_no}"

    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=500
    )

    # =====================================
    # STATION TIMELINE
    # =====================================

    st.subheader(
        "📍 Station Timeline"
    )

    if "data" in schedule_data:

        route = (
            schedule_data["data"]
            .get("route", [])
        )

        for station in route:

            with st.container(border=True):

                st.markdown(

                    f"""
                    ### 🚉 {station.get('station_name')}

                    Arrival:
                    {station.get('arrival_time')}

                    Departure:
                    {station.get('departure_time')}
                    """
                )

# =========================================
# AI ASSISTANT
# =========================================

st.divider()

st.subheader(
    "🤖 AI Assistant"
)

question = st.text_input(
    "Ask AI about train"
)

if st.button("Ask AI"):

    try:

        response = requests.post(

            f"{API_URL}/api/groq",

            json={
                "question": question
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.ai_reply = (
                data["reply"]
            )

        else:

            st.error(
                "AI request failed"
            )

    except Exception as e:

        st.error(
            f"AI Error: {e}"
        )

# =========================================
# SHOW AI RESPONSE
# =========================================

if st.session_state.ai_reply:

    st.info(
        st.session_state.ai_reply
    )