import streamlit as st
import sqlite3
import time
from db import init_db, register_user, store_transport_data, get_logged_in_user_id, calculate_emissions

# Set page configuration
st.set_page_config(page_title="Transport Emissions", layout="wide")

# Initialize the database (call it once when app starts)
init_db()

# Sidebar Navigation (Collapsible)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=60)
    st.title("🚀 Menu")
    
    option = st.radio("Go to", ["Home", "Register/Login", "Transport", "View Data", "Contact Us"])

# Home Page
if option == "Home":
    st.header("🌍 Welcome!")
    st.write("Track your carbon footprint and reduce emissions.")

# Register/Login Page
elif option == "Register/Login":
    st.header("🔑 Register / Login")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register/Login"):
        if name and email and password:
            register_user(name, email, password)
            st.success("✅ Registration successful!")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("⚠️ Please fill all fields.")

# Transport Page (Restricted)
elif option == "Transport":
    user_id = get_logged_in_user_id()
    if not user_id:
        st.warning("⚠️ Please Register/Login first.")
    else:
        st.header("🚗 Transport Emissions")
        transport_mode = st.radio("Select Transport Mode", ["Car", "Bike", "Bus", "Walking"])
        distance = st.slider("Distance traveled (km)", 1, 50, 5)
        
        if st.button("Calculate Emissions"):
            emissions = calculate_emissions(transport_mode, distance)
            store_transport_data(user_id, transport_mode, distance, emissions)
            st.write(f"Your emissions: {emissions} kg CO2")

# View Data Page (Restricted)
elif option == "View Data":
    user_id = get_logged_in_user_id()
    if not user_id:
        st.warning("⚠️ Please Register/Login first.")
    else:
        st.header("Your Transport Emissions Data")
        # Fetch user emissions data from the database
        conn = sqlite3.connect('data/emissions.db')
        c = conn.cursor()
        c.execute("SELECT transport_mode, distance, emissions FROM transport_data WHERE user_id = ?", (user_id,))
        data = c.fetchall()
        conn.close()
        
        if data:
            for entry in data:
                st.write(f"Mode: {entry[0]}, Distance: {entry[1]} km, Emissions: {entry[2]} kg CO2")
        else:
            st.write("No data available.")

# Contact Us Page
elif option == "Contact Us":
    st.header("📞 Contact Us")
    name = st.text_input("Your Name")
    message = st.text_area("Your Message")
    st.button("Send Message")
st.markdown("""
    <style>
        /* Center the content and restrict width */
        .stApp {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f5f5f5;
        }

        .mobile-box {
            width: 360px; /* Mobile screen size */
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="mobile-box">', unsafe_allow_html=True)

# Your existing Streamlit content goes here
st.header("🔑 Register / Login")
name = st.text_input("Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register/Login"):
    if name and email and password:
        st.success("✅ Registration successful!")
    else:
        st.error("⚠️ Please fill all fields.")

st.markdown('</div>', unsafe_allow_html=True)
