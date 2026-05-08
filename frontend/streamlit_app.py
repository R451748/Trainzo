import streamlit as st
import requests
import folium

from streamlit_folium import st_folium

# =========================
# BACKEND API URL
# =========================

API_URL = "https://trainzo-backend-9umr.onrender.com"

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Where Is My Train AI",
    layout="wide"
)

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

        st.write(
            "Status Code:",
            response.status_code
        )

        st.write(
            "Response:",
            response.text
        )

        if response.status_code != 200:

            st.error(
                "Backend request failed"
            )

            st.stop()

        try:

            data = response.json()

        except Exception:

            st.error(
                "Backend did not return valid JSON"
            )

            st.stop()

        st.success(
            "Train Data Loaded"
        )

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

            popup="🚆 Train Location"

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

        st.write(response.text)

        data = response.json()

        st.info(data["reply"])

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

        st.write(response.text)

        history = response.json()

        st.dataframe(history)

    except Exception as e:

        st.error(
            f"History Error: {e}"
        )