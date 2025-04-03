import streamlit as st
import sqlite3
import time
import qrcode
from io import BytesIO
from db import init_db, store_transport_data, store_food_data

# Initialize the database
init_db()

# Define the URL for your app
app_url = "https://transport-food-data-collection-pzksckdswfrpqjusoctcx5.streamlit.app/"

# Generate QR code
qr = qrcode.make(app_url)
buf = BytesIO()
qr.save(buf, format="PNG")
buf.seek(0)

# Session management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(time.time())

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=60)
    st.title("🚀 Menu")
    option = st.radio("Go to", ["Home", "Scan QR", "Transport", "Food", "View Data", "Contact Us"])

# Main Container
with st.container():
    st.markdown("<div style='max-width: 360px; margin: auto;'>", unsafe_allow_html=True)
    
    if option == "Home":
        st.header("🌍 Welcome to the Event Emissions Data Collector!")
        st.write("Track your carbon footprint from transportation and food choices.")
        st.subheader("📌 What You Can Do Here:")
        st.markdown(""" 
        - ✅ Enter Transportation Details
        - ✅ Choose Your Food Preference
        - ✅ View Your Carbon Impact
        """)

    elif option == "Scan QR":
        st.header("📱 Scan this QR Code")
        st.image(buf, caption="Scan me!", use_column_width=True)

    elif option == "Transport":
        st.header("🚗 Transport Details")
        selected_modes = st.multiselect(
            "Select Transport Modes", 
            ["3-Wheeler CNG", "2-Wheeler", "4W Petrol", "4W CNG", "BUS", 
             "Electric 2-Wheeler", "Electric 4-Wheeler", "Local Train (Electricity)", "Air ways"]
        )
        distances = {
            mode: st.number_input(
                f"Distance traveled by {mode} (km)", 
                min_value=1, max_value=5000, step=1, key=mode
            ) for mode in selected_modes
        }
        if st.button("Submit Transport Data"):
            for mode, distance in distances.items():
                store_transport_data(st.session_state.session_id, mode, distance)
            st.success("✅ Transport details submitted!")

    elif option == "Food":
        st.header("🍽 Select Your Food Preferences")
        
        # Dietary Pattern Selection
        dietary_pattern = st.radio(
            "Select Your Dietary Pattern", 
            ["Vegetarian Diet", "Vegan Diet", "Non-Vegetarian Diet (with Fish)", 
             "Non-Vegetarian Diet (with Eggs)", "Non-Vegetarian Diet (with Mutton)", 
             "Non-Vegetarian Diet (with Chicken)"]
        )
        
        # Number of meals slider
        num_meals = st.slider("Number of meals consumed", 1, 5, 2)
        
        # Food selection based on diet
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Main Course")
            if "Vegetarian" in dietary_pattern:
                main_options = ["Chapatti", "Rice", "Pulses", "Vegetable Curry", "Paneer Dish"]
            elif "Vegan" in dietary_pattern:
                main_options = ["Chapatti", "Rice", "Pulses", "Vegetable Curry", "Tofu Dish"]
            elif "Fish" in dietary_pattern:
                main_options = ["Chapatti", "Rice", "Pulses", "Grilled Fish", "Vegetable Curry"]
            elif "Eggs" in dietary_pattern:
                main_options = ["Chapatti", "Rice", "Pulses", "Egg Curry", "Vegetable Curry"]
            else:  # Chicken/Mutton
                main_options = ["Chapatti", "Rice", "Pulses", "Chicken Curry", "Vegetable Curry"]
            
            main_course = st.multiselect("Select main course items", main_options)
        
        with col2:
            st.subheader("Extras")
            extras = st.multiselect("Select additional items", 
                                  ["Salad", "Soup", "Yogurt", "Pickle", "Papad"])
        
        st.subheader("Sweets")
        sweets = st.multiselect("Select desserts", 
                              ["Gulab Jamun", "Rasgulla", "Kheer", "Jalebi", "Fruit"])
        
        # Combine selections
        all_selections = {
            "Dietary Pattern": dietary_pattern,
            "Number of Meals": num_meals,
            "Main Course": main_course,
            "Extras": extras,
            "Sweets": sweets
        }
        
        if st.button("Save Food Preferences"):
            if main_course or extras or sweets:  # At least one selection
                for category, items in all_selections.items():
                    if items and category != "Number of Meals":
                        store_food_data(
                            st.session_state.session_id, 
                            f"{dietary_pattern} - {category}", 
                            items if isinstance(items, list) else [items]
                        )
                # Store number of meals separately
                store_food_data(
                    st.session_state.session_id,
                    "Meal Information",
                    [f"Number of meals: {num_meals}"]
                )
                st.success("✅ Food preferences saved!")
            else:
                st.warning("⚠️ Please select at least one food item.")

    elif option == "View Data":
        st.header("📊 Your Submitted Data")
        conn = sqlite3.connect('data/emissions.db')
        c = conn.cursor()
        
        # Transport data
        c.execute("SELECT transport_mode, distance FROM transport_data WHERE session_id = ?", 
                 (st.session_state.session_id,))
        transport_data = c.fetchall()
        
        # Food data
        c.execute("SELECT food_item FROM food_choices WHERE session_id = ?", 
                 (st.session_state.session_id,))
        food_data = c.fetchall()
        
        conn.close()
        
        if transport_data:
            st.subheader("🚗 Transport Details")
            for mode, distance in transport_data:
                st.write(f"- {mode}: {distance} km")
        
        if food_data:
            st.subheader("🍽 Food Preferences")
            current_category = ""
            for item in food_data:
                item = item[0]
                if " - " in item:
                    category = item.split(" - ")[1]
                    if category != current_category:
                        st.write(f"**{category}**")
                        current_category = category
                    st.write(f"- {item.split(' - ')[-1]}")
                else:
                    st.write(item)

    elif option == "Contact Us":
        st.header("📞 Contact Us")
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            message = st.text_area("Your Message")
            if st.form_submit_button("Send Message"):
                st.success("✅ Your message has been sent!")

    st.markdown("</div>", unsafe_allow_html=True)
