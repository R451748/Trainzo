import streamlit as st
import requests
import folium

from streamlit_folium import st_folium

# =========================
# BACKEND API URL
# =========================

API_URL = "https://trainzo-backend-9umr.onrender.com/"

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Where Is My Train AI",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("🚆 Where Is My Train AI")

st.markdown(
    "AI-powered live train tracking system"
)

# =========================
# TRAIN SEARCH
# =========================

train_no = st.text_input(
    "Enter Train Number"
)

if st.button("Search Train"):

    try:

        response = requests.get(
            f"{API_URL}/api/live/{train_no}"
        )

        # Debug response
        st.write(
            "Status Code:",
            response.status_code
        )

        # If backend failed
        if response.status_code != 200:

            st.error(
                f"Backend Error: {response.status_code}"
            )

            st.write(response.text)

            st.stop()

        # Parse JSON safely
        try:

            data = response.json()

        except Exception:

            st.error(
                "Invalid JSON returned from backend"
            )

            st.write(response.text)

            st.stop()

        # Success Message
        st.success(
            "Train Data Loaded Successfully"
        )

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Train",
            data["trainNo"]
        )

        col2.metric(
            "Speed",
            f"{data['speed']} km/h"
        )

        col3.metric(
            "Updated",
            data["lastUpdated"]
        )

        # =========================
        # MAP
        # =========================

        st.subheader(
            "🗺️ Live Train Location"
        )

        m = folium.Map(

            location=[
                data["latitude"],
                data["longitude"]
            ],

            zoom_start=7
        )

        folium.Marker(

            [
                data["latitude"],
                data["longitude"]
            ],

            popup="🚆 Train Location",

            tooltip="Train"

        ).add_to(m)

        st_folium(
            m,
            width=1200,
            height=500
        )

    except Exception as e:

        st.error(
            f"Application Error: {e}"
        )

# =========================
# AI ASSISTANT
# =========================

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

        if response.status_code != 200:

            st.error(
                f"AI Backend Error: {response.status_code}"
            )

            st.write(response.text)

            st.stop()

        try:

            data = response.json()

        except Exception:

            st.error(
                "Invalid AI JSON response"
            )

            st.write(response.text)

            st.stop()

        st.info(
            data["reply"]
        )

    except Exception as e:

        st.error(
            f"AI Error: {e}"
        )

# =========================
# HISTORY
# =========================

st.divider()

st.subheader(
    "📜 Train Search History"
)

if st.button("Load History"):

    try:

        response = requests.get(
            f"{API_URL}/api/history"
        )

        if response.status_code != 200:

            st.error(
                f"History Error: {response.status_code}"
            )

            st.write(response.text)

            st.stop()

        try:

            history = response.json()

        except Exception:

            st.error(
                "Invalid History JSON"
            )

            st.write(response.text)

            st.stop()

        st.dataframe(history)

    except Exception as e:

        st.error(
            f"History Error: {e}"
        )