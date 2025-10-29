import streamlit as st
import requests
import base64
from io import BytesIO

API_BASE_URL = "https://obala-api.onrender.com"  # change to your deployed URL later

st.set_page_config(page_title="OBALA Login", layout="centered")

st.title("🔐 OBALA Access Portal")
st.subheader("Developed by WAIT Technologies")

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Select Option", menu)

# --- Signup Page ---
if choice == "Signup":
    st.subheader("Create an Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        payload = {"full_name": full_name, "email": email, "password": password}
        try:
            res = requests.post(f"{API_BASE_URL}/signup", json=payload)
            if res.status_code == 201:
                data = res.json()
                st.success(f"Account created successfully! 🎉 Your API Key: {data['api_key']}")
            else:
                st.error(res.json().get("error", "Signup failed!"))
        except Exception as e:
            st.error(f"Connection error: {e}")

# --- Login Page ---
else:
    st.subheader("Login to OBALA")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {"email": email, "password": password}
        try:
            res = requests.post(f"{API_BASE_URL}/login", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.success("Login successful ✅")
                st.code(f"Your API Key: {data['api_key']}")
                st.session_state["api_key"] = data["api_key"]
            else:
                st.error(res.json().get("error", "Login failed!"))
        except Exception as e:
            st.error(f"Connection error: {e}")

# --- After Login ---
if "api_key" in st.session_state:
    st.subheader("💬 Try OBALA Chat")
    user_prompt = st.text_area("Enter your question in Twi or English")

    if st.button("Send to OBALA"):
        headers = {"X-API-Key": st.session_state["api_key"]}
        payload = {"prompt": user_prompt}

        try:
            res = requests.post(f"{API_BASE_URL}/obala_chat", json=payload, headers=headers)
            if res.status_code == 200:
                data = res.json()
                st.info(f"OBALA says: {data.get('response', 'No text response received.')}")

                # --- Safe Audio Playback ---
                if "audio" in data and data["audio"]:
                    try:
                        audio_bytes = base64.b64decode(data["audio"])
                        st.audio(BytesIO(audio_bytes), format="audio/mp3")
                    except Exception as e:
                        st.error(f"Failed to play audio: {e}")
                else:
                    st.warning("No audio received from the OBALA API.")
            else:
                st.error(res.json().get("error", "Something went wrong."))
        except Exception as e:
            st.error(f"Connection error: {e}")
