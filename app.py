import streamlit as st
import requests

API_BASE_URL = "https://obala-api.onrender.com"  # replace with your deployed API

st.set_page_config(page_title="OBALA Login", layout="centered")

st.title("🔐 OBALA Access Portal")
st.subheader("Developed by WAIT Technologies")

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Select Option", menu)

# --- SIGNUP ---
if choice == "Signup":
    st.subheader("Create an Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        payload = {"full_name": full_name, "email": email, "password": password}
        res = requests.post(f"{API_BASE_URL}/signup", json=payload)
        if res.status_code == 201:
            data = res.json()
            st.success("✅ Account created successfully!")
            st.code(f"Your API Key: {data['api_key']}")
        else:
            st.error(res.json().get("error", "Signup failed!"))

# --- LOGIN ---
else:
    st.subheader("Login to OBALA")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {"email": email, "password": password}
        res = requests.post(f"{API_BASE_URL}/login", json=payload)
        if res.status_code == 200:
            data = res.json()
            st.success("✅ Login successful!")
            st.session_state["api_key"] = data["api_key"]
            st.code(f"Your API Key: {data['api_key']}")
        else:
            st.error(res.json().get("error", "Login failed!"))

# --- OBALA CHAT ---
if "api_key" in st.session_state:
    st.divider()
    st.subheader("💬 Try OBALA Chat")

    user_prompt = st.text_area("Enter your question in Twi or English")

    if st.button("Send to OBALA"):
        headers = {"X-API-Key": st.session_state["api_key"]}
        payload = {"prompt": user_prompt}
        res = requests.post(f"{API_BASE_URL}/obala_chat", json=payload, headers=headers)

        if res.status_code == 200:
            data = res.json()
            st.info(f"🗣️ OBALA says: {data['response']}")

            # --- Handle Audio File Path ---
            audio_path = data.get("audio_path")
            if audio_path:
                st.audio(audio_path, format="audio/wav")
                st.caption(f"🎵 Playing: {audio_path}")
            else:
                st.warning("No audio received from OBALA API.")
        else:
            st.error(res.json().get("error", "Something went wrong."))
