import streamlit as st
import requests
import folium

from streamlit_folium import st_folium

API_URL = "https://trainzo-backend-9umr.onrender.com"

st.set_page_config(
    page_title="Where Is My Train",
    layout="wide"
)

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

# =========================================
# SEARCH UI
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

# =========================================
# FIND TRAINS
# =========================================

if st.button("🚆 Find Trains"):

    try:

        response = requests.get(

            f"{API_URL}/api/search",

            params={

                "from":
                    from_station,

                "to":
                    to_station
            }
        )

        data = response.json()

        st.write(data)

        if "data" in data:

            trains = data["data"]

            if isinstance(
                trains,
                list
            ):

                st.session_state.trains = (
                    trains
                )

            else:

                st.error(
                    "Unexpected API format"
                )

        else:

            st.error(
                "No trains found"
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

    try:

        live_response = requests.get(
            f"{API_URL}/api/live/{train_no}"
        )

        live_data = (
            live_response.json()
        )

        st.write(live_data)

    except Exception as e:

        st.error(
            f"Live API Error: {e}"
        )

        live_data = {}

    latitude = 12.9716
    longitude = 77.5946

    st.subheader(
        "🗺️ Live Train Map"
    )

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