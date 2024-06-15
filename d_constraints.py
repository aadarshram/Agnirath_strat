'''
Constraints, bounds and objective for the model
'''
# Import necessary modules

import numpy as np
import pandas as pd
from d_config import BATTERY_CAPACITY, DISCHARGE_CAP, MAX_V,  MAX_CURRENT, CAR_MASS, BUS_VOLTAGE
import d_setting
from d_car_dynamics import calculate_dx, calculate_power_req, convert_domain_d2t
from d_solar import calculate_incident_solarpower
from d_offrace_solarcalc import calculate_energy
from d_preprocess import find_control_stops

SAFE_BATTERY_LEVEL = BATTERY_CAPACITY * DISCHARGE_CAP
MAX_P = BUS_VOLTAGE * MAX_CURRENT

# Bounds for the velocity
def get_bounds(N):
    '''
    Velocity bounds throughout the race
    '''
    return ([(0, 0)] + [(0.01, MAX_V)] * (N-2) + [(0, 0)]) # Start and end velocity is zero

def objective(velocity_profile, dt
              ):
    '''
    Maximize total distance travelled
    '''
    dx = calculate_dx(velocity_profile[:-1], velocity_profile[1:], dt)
    #Min_B, B_bar = battery_and_acc_constraint(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array)
    # return np.abs(3055 * 10**3 - cum_d - np.sum(dx)) 
    return - np.sum(dx)*10**2

#+ np.max(-Min_B * 10 ** 16, 0) + np.max(-B_bar * 10 ** 12, 
def battery_and_acc_constraint(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array,ws_array,wd_array, cum_d, i):
    '''
    Battery safety and acceleration constraint
    '''

 
    
   
    dx = calculate_dx(velocity_profile[:-1], velocity_profile[1:], dt)
    cum_d1 = dx.cumsum() + cum_d
    cum_t = dt.cumsum() + i * (9 * 3600)
    dat = pd.DataFrame({'Cumulative Distance': cum_d1, 'Time': cum_t})
    control_stop_array =  find_control_stops(dat)

    slope_array, lattitude_array, longitude_array,ws,wd = convert_domain_d2t(velocity_profile, pd.DataFrame({'CumulativeDistance(km)': cum_d_array, 'Slope': slope_array, 'Lattitude': lattitude_array, 'Longitude': longitude_array,'wind speed':ws_array,'wind angle':wd_array }), dt)

    start_speeds, stop_speeds = velocity_profile[:-1], velocity_profile[1:]
    acceleration = (stop_speeds - start_speeds) / dt
    avg_speed = (start_speeds + stop_speeds) / 2
   

    P_total, P_resistance = calculate_power_req(avg_speed, acceleration, slope_array,ws,wd)
    P_solar = calculate_incident_solarpower(dt.cumsum() + d_setting.TimeOffset, lattitude_array, longitude_array)
    
    for gt in control_stop_array:
        t = gt % (9 * 3600)
        P_solar[t:] += calculate_energy(t, t + (0.5 * 3600))

    energy_consumed = ((P_total - P_solar) * dt).cumsum() / 3600 # Wh
    battery_profile = d_setting.InitialBatteryCapacity - energy_consumed - SAFE_BATTERY_LEVEL

    return   np.min(battery_profile)/np.abs(np.min(battery_profile)),(((BATTERY_CAPACITY - SAFE_BATTERY_LEVEL) - np.max(battery_profile)))/np.abs(((BATTERY_CAPACITY - SAFE_BATTERY_LEVEL) - np.max(battery_profile))), (MAX_P - np.max(P_total))# Ensure battery level never falls below safe level and exceeds total capacity 


def final_battery_constraint(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array,ws_array,wd_array):
    '''
    Finish recommended batery each day
    '''
    # Change the domain of slope, lat, lon to time
    
    slope_array, lattitude_array, longitude_array,ws,wd = convert_domain_d2t(velocity_profile, pd.DataFrame({'CumulativeDistance(km)': cum_d_array, 'Slope': slope_array, 'Lattitude': lattitude_array, 'Longitude': longitude_array,'wind speed':ws_array,'wind angle':wd_array }), dt)
    start_speeds, stop_speeds = velocity_profile[:-1], velocity_profile[1:]
    
    avg_speed = (start_speeds + stop_speeds) / 2
    acceleration = (stop_speeds - start_speeds) / dt

    P_net, _= calculate_power_req(avg_speed, acceleration, slope_array,ws,wd)
    P_solar = calculate_incident_solarpower(dt.cumsum() + d_setting.TimeOffset, lattitude_array, longitude_array)

    energy_consumption = ((P_net - P_solar) * dt).cumsum() / 3600
    final_battery_lev = d_setting.InitialBatteryCapacity - energy_consumption[-1] - d_setting.FinalBatteryCapacity
    return final_battery_lev, -final_battery_lev # Excess battery than recommended at each day = 0
    
def v_end(velocity_profile, dt, cum_d):
    dx = calculate_dx(velocity_profile[:-1], velocity_profile[1:], dt)
    d = cum_d + np.sum(dx)
    return (3050 * 10 **3 - d) * np.min(velocity_profile), np.min(velocity_profile)

