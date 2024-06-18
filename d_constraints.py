'''
Constraints, bounds and objective for the model
'''
# Import necessary modules

import numpy as np
import pandas as pd
from d_config import BATTERY_CAPACITY, DISCHARGE_CAP, MAX_V,  MAX_CURRENT, CAR_MASS, BUS_VOLTAGE, HR
from d_setting import DT, CONTROL_STOP_DURATION
from d_car_dynamics import calculate_dx, calculate_power_req, convert_domain_d2t
from d_solar import calculate_incident_solarpower
from d_offrace_solarcalc import calculate_energy
from d_helper_fns import find_control_stops

# Define constants
SAFE_BATTERY_LEVEL = BATTERY_CAPACITY * DISCHARGE_CAP
MAX_P = BUS_VOLTAGE * MAX_CURRENT

# Bounds for the velocity
def get_bounds(N):
    '''
    Velocity bounds throughout the race
    '''
    return ([(0, 0)] + [(0.01, MAX_V)] * (N-2) + [(0, 0)]) # Start and end velocity is zero

def objective(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array, cum_d):
    '''
    Maximize total distance travelled
    '''
    dx = calculate_dx(velocity_profile[:-1], velocity_profile[1:], dt)
    #Min_B, B_bar = battery_and_acc_constraint(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array)

    # return np.abs(3055 * 10**3 - cum_d - np.sum(dx)) 
    return - np.sum(dx) #+ np.max(-Min_B * 10 ** 16, 0) + np.max(-B_bar * 10 ** 12, 0)

def battery_and_acc_constraint(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array, cum_d, i, InitialBatteryCapacity, FinalBatteryCapacity):
    '''
    Battery safety and acceleration constraint
    '''
    dx = calculate_dx(velocity_profile[:-1], velocity_profile[1:], dt)
     
    slope_array, lattitude_array, longitude_array = convert_domain_d2t(velocity_profile, pd.DataFrame({'CumulativeDistance(km)': cum_d_array, 'Slope': slope_array, 'Lattitude': lattitude_array, 'Longitude': longitude_array }), dt)

    start_speeds, stop_speeds = velocity_profile[:-1], velocity_profile[1:]

    acceleration = (stop_speeds - start_speeds) / dt
    avg_speed = (start_speeds + stop_speeds) / 2

    # Find control stops
    cum_dtot = dx.cumsum() + cum_d
    cum_t = dt.cumsum() + i * DT
    control_stop_array =  find_control_stops((pd.DataFrame({'Cumulative Distance': cum_dtot, 'Time': cum_t})))

    # Solar correction
    indices = [np.searchsorted(dt.cumsum(), (t - i * DT), side='left') for t in control_stop_array]
    dt1_cumsum = np.copy(dt.cumsum())
    for idx in indices:
        if idx < len(dt1_cumsum):
            dt1_cumsum[idx:] += CONTROL_STOP_DURATION

    P_req, _ = calculate_power_req(avg_speed, acceleration, slope_array)
    # P_solar = calculate_incident_solarpower(dt1.cumsum() + timeoffset, lattitude_array, longitude_array)
    P_solar = calculate_incident_solarpower(dt1_cumsum, lattitude_array, longitude_array)

    energy_consumed = ((P_req - P_solar) * dt).cumsum()
    
    # Add energy gained through control stop
    for i,gt in enumerate(control_stop_array):
        t = int(gt % (DT))
        control_stop_E = calculate_energy(t, t + CONTROL_STOP_DURATION)
        energy_consumed[indices[i]:] -= control_stop_E

    energy_consumed = energy_consumed / HR # Wh

    battery_profile = InitialBatteryCapacity - energy_consumed - SAFE_BATTERY_LEVEL
    final_battery_lev = InitialBatteryCapacity - energy_consumed[-1] - FinalBatteryCapacity
    return np.min(battery_profile), (BATTERY_CAPACITY - SAFE_BATTERY_LEVEL) - np.max(battery_profile), MAX_P - np.max(P_req - P_solar), final_battery_lev # Ensure battery level bounds
    
# def v_end(velocity_profile, dt, cum_d):
#     dx = calculate_dx(velocity_profile[:-1], velocity_profile[1:], dt)
#     d = cum_d + np.sum(dx)
#     return (3050 * 10 **3 - d) * np.min(velocity_profile), np.min(velocity_profile)

