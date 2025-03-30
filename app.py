import streamlit as st
import sqlite3
import time
from db import init_db, register_user, authenticate_user, store_transport_data, get_logged_in_user_id, calculate_emissions, update_password

# Initialize the database
init_db()

# Set up session state for login management
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'reset_password' not in st.session_state:
    st.session_state.reset_password = False

# Sidebar Navigation (Collapsible)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=60)
    st.title("🚀 Menu")
    
    option = st.radio("Go to", ["Home", "Register/Login", "Transport", "Food", "View Data", "Contact Us"])
    
    if st.session_state.user_id:
        if st.button("Logout"):
            st.session_state.user_id = None
            st.success("✅ Logged out successfully!")
            time.sleep(1)
            st.rerun()

# Centered container for mobile-friendly display
with st.container():
    st.markdown("<div style='max-width: 360px; margin: auto;'>", unsafe_allow_html=True)

    # Home Page
    if option == "Home":
       st.header("🌍 Welcome to the Event Emissions Data Collector!")
       st.write(
        "We developed a dashboard using Streamlit that displays **Scope 1, 2, and 3 emissions** for an event. "
        "To support this, this web application collects data from event attendees to estimate emissions more accurately."
    )

       st.subheader("📌 What You Can Do Here:")
       st.markdown("""
    - ✅ **Register & Login** to access the platform.
    - ✅ **Enter Transportation Details** – Specify your mode of travel (Car, Train, Airplane, etc.) and distance traveled.
    - ✅ **Choose Your Food Preference** – Select from Veg, Non-Veg, or Vegan options.
    
    This data helps event managers estimate total emissions from attendee travel and food consumption.
    """)

       st.write("Use the sidebar to navigate: **Home, Register, Login, Transportation, Food, and Contact Us.**")

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
                st.rerun()
        
        if st.session_state.reset_password:
            st.header("🔄 Reset Password")
            email = st.text_input("Enter your registered email")
            new_password = st.text_input("New Password", type="password")
            
            if st.button("Reset Password"):
                success = update_password(email, new_password)
                if success:
                    st.success("✅ Password reset successfully! Please login.")
                    st.session_state.reset_password = False
                    st.rerun()
                else:
                    st.error("⚠️ Email not found.")

    # Transport Page (Restricted)
    elif option == "Transport":
        if not st.session_state.user_id:
            st.warning("⚠️ Please Register/Login first.")
        else:
            st.header("🚗 Transport Emissions")
            transport_mode = st.radio("Select Transport Mode", ["Car", "Bike", "Bus", "Walking", "Airplane", "Train"])
            distance = st.slider("Distance traveled (km)", 1, 5000, 10)
            
            if st.button("Calculate Emissions"):
                emissions = calculate_emissions(transport_mode, distance)
                store_transport_data(st.session_state.user_id, transport_mode, distance, emissions)
                st.write(f"Your emissions: {emissions} kg CO2")

    # Food Preferences Page (Restricted)
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
                c.execute("INSERT INTO food_preferences (user_id, food_choice) VALUES (?, ?)", (st.session_state.user_id, food_choice))
                conn.commit()
                conn.close()
                st.success("✅ Food preference saved!")

    # View Data Page (Restricted)
    elif option == "View Data":
        if not st.session_state.user_id:
            st.warning("⚠️ Please Register/Login first.")
        else:
            st.header("Your Transport and Food Data")
            conn = sqlite3.connect('data/emissions.db')
            c = conn.cursor()
            c.execute("SELECT transport_mode, distance, emissions FROM transport_data WHERE user_id = ?", (st.session_state.user_id,))
            transport_data = c.fetchall()
            c.execute("SELECT food_choice FROM food_preferences WHERE user_id = ?", (st.session_state.user_id,))
            food_data = c.fetchone()
            conn.close()
            
            if transport_data:
                for entry in transport_data:
                    st.write(f"Mode: {entry[0]}, Distance: {entry[1]} km, Emissions: {entry[2]} kg CO2")
            else:
                st.write("No transport data available.")
            
            if food_data:
                st.write(f"Food Preference: {food_data[0]}")
            else:
                st.write("No food data available.")

    # Contact Us Page
    elif option == "Contact Us":
        st.header("📞 Contact Us")
        name = st.text_input("Your Name")
        message = st.text_area("Your Message")
        st.button("Send Message")
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close the centered div
