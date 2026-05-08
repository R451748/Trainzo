import streamlit as st
import requests
import folium

from streamlit_folium import st_folium

st.set_page_config(
    page_title="Where Is My Train AI",
    layout="wide"
)

st.title("🚆 Where Is My Train AI")

st.markdown(
    "AI-powered live train tracking system"
)

train_no = st.text_input(
    "Enter Train Number"
)

if st.button("Search Train"):

    response = requests.get(
        f"http://127.0.0.1:5000/api/live/{train_no}"
    )

    data = response.json()

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

st.divider()

st.subheader(
    "🤖 AI Assistant"
)

question = st.text_input(
    "Ask AI about train"
)

if st.button("Ask AI"):

    response = requests.post(

        "http://127.0.0.1:5000/api/groq",

        json={
            "question": question
        }
    )

    data = response.json()

    st.info(data["reply"])

st.divider()

st.subheader(
    "📜 Train Search History"
)

if st.button("Load History"):

    response = requests.get(
        "http://127.0.0.1:5000/api/history"
    )

    history = response.json()

    st.dataframe(history)