import numpy as np
import pandas as pd

from d_config import (
    CAR_MASS, ZERO_SPEED_CRR, AIR_DENSITY, CDA, OUTER_WHEEL_RADIUS, AMBIENT_TEMP, GRAVITY,
)

def calculate_dx(start_speed, stop_speed, dt):
    '''
    Calculate step distance dx
    '''
    dx = dt * (start_speed + stop_speed) / 2

    return dx

    
def convert_domain_d2t(velocity_profile, route_df, dt):

    dx = calculate_dx(velocity_profile[:-1], velocity_profile[1:], dt)
    cum_distance = dx.cumsum() / 1000 # km

    nearest_cum_dist = pd.merge_asof(pd.DataFrame({'distance': cum_distance}), route_df['CumulativeDistance(km)'], left_on = 'distance',  right_on = 'CumulativeDistance(km)', direction = 'nearest')
    result = pd.merge(nearest_cum_dist, route_df, on = 'CumulativeDistance(km)')
    
    try:
        return np.array(result['Slope']), np.array(result['Lattitude']), np.array(result['Longitude'])
    except:
        return result
    
def calculate_power_req(speed, acceleration, slope,ws,wd):
    '''
    Calculate Power required by Car
    '''

    # Resistive torque on motor
    friction_torque = ZERO_SPEED_CRR * CAR_MASS * GRAVITY * np.cos(np.radians(slope)) * OUTER_WHEEL_RADIUS # Neglecting Dynamic Crr as it's order 1/100 th of static
    drag_torque = 0.5 * CDA * AIR_DENSITY * ((speed**2+ws**2-2*speed*ws*np.cos(np.radians(wd))))* OUTER_WHEEL_RADIUS
    # t = r_out * ((m * 9.81 * u1) + (0.5 * Cd * a * rho * (omega ** 2) * (r_out ** 2)))
    net_resistance_torque = friction_torque + drag_torque

    # Resistive power
    P_resistance = net_resistance_torque * (speed / OUTER_WHEEL_RADIUS)
    
    # Power due to windage, ohmic and eddy current losses
    # Finding winding temperature
    Tw_i = AMBIENT_TEMP
    while True:
        # B = 1.32 - 1.2 * 10**-3 * (AMBIENT_TEMP / 2 + Tw_i / 2 - 293)
        B = 1.6716 - 0.0006 * (AMBIENT_TEMP + Tw_i)  # magnetic remanence
        i = 0.561 * B * net_resistance_torque  # RMS phase current

        # R = 0.0575 * (1 + 0.0039 * (Tw_i - 293))
        resistance = 0.00022425 * Tw_i - 0.00820525  # resistance of windings
        
        P_ohmic = 3 * i ** 2 * resistance  # copper (ohmic) losses
        P_eddy = (9.602 * (10**-6) * ((B/OUTER_WHEEL_RADIUS) ** 2) / resistance) * (speed ** 2) # eddy current losses
        Tw = 0.455 * (P_ohmic + P_eddy) + AMBIENT_TEMP
    
        cond = np.abs(Tw - Tw_i) < 0.001
        if np.all(cond):
            break

        Tw_i = np.where(cond, Tw_i, Tw)
    # Final eta calculations
    P_windage = (speed ** 2) * (170.4 * (10**-6)) / (OUTER_WHEEL_RADIUS **2) # windage losses

    # Power required for acceleration
    P_acc = (CAR_MASS * acceleration + CAR_MASS * GRAVITY * np.sin(np.radians(slope))) * speed

    # Net power required
    P_net = P_resistance + P_windage + P_ohmic + P_eddy + P_acc
    # print("\u001b[31m",   CAR_MASS * GRAVITY * np.sin(np.radians(slope)) * speed, "\u001b[34m", acceleration, "\u001b[32m", slope, "\u001b[33m", speed, "\u001b[35m", P_acc, "\u001b[0m")
    return P_net.clip(0), P_resistance # Returning P_resistance for other calculations


