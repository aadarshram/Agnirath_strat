import numpy as np
import pandas as pd
from d_config import BATTERY_CAPACITY, HR,K
from d_setting import  CONTROL_STOP_DURATION,STEP,RACE_START,d_control_stops
from d_car_dynamics import calculate_power_req, convert_domain_d2t, calculate_dx
from d_solar import calculate_incident_solarpower
from d_offrace_solarcalc import calculate_energy
from d_helper_fns import find_control_stops

def extract_profiles(k,DT,velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array, cum_d, i, InitialBatteryCapacity, wind_speed, wind_direction):
    # convert data to time domain
    slope_array, lattitude_array, longitude_array, wind_speed_array, wind_direction_array = convert_domain_d2t(velocity_profile, pd.DataFrame({'CumulativeDistance(km)': cum_d_array, 'Slope': slope_array, 'Lattitude': lattitude_array, 'Longitude': longitude_array,'WindSpeed(m/s)':wind_speed,'Winddirection(frmnorth)':wind_direction }), dt)

    start_speeds, stop_speeds = velocity_profile[:-1], velocity_profile[1:]
    
    avg_speed = (start_speeds + stop_speeds) / 2
    acceleration = (stop_speeds - start_speeds) / dt


    dx = calculate_dx(start_speeds, stop_speeds, dt)

   

   # Find control stops
    cum_dtot = dx.cumsum() + cum_d
    cum_dtot=cum_dtot/ K
    cum_t = dt.cumsum() + i * DT
    print(cum_t[:10])
    dfx=pd.DataFrame({'Cumulative Distance': cum_dtot, 'Time': cum_t})
    
    control_stop_array =  find_control_stops((dfx))
    # control_stop_array = cum_t[np.searchsorted(cum_dtot, dis, side='right') for dis in d_control_stops]
    # control_stop_array=[i for i in control_stop_array if i!=0 or i!= len(cum_dtot)-1]

    #Solar correction
    indices = [np.searchsorted(dt.cumsum(), t% DT, side='right') for t in control_stop_array ]
    print("control stops my igga",control_stop_array)
    print("control-spto",indices)
    dt1 = np.copy(dt)
    for idx in indices:
        if idx < len(dt1) and idx!=0:
            dt1[idx] += CONTROL_STOP_DURATION


    P_req, _ = calculate_power_req(avg_speed, acceleration, slope_array, wind_speed_array, wind_direction_array)
    P_solar = calculate_incident_solarpower(dt1.cumsum(), lattitude_array, longitude_array)

    energy_consumption = P_req * dt / HR # Wh

    #energy_consumption = energy_consumption.cumsum()
    energy_gain = P_solar * dt 

    energy_gain1 = energy_gain
    energy_gain = energy_gain / HR 
    #Add energy gained through control stop
    for i,gt in enumerate(control_stop_array):
        print(i,indices[i])
        t = int(gt % (DT))
        control_stop_E = calculate_energy(t, t + CONTROL_STOP_DURATION)
        print(control_stop_E)
        print("en",energy_gain[indices[i]])
        energy_gain[indices[i]] += control_stop_E
        print("en1",energy_gain[indices[i]])
    # Wh
    
    net_energy_profile = energy_consumption.cumsum() - energy_gain.cumsum()

    battery_profile = InitialBatteryCapacity - net_energy_profile
    battery_profile = np.concatenate((np.array([InitialBatteryCapacity]), battery_profile))

    battery_profile = battery_profile * 100 / (BATTERY_CAPACITY)

    # Matching shapes
    dt =  np.concatenate((np.array([0]), dt))
    energy_gain = np.concatenate((np.array([np.nan]), energy_gain))
    #energy_gain = np.concatenate((np.array([np.nan]), energy_gain))
    energy_gain1 = np.concatenate((np.array([np.nan]), energy_gain1))
    energy_consumption =  np.concatenate((np.array([np.nan]), energy_consumption,))
    acceleration = np.concatenate((np.array([np.nan]), acceleration,))
    dx = np.concatenate((np.array([0]), dx))
    
    return [
        dt.cumsum(),
        velocity_profile,
        acceleration,
        battery_profile,
        energy_consumption,
        energy_gain1/HR,
        dx,
    ]