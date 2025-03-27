import streamlit as st
import sqlite3
from db import create_table, insert_data  # Importing functions from db.py

# Ensure the table exists
create_table()

# Set up the page layout and title
st.set_page_config(page_title="Transportation Emissions Calculator", layout="wide")
st.title("Transportation Emissions Calculator")

# Step 1: Choose transport mode (example: dropdown)
transport_mode = st.selectbox("Select transport mode", ["3-Wheeler CNG", "2-Wheeler", "4W Petrol", "4W CNG", "BUS", "Electric 2-Wheeler", "Electric 4-Wheeler"])

# Step 2: Get the distance for the transport mode (popup when clicking on distance)
distance = st.number_input("Enter the distance traveled (in km)", min_value=0.1, step=0.1)

# Step 3: Calculate emissions for the selected transport mode
def calculate_emissions(transport_mode, distance):
    # Define emission factors for different transport modes
    EMISSION_FACTORS = {
        "3-Wheeler CNG": 0.10768,
        "2-Wheeler": 0.04911,
        "4W Petrol": 0.187421,
        "4W CNG": 0.068,
        "BUS": 0.015161,
        "Electric 2-Wheeler": 0.0319,
        "Electric 4-Wheeler": 0.1277
    }
    
    # Get the emission factor for the selected transport mode
    emission_factor = EMISSION_FACTORS.get(transport_mode)
    
    if emission_factor:
        emissions = emission_factor * distance
        return emissions
    else:
        return None

# Step 4: Display the emissions calculation
if st.button("Calculate Emissions"):
    emissions = calculate_emissions(transport_mode, distance)
    
    if emissions:
        st.write(f"Emissions for {transport_mode} for {distance} km: {emissions:.4f} kg CO2")
        
        # Step 5: Save the data to the database
        name = "Event Attendee"  # You can replace this with user input if needed
        input_type = "Distance"
        value = distance
        frequency = 1  # For now, set to 1 (you can modify this if needed)
        travel_date = st.date_input("Select travel date").strftime("%Y-%m-%d")
        
        # Insert data into the database
        insert_data(name, transport_mode, input_type, value, frequency, travel_date, emissions)
        st.success("Data saved to the database successfully!")
    else:
        st.error("Invalid transport mode selected.")

# Optional: Display the data from the database (for debugging or testing purposes)
if st.checkbox("Show saved data"):
    conn = sqlite3.connect("data/emissions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transport_emissions")
    rows = cursor.fetchall()
    
    if rows:
        st.write("Saved Data:")
        for row in rows:
            st.write(row)
    else:
        st.write("No data found in the database.")
    conn.close()
