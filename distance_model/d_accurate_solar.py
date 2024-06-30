'''
Find solar power more accurately using time and location data
'''

# Import libraries
import numpy as np
from d_config import PANEL_AREA, PANEL_EFFICIENCY
import d_setting

# Constants
Gs = 1366  # Solar constant in W/m^2
_power_coeff = PANEL_EFFICIENCY * PANEL_AREA
DT = d_setting.DT

def find_day(date):
    '''
    Find day given date
    '''

    return date.timetuple().tm_yday

# Function to calculate B
def calculate_B(N):

    return (N - 1) * 360 / 365

# Function to calculate the equation of time (E)
def equation_of_time(B):

    return (229.2 * (0.000075 + 0.001868 * np.cos(np.radians(B)) - 0.032077 * np.sin(np.radians(B)) -
                    0.014615 * np.cos(np.radians(2 * B)) - 0.04089 * np.sin(np.radians(2 * B))))

# Function to calculate solar local time (T_s)
def solar_local_time(standard_time, longitude, Lst, E):

    return standard_time + (4 * (Lst - longitude) + E)

# Function to calculate hour angle (ω)
def hour_angle(Ts):

    return 15 * max(Ts, 12 - Ts)

# Function to calculate sun declination angle (δ)
def sun_declination_angle(N):
    
    return 23.45 * np.sin(np.radians(360 / 365 * (284 + N)))

# Function to calculate solar irradiance (G_b)
def solar_irradiance(Gs_prime, latitude, declination, hour_angle):
    latitude_rad = np.radians(latitude)
    declination_rad = np.radians(declination)
    hour_angle_rad = np.radians(hour_angle)
    return Gs_prime * (np.cos(latitude_rad) * np.cos(declination_rad) * np.sin(hour_angle_rad) + np.sin(latitude_rad) * np.sin(declination_rad))

# Main function to calculate incident solar power
def calculate_incident_solarpower(globaltime, latitude_array, longitude_array, Tz = 9.5):

    # Calculate the day of the year
    N = find_day(d_setting.Day)
    B = calculate_B(N)
    # Calculate the standard meridian
    Lst = Tz * 15

    # Calculate the equation of time
    E = equation_of_time(B)
    time = globaltime % DT
    # Calculate the standard time in hours (decimal)
    standard_time = (d_setting.RACE_START + time) / 3600
    # Calculate the solar local time for each point
    Ts = solar_local_time(standard_time, longitude_array, Lst, E)

    # Calculate the hour angle for each point
    omega = hour_angle(Ts)
    # Calculate the sun declination angle
    delta = sun_declination_angle(N)

    Gs1 = Gs(1 + 0.033 * np.cos(np.radians(360/ 365 * N)))
    Gs_prime = 0.7 * Gs1  # Adjusted solar constant for cloudy day

    # Calculate the solar irradiance for each point
    Is = solar_irradiance(Gs_prime, latitude_array, delta, omega)   

    P_solar = Is * _power_coeff

    return P_solar

# # Example usage
# if __name__ == "__main__":
#     # Example input
#     latitude_array = np.array([35.6895, 34.0522])  # Example latitudes
#     longitude_array = np.array([139.6917, -118.2437])  # Example longitudes
#     globaltime = 3600  # Example global time in seconds

#     # Calculate the incident solar power
#     power = calculate_incident_solarpower(globaltime, latitude_array, longitude_array)
#     print(f"Incident Solar Power: {power} W")

'''
Time offset from Coordinated Universal Time (UTC) across Stuart highway is 9hrs 30min with no Daylight Saving Time (DST) in the month of August.
'''