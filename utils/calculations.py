EMISSION_FACTORS = {
    "3-Wheeler CNG": 0.10768,
    "2-Wheeler (Petrol)": 0.04911,
    "4-Wheeler (Petrol)": 0.187421,
    "4-Wheeler (CNG)": 0.068,
    "Bus (Diesel)": 0.015161,
}

ELECTRIC_CONSUMPTION = {
    "Electric 2-Wheeler": 0.0319,
    "Electric 4-Wheeler": 0.1277,
}

def calculate_emissions(transport_mode, input_type, value, frequency):
    """Calculate emissions based on transport mode."""
    if transport_mode in EMISSION_FACTORS:
        emission_factor = EMISSION_FACTORS[transport_mode]
        if input_type == "Time":
            average_speed = 40  # Assuming 40 km/h
            distance = (value / 60) * average_speed
        else:
            distance = value
        total_emissions = distance * emission_factor * frequency
        return total_emissions
    elif transport_mode in ELECTRIC_CONSUMPTION:
        consumption = ELECTRIC_CONSUMPTION[transport_mode]
        if input_type == "Time":
            average_speed = 40
            distance = (value / 60) * average_speed
        else:
            distance = value
        total_energy = distance * consumption * frequency
        return total_energy
    return None
