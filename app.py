import streamlit as st
import sqlite3
import time
import qrcode
from io import BytesIO
from db import init_db, register_user, authenticate_user, store_transport_data, get_logged_in_user_id, update_password

# Initialize the database
init_db()

# Set up session state for login management
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'reset_password' not in st.session_state:
    st.session_state.reset_password = False

# Define the URL for your app (replace with your actual app URL)
app_url = "http://localhost:8504/"

# Generate the QR code for your app URL
qr = qrcode.make(app_url)
buf = BytesIO()
qr.save(buf, format="PNG")
buf.seek(0)

# Sidebar Navigation (single definition)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=60)
    st.title("🚀 Menu")
    option = st.radio("Go to", 
                      ["Home", "Register/Login", "Scan QR", "Transport", "Food", "View Data", "Contact Us"])
    
    # Logout button (if logged in)
    if st.session_state.user_id:
        if st.button("Logout"):
            st.session_state.user_id = None
            st.success("✅ Logged out successfully!")
            time.sleep(1)
            st.experimental_rerun()

# Main Container for Mobile-Friendly Display
with st.container():
    st.markdown("<div style='max-width: 360px; margin: auto;'>", unsafe_allow_html=True)
    
    # Home Page
    if option == "Home":
        st.header("🌍 Welcome to the Event Emissions Data Collector!")
        st.write(
            "We developed a dashboard using Streamlit that displays **Scope 1, 2, and 3 emissions** for an event. "
            "This web application allows event attendees to register and submit transportation and food data."
        )
        st.subheader("📌 What You Can Do Here:")
        st.markdown("""
        - ✅ **Register & Login** to access the platform.
        - ✅ **Enter Transportation Details** – Specify your mode of travel (Car, Train, Airplane, etc.) and distance traveled.
        - ✅ **Choose Your Food Preference** – Select from Veg, Non-Veg, or Vegan options.
        
        This data helps event managers estimate total emissions from attendee travel and food consumption.
        """)
        st.write("Use the sidebar to navigate: **Home, Register/Login, Scan QR, Transport, Food, and Contact Us.**")
    
    # Register/Login Page
    elif option == "Register/Login":
        st.header("🔑 Register / Login")
        tab1, tab2 = st.tabs(["Register", "Login"])
        
        with tab1:
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Register"):
                if name and email and password:
                    success = register_user(name, email, password)
                    if success:
                        st.success("✅ Registration successful! Please login.")
                    else:
                        st.error("⚠️ Email already exists.")
                else:
                    st.error("⚠️ Please fill all fields.")
        
        with tab2:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                user_id = authenticate_user(email, password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("⚠️ Invalid credentials.")
            
            if st.button("Forgot Password?"):
                st.session_state.reset_password = True
                st.experimental_rerun()
        
        if st.session_state.reset_password:
            st.header("🔄 Reset Password")
            email = st.text_input("Enter your registered email")
            new_password = st.text_input("New Password", type="password")
            if st.button("Reset Password"):
                success = update_password(email, new_password)
                if success:
                    st.success("✅ Password reset successfully! Please login.")
                    st.session_state.reset_password = False
                    st.experimental_rerun()
                else:
                    st.error("⚠️ Email not found.")
    
    # Scan QR Page: Display the QR code so users can scan it with their mobile device
    elif option == "Scan QR":
        st.header("📱 Scan this QR Code")
        st.write("Scan this QR code with your mobile device to open the app and enter your transport and food preferences.")
        st.image(buf, caption="Scan me!", use_column_width=True)
    
    # Transport Data Collection Page
    elif option == "Transport":
        if not st.session_state.user_id:
            st.warning("⚠️ Please Register/Login first.")
        else:
            st.header("🚗 Transport Details")
            st.write("Select all the modes of transportation you used and provide the distance traveled for each.")
            selected_modes = st.multiselect("Select Transport Modes", 
                                            ["3-Wheeler CNG", "2-Wheeler", "4W Petrol", "4W CNG", "BUS", 
                                             "Electric 2-Wheeler", "Electric 4-Wheeler", "Local Train (Electricity)", "Air ways"])
            distances = {}
            for mode in selected_modes:
                distances[mode] = st.number_input(f"Distance traveled by {mode} (km)", 
                                                  min_value=1, max_value=5000, step=1, key=mode)
            if st.button("Submit Transport Data"):
                for mode, distance in distances.items():
                    store_transport_data(st.session_state.user_id, mode, distance, None)
                st.success("✅ Transport details submitted!")
    
    # Food Preferences Data Collection Page
    elif option == "Food":
        if not st.session_state.user_id:
            st.warning("⚠️ Please Register/Login first.")
        else:
            st.header("🍽 Food Preferences")
            food_choice = st.radio("Select Food Preference", ["Veg", "Non-Veg", "Vegan"])
            conn = sqlite3.connect('data/emissions.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS food_preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        food_choice TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
            conn.commit()
            if st.button("Save Preference"):
                c.execute("INSERT INTO food_preferences (user_id, food_choice) VALUES (?, ?)", 
                          (st.session_state.user_id, food_choice))
                conn.commit()
                conn.close()
                st.success("✅ Food preference saved!")
    
    # View Data Page
    elif option == "View Data":
        if not st.session_state.user_id:
            st.warning("⚠️ Please Register/Login first.")
        else:
            st.header("📊 Your Submitted Data")
            conn = sqlite3.connect('data/emissions.db')
            c = conn.cursor()
            c.execute("SELECT transport_mode, distance FROM transport_data WHERE user_id = ?", (st.session_state.user_id,))
            transport_data = c.fetchall()
            c.execute("SELECT food_choice FROM food_preferences WHERE user_id = ?", (st.session_state.user_id,))
            food_data = c.fetchone()
            conn.close()
            if transport_data:
                st.subheader("🚗 Transport Details")
                for entry in transport_data:
                    st.write(f"**Mode:** {entry[0]}, **Distance:** {entry[1]} km")
            else:
                st.write("No transport data available.")
            if food_data:
                st.subheader("🍽 Food Preference")
                st.write(f"**Preference:** {food_data[0]}")
            else:
                st.write("No food data available.")
    
    # Contact Us Page
    elif option == "Contact Us":
        st.header("📞 Contact Us")
        name = st.text_input("Your Name")
        message = st.text_area("Your Message")
        if st.button("Send Message"):
            st.success("Your message has been sent!")

    st.markdown("</div>", unsafe_allow_html=True)