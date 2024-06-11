'''
Constraints, bounds and objective for the model
'''
# Import necessary modules

import numpy as np
import pandas as pd
from d_config import BATTERY_CAPACITY, DISCHARGE_CAP, MAX_V,  MAX_CURRENT, CAR_MASS
import d_setting
from d_car_dynamics import calculate_dx, calculate_power_req, convert_domain_d2t
from d_solar import calculate_incident_solarpower

SAFE_BATTERY_LEVEL = BATTERY_CAPACITY * DISCHARGE_CAP
MAX_P = MAX_V * MAX_CURRENT

# Bounds for the velocity
def get_bounds(N):
    '''
    Velocity bounds throughout the race
    '''
    return ([(0, 0)] + [(0.01, MAX_V)] * (N-2) + [(0, 0)]) # Start and end velocity is zero

def objective(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array
              ):
    '''
    Maximize total distance travelled
    '''
    dx = calculate_dx(velocity_profile[:-1], velocity_profile[1:], dt)
    Min_B, B_bar = battery_and_acc_constraint(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array)
    return (- np.sum(dx)) + np.max(-Min_B * 10 ** 16, 0) + np.max(-B_bar * 10 ** 12, 0)

def battery_and_acc_constraint(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array):
    '''
    Battery safety and acceleration constraint
    '''

    slope_array, lattitude_array, longitude_array = convert_domain_d2t(velocity_profile, pd.DataFrame({'CumulativeDistance(km)': cum_d_array, 'Slope': slope_array, 'Lattitude': lattitude_array, 'Longitude': longitude_array }), dt)

    start_speeds, stop_speeds = velocity_profile[:-1], velocity_profile[1:]
    acceleration = (stop_speeds - start_speeds) / dt
    avg_speed = (start_speeds + stop_speeds) / 2

    P_total, P_resistance = calculate_power_req(avg_speed, acceleration, slope_array)
    P_solar = calculate_incident_solarpower(dt.cumsum() + d_setting.TimeOffset, lattitude_array, longitude_array)
    energy_consumed = ((P_total - P_solar) * dt).cumsum() / 3600
    battery_profile = d_setting.InitialBatteryCapacity - energy_consumed - SAFE_BATTERY_LEVEL

    return np.min(battery_profile), (BATTERY_CAPACITY - SAFE_BATTERY_LEVEL) - np.max(battery_profile)
#np.max((P_resistance.clip(0) / (CAR_MASS * avg_speed)) - acceleration) # Ensure battery level never falls below safe level and acceleration ??

#MAX_P - np.max(P_total)

def final_battery_constraint(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array):
    '''
    Finish recommended batery each day
    '''
    # Change the domain of slope, lat, lon to time

    slope_array, lattitude_array, longitude_array = convert_domain_d2t(velocity_profile, pd.DataFrame({'CumulativeDistance(km)': cum_d_array, 'Slope': slope_array, 'Lattitude': lattitude_array, 'Longitude': longitude_array }), dt)
    start_speeds, stop_speeds = velocity_profile[:-1], velocity_profile[1:]
    
    avg_speed = (start_speeds + stop_speeds) / 2
    acceleration = (stop_speeds - start_speeds) / dt

    P_net, _= calculate_power_req(avg_speed, acceleration, slope_array)
    P_solar = calculate_incident_solarpower(dt.cumsum() + d_setting.TimeOffset, lattitude_array, longitude_array)

    energy_consumption = ((P_net - P_solar) * dt).cumsum() / 3600
    final_battery_lev = d_setting.InitialBatteryCapacity - energy_consumption[-1] - d_setting.FinalBatteryCapacity
    return final_battery_lev, -final_battery_lev # Excess battery than recommended at each day = 0
    


