import streamlit as st
import sqlite3
from db import create_table, insert_data

# Ensure the database table exists
create_table()

# --- Navigation Bar ---
menu = ["Home", "Register for Event", "Transportation Data", "Food Details", "Contact Us"]
selected = st.radio("", menu, horizontal=True)

# --- Event Registration ---
if selected == "Register for Event":
    st.title("Event Registration")
    name = st.text_input("Full Name")
    origin = st.text_input("Where are you traveling from?")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    
    if st.button("Register"):
        if name and origin and email and phone:
            st.session_state.registered = True
            st.session_state.name = name
            st.session_state.origin = origin
            st.success("Registration successful! You can now enter transportation data.")
        else:
            st.error("Please fill in all fields.")

# --- Home Page ---
elif selected == "Home":
    st.title("Welcome to the Emissions Calculator")
    st.write("This tool helps you calculate transportation and food-related emissions.")

# --- Transportation Data Page ---
elif selected == "Transportation Data":
    if not st.session_state.get("registered", False):
        st.warning("Please register for the event first.")
    else:
        st.title("Transportation Emissions Calculator")
        transport_mode = st.selectbox("Select transport mode", [
            "3-Wheeler CNG", "2-Wheeler", "4W Petrol", "4W CNG", "BUS", "Electric 2-Wheeler", "Electric 4-Wheeler"
        ])
        distance = st.number_input("Enter the distance traveled (in km)", min_value=0.1, step=0.1)

        def calculate_emissions(transport_mode, distance):
            EMISSION_FACTORS = {
                "3-Wheeler CNG": 0.10768,
                "2-Wheeler": 0.04911,
                "4W Petrol": 0.187421,
                "4W CNG": 0.068,
                "BUS": 0.015161,
                "Electric 2-Wheeler": 0.0319,
                "Electric 4-Wheeler": 0.1277
            }
            return EMISSION_FACTORS.get(transport_mode, 0) * distance

        if st.button("Calculate Emissions"):
            emissions = calculate_emissions(transport_mode, distance)
            if emissions:
                st.write(f"Emissions for {transport_mode} for {distance} km: {emissions:.4f} kg CO2")
                travel_date = st.date_input("Select travel date").strftime("%Y-%m-%d")
                insert_data(st.session_state.name, transport_mode, "Distance", distance, 1, travel_date, emissions)
                st.success("Data saved successfully!")
            else:
                st.error("Invalid transport mode selected.")

# --- Food Details Page ---
elif selected == "Food Details":
    st.title("Food Emissions Data")
    st.write("This section will track emissions related to food consumption.")

# --- Contact Us Page ---
elif selected == "Contact Us":
    st.title("Contact Us")
    st.write("For any queries, please reach out to us via email at: support@example.com")
