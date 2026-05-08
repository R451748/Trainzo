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
    page_title="Where Is My Train AI",
    layout="wide"
)

# =========================================
# TITLE
# =========================================

st.title("🚆 Where Is My Train AI")

st.markdown(
    "AI-powered live train tracking system"
)

# =========================================
# SESSION STATE
# =========================================

if "train_data" not in st.session_state:
    st.session_state.train_data = None

if "history_data" not in st.session_state:
    st.session_state.history_data = []

if "ai_reply" not in st.session_state:
    st.session_state.ai_reply = ""

# =========================================
# TRAIN SEARCH
# =========================================

train_no = st.text_input(
    "Enter Train Number"
)

if st.button("Search Train"):

    try:

        response = requests.get(
            f"{API_URL}/api/live/{train_no}"
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.train_data = data

        else:

            st.error(
                "Backend request failed"
            )

            st.write(
                response.text
            )

    except Exception as e:

        st.error(
            f"Application Error: {e}"
        )

# =========================================
# SHOW TRAIN DATA
# =========================================

if st.session_state.train_data:

    data = st.session_state.train_data

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

    # =====================================
    # MAP
    # =====================================

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

        popup="🚆 Train Location"

    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=500
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

            st.session_state.ai_reply = data["reply"]

        else:

            st.error(
                "AI request failed"
            )

            st.write(
                response.text
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

# =========================================
# HISTORY
# =========================================

st.divider()

st.subheader(
    "📜 Train Search History"
)

if st.button("Load History"):

    try:

        response = requests.get(
            f"{API_URL}/api/history"
        )

        if response.status_code == 200:

            history = response.json()

            st.session_state.history_data = history

        else:

            st.error(
                "History request failed"
            )

            st.write(
                response.text
            )

    except Exception as e:

        st.error(
            f"History Error: {e}"
        )

# =========================================
# SHOW HISTORY
# =========================================

if st.session_state.history_data:

    st.dataframe(
        st.session_state.history_data
    )