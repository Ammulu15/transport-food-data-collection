import streamlit as st
import sqlite3
import time
import qrcode
from io import BytesIO
from db import init_db, store_transport_data, store_food_data  # (Ensure store_message is also defined if needed)

# Initialize the database
init_db()

# Define the URL for your app (replace with your actual app URL)
app_url = "https://transport-food-data-collection-pzksckdswfrpqjusoctcx5.streamlit.app/"

# Generate the QR code for your app URL
qr = qrcode.make(app_url)
buf = BytesIO()
qr.save(buf, format="PNG")
buf.seek(0)

# Create a session ID for each user (used to store data separately)
if "session_id" not in st.session_state:
    # Using time.time() to generate a session id; consider uuid.uuid4() for randomness.
    st.session_state.session_id = str(time.time())
    print(f"[DEBUG] New session ID generated: {st.session_state.session_id}")
else:
    print(f"[DEBUG] Using existing session ID: {st.session_state.session_id}")

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=60)
    st.title("🚀 Menu")
    option = st.radio("Go to", ["Home", "Scan QR", "Transport", "Food", "View Data", "Contact Us"])

# Main Container for Display
with st.container():
    st.markdown("<div style='max-width: 360px; margin: auto;'>", unsafe_allow_html=True)
    
    # Home Page
    if option == "Home":
        st.header("🌍 Welcome to the Event Emissions Data Collector!")
        st.write(
            "We developed a dashboard using Streamlit that displays **Scope 1, 2, and 3 emissions** for an event. "
            "This web application allows event attendees to submit transportation and food data."
        )
        st.subheader("📌 What You Can Do Here:")
        st.markdown(""" 
        - ✅ **Enter Transportation Details** – Specify your mode of travel and distance traveled.
        - ✅ **Choose Your Food Preference** – Select from Veg, Non-Veg, or Vegan options.
        """)
        st.write("Use the sidebar to navigate.")

    # QR Code Page
    elif option == "Scan QR":
        st.header("📱 Scan this QR Code")
        st.write("Scan this QR code to open the app on your mobile device.")
        st.image(buf, caption="Scan me!", use_column_width=True)

    # Transport Data Collection
    elif option == "Transport":
        st.header("🚗 Transport Details")
        st.write("Select the transport modes you used and provide the distance traveled.")
        selected_modes = st.multiselect("Select Transport Modes", 
                                        ["3-Wheeler CNG", "2-Wheeler", "4W Petrol", "4W CNG", "BUS", 
                                         "Electric 2-Wheeler", "Electric 4-Wheeler", "Local Train (Electricity)", "Air ways"])
        distances = {mode: st.number_input(f"Distance traveled by {mode} (km)", 
                                           min_value=1, max_value=5000, step=1, key=mode) 
                     for mode in selected_modes}
        if st.button("Submit Transport Data"):
            for mode, distance in distances.items():
                store_transport_data(st.session_state.session_id, mode, distance)
            st.success("✅ Transport details submitted!")
    # Food Preferences Data Collection
    elif option == "Food":
        st.header("🍽 Select Your Food Preferences")

        # Dietary Pattern Selection
        dietary_pattern = st.radio("Select Your Dietary Pattern", 
        ["Vegetarian Diet",'Vegan Diet','Non-Vegetarian Diet (with Fish)','Non Vegetarian Diet (with Eggs)', "Non-Vegetarian Diet (with Mutton)", "Non-Vegetarian Diet (with Chicken)",])

        # Breakfast Selection
        breakfast = st.multiselect("Choose your Breakfast options", 
                               ["Milk", "Eggs", "Idli with Sambar", "Poha with Vegetables", 
                                "Paratha with Curd", "Upma", "Omelette with Toast", 
                                "Masala Dosa", "Puri Bhaji", "Aloo Paratha", "Medu Vada", 
                                "Sabudana Khichdi", "Dhokla", "Chole Bhature", 
                                "Besan Cheela", "Pongal"])

        # Lunch Selection
        lunch = st.multiselect("Choose your Lunch options", 
                           ["Chapatti (Wheat Bread)", "Rice", "Pulses (Lentils)", "Vegetables (Cauliflower, Brinjal)", 
                            "Dal Tadka", "Paneer Butter Masala", "Mutton Curry", "Chicken Curry", "Fish Fry", 
                            "Sambhar", "Curd Rice", "Mixed Vegetable Curry"])

        # Dinner Selection
        dinner = st.multiselect("Choose your Dinner options", 
                            ["Chapatti (Wheat Bread)", "Rice", "Pulses (Lentils)", "Vegetables (Cauliflower, Brinjal)", 
                             "Khichdi", "Daal Rice", "Grilled Fish", "Grilled Chicken", "Tofu Stir Fry", 
                             "Egg Bhurji", "Soup", "Salad"])

        # Salads and Sweets remain unchanged
        salad_selection = st.multiselect("Choose your Salads", 
                                     ["Kachumber Salad", "Sprouted Moong Salad", "Cucumber Raita Salad", 
                                      "Tomato Onion Salad", "Carrot and Cabbage Salad"])

        sweets_selection = st.multiselect("Choose your Sweets", 
                                      ["Gulab Jamun", "Rasgulla", "Kheer", "Jalebi", "Kaju Katli", 
                                       "Barfi", "Halwa (Carrot or Bottle Gourd)", "Laddu"])

        banana_selection = ["Single Banana"]  # This is a fixed option
    
        # Combine all meal selections
        user_choices = {
        "Breakfast": breakfast,
        "Lunch": lunch,
        "Dinner": dinner,
        "Salads": salad_selection,
        "Sweets": sweets_selection,
        "Others": banana_selection}

        # Save to database
        if st.button("Save Food Preferences"):
            if any(user_choices.values()):  # Check if user made at least one selection
                for meal_type, items in user_choices.items():
                    if items:
                        store_food_data(st.session_state.session_id, f"{dietary_pattern} - {meal_type}", items)
                st.success("✅ Food preferences saved!")
            else:
                st.warning("⚠️ Please select at least one food option.")
    


    # View Submitted Data
    elif option == "View Data":
        st.header("📊 Your Submitted Data")
        conn = sqlite3.connect('data/emissions.db')
        c = conn.cursor()
        
        c.execute("SELECT transport_mode, distance FROM transport_data WHERE session_id = ?", 
                  (st.session_state.session_id,))
        transport_data = c.fetchall()
        c.execute("SELECT food_item FROM food_choices WHERE session_id = ?", 
                  (st.session_state.session_id,))
        food_data = c.fetchall()
        conn.close()
        
        if transport_data:
            st.subheader("🚗 Transport Details")
            for entry in transport_data:
                st.write(f"**Mode:** {entry[0]}, **Distance:** {entry[1]} km")
        else:
            st.write("No transport data available.")
        
        if food_data:
            st.subheader("🍽 Food Preference")
            for food in food_data:
                st.write(f"**Preference:** {food[0]}")
        else:
            st.write("No food data available.")

    # Contact Us Page
    elif option == "Contact Us":
        st.header("📞 Contact Us")
        name = st.text_input("Your Name")
        message = st.text_area("Your Message")
        if st.button("Send Message"):
            # Uncomment the following line if store_message is defined in db.py and imported
            # store_message(name, message)
            st.success("✅ Your message has been sent!")

    st.markdown("</div>", unsafe_allow_html=True)
