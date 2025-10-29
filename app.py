# obala_twi_app.py
# OBALA Streamlit Frontend — Signup/Login + Chat Interface (Connected to Flask API)

import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder
import json
import os
from PIL import Image

# --- Configuration ---
API_BASE_URL = "https://obala-api.onrender.com"  # 🟢 Replace with your Render backend URL

# --- Page Setup ---
try:
    logo = Image.open("obpic.png")
    st.set_page_config(page_title="OBALA TWI", page_icon=logo, layout="centered")
except:
    st.set_page_config(page_title="OBALA TWI", page_icon="🇬🇭", layout="centered")

# --- Custom CSS ---
st.markdown("""
<style>
    .stButton>button {
        padding: 0.3rem 0.9rem;
        font-size: 0.85rem;
        border-radius: 0.5rem;
    }
    .centered-text {
        text-align: center;
        font-size: 1.2rem;
        margin-top: 15px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)


# --- AUTH FUNCTIONS ---
def signup_user(username, password):
    res = requests.post(f"{API_BASE_URL}/signup", json={"username": username, "password": password})
    if res.status_code == 200:
        return True
    else:
        return False

def login_user(username, password):
    res = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password})
    if res.status_code == 200:
        return res.json().get("api_key")
    else:
        return None

def obala_chat(prompt, api_key):
    headers = {"X-API-Key": api_key}
    data = {"prompt": prompt}
    res = requests.post(f"{API_BASE_URL}/obala_chat", headers=headers, json=data)
    if res.status_code == 200:
        return res.json().get("response", "")
    else:
        return "Mepakyɛw, ɛwɔ problem bi wɔ server no mu."


# --- SIDEBAR (AUTHENTICATION) ---
st.sidebar.title("🔐 OBALA Access")

auth_choice = st.sidebar.radio("Select Action", ["Login", "Signup"])

if auth_choice == "Signup":
    st.sidebar.subheader("Create New Account")
    username = st.sidebar.text_input("Username", key="signup_user")
    password = st.sidebar.text_input("Password", type="password", key="signup_pass")

    if st.sidebar.button("Create Account"):
        if signup_user(username, password):
            st.sidebar.success("✅ Account created successfully! Please log in.")
        else:
            st.sidebar.error("❌ Signup failed. Try again later.")

elif auth_choice == "Login":
    st.sidebar.subheader("Login to OBALA")
    username = st.sidebar.text_input("Username", key="login_user")
    password = st.sidebar.text_input("Password", type="password", key="login_pass")

    if st.sidebar.button("Login"):
        api_key = login_user(username, password)
        if api_key:
            st.session_state.api_key = api_key
            st.sidebar.success("✅ Login successful!")
        else:
            st.sidebar.error("❌ Invalid credentials.")


# --- MAIN INTERFACE ---
st.title("🇬🇭 OBALA — Your AI Assistant that Speaks and Hears Your Language")
st.caption("O- Omniscient • B- Bilingual • A- Akan • L- LLM • A- Agent")
st.caption("From WAIT ❤")
st.info("Type or speak in Twi or English. OBALA will respond in Twi.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Afehyia pa! Me din de OBALA. Mɛtumi aboa wo sɛn?"}
    ]

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input Section ---
audio_info = mic_recorder(start_prompt="🎤 Kasa (Speak)", stop_prompt="⏹️ Gyae (Stop)", just_once=True, key='recorder')
prompt = st.chat_input("Kyerɛw wo asɛm wɔ Twi anaa Borɔfo mu...")

# --- Handle Voice Input ---
if audio_info and audio_info['bytes']:
    st.warning("🎙 Voice messages are not yet processed in this demo. Use text input instead.")

# --- Handle Text Input ---
if prompt:
    if "api_key" not in st.session_state or not st.session_state.api_key:
        st.warning("Please log in before chatting with OBALA.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("OBALA redwene ho..."):
                response_text = obala_chat(prompt, st.session_state.api_key)
                st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()
