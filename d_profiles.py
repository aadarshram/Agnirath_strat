import numpy as np
import pandas as pd
from d_config import BATTERY_CAPACITY
import d_setting
from d_car_dynamics import calculate_power_req, convert_domain_d2t, calculate_dx
from d_solar import calculate_incident_solarpower

def extract_profiles(velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array,ws,wd):
    # convert data to time domain
    slope_array, lattitude_array, longitude_array = convert_domain_d2t(velocity_profile, pd.DataFrame({'CumulativeDistance(km)': cum_d_array, 'Slope': slope_array, 'Lattitude': lattitude_array, 'Longitude': longitude_array }), dt)

    start_speeds, stop_speeds = velocity_profile[:-1], velocity_profile[1:]
    
    avg_speed = (start_speeds + stop_speeds) / 2
    acceleration = (stop_speeds - start_speeds) / dt

    P_net,_ = calculate_power_req(avg_speed, acceleration, slope_array,ws,wd)
    P_solar = calculate_incident_solarpower(dt.cumsum() + d_setting.TimeOffset, lattitude_array, longitude_array)

    energy_consumption = P_net * dt /3600
    energy_gain = P_solar * dt /3600

    net_energy_profile = energy_consumption.cumsum() - energy_gain.cumsum()
    
    battery_profile = d_setting.InitialBatteryCapacity - net_energy_profile
    battery_profile = np.concatenate((np.array([d_setting.InitialBatteryCapacity]), battery_profile))

    battery_profile = battery_profile * 100 / (BATTERY_CAPACITY)
    dx = calculate_dx(start_speeds, stop_speeds, dt)

    # Matching shapes
    dt =  np.concatenate((np.array([0]), dt))
    energy_gain = np.concatenate((np.array([np.nan]), energy_gain))
    energy_consumption =  np.concatenate((np.array([np.nan]), energy_consumption,))
    acceleration = np.concatenate((np.array([np.nan]), acceleration,))
    dx = np.concatenate((np.array([0]), dx))
    
    return [
        dt.cumsum(),
        velocity_profile,
        acceleration,
        battery_profile,
        energy_consumption,
        energy_gain,
        dx,
    ]