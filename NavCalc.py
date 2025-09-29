import math


def compute_altitude_azimuth(latitude, declination,local_hour_angle):
    """    Computes the altitude and azimuth of a celestial body.
   
    Parameters:
    latitude (float): Observer's latitude in degrees (-90 to 90).
    declination (float): Celestial body's declination in degrees (-90 to 90).
    local_hour_angle (float): Celestial body's local hour angle in degrees (0 to 360).


    Returns:
    tuple: Altitude (Hc) and azimuth (Z) in degrees."""

    # Convert degrees to radians
    
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    local_h_rad = math.radians(local_hour_angle)


    # Compute altitude (Hc)
    
    sin_alt = (math.sin(lat_rad) * math.sin(dec_rad) +
               math.cos(lat_rad) * math.cos(dec_rad) * math.cos(local_h_rad))
    sin_alt = max(-1.0, min(1.0, sin_alt))  # Clamp value to avoid domain errors
    # Ensure sin_alt is within the valid range for arcsin           
    altitude = math.degrees(math.asin(sin_alt))


    # Compute azimuth (Z)
    
    cos_az = (math.sin(dec_rad) - math.sin(lat_rad) * math.sin(math.radians(altitude))) / (
              math.cos(lat_rad) * math.cos(math.radians(altitude)))
    cos_az = max(-1.0, min(1.0, cos_az))  # Clamp value to avoid domain errors
    # Ensure cos_az is within the valid range for arccos        
    azimuth = math.degrees(math.acos(cos_az))


    # Determine correct quadrant for azimuth
    
    if math.sin(local_h_rad) > 0:  # Hour angle positive
        azimuth = 360 - azimuth


    return altitude, azimuth


# Example usage


if __name__ == "__main__":
   
    # Input values
   
    latitude = float(input("Enter observer's latitude (degrees): "))
    declination = float(input("Enter celestial body's declination (degrees): "))
    local_hour_angle = float(input("Enter celestial body's local hour angle (degrees): "))


    # Calculate altitude and azimuth
   
    alt, az = compute_altitude_azimuth(latitude, declination, local_hour_angle)


    # Output results

    print(f"Altitude (Hc): {alt:.2f} degrees")
    print(f"Azimuth (Z): {az:.2f} degrees")