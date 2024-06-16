'''
Set day-wise model parameters
'''

# Import necessary modules

from d_config import BATTERY_CAPACITY, KM
import pandas as pd

# Model Settings

ModelMethod = "COBYLA"
InitialGuessVelocity = 20 # m/s (Total average speed)

RunforDays = 5
# Day-wise race time

RACE_START = 8 * 3600  # 8:00 am
RACE_END = 17 * 3600  # 5:00 pm
RACE_DISTANCE = 3037 * KM
CONTROL_STOP_DURATION = int(0.5 * 3600) # s
DT = RACE_END - RACE_START - 2 * CONTROL_STOP_DURATION

# Control stops
d_control_stops = [322., 588., 987., 1210., 1493., 1766., 2178., 2432., 2720.] # 2023 data

# Resolution 
STEP = 300 # s

# Average velocity

AVG_V = RACE_DISTANCE / (DT * RunforDays)

# Final Battery optimisation way-points
discharge_list= [60, 60, 40, 40, 0]

# route_df = pd.read_csv("raw_route_data.csv")
route_df = pd.read_csv("processed_route_data.csv")


def set_day(present_battery_cent, i, time_offset = 0):
    '''
    Set day-wise parameters
    '''

    global InitialBatteryCapacity
    global TimeOffset
    
    TimeOffset = time_offset
    # DISCHARGE_CAP = discharge_list[i]/100
    PresentBatteryCapacity = (present_battery_cent / 100) * BATTERY_CAPACITY
    InitialBatteryCapacity = PresentBatteryCapacity # Wh
    FinalBatteryCapacity = (discharge_list[i] / 100) * BATTERY_CAPACITY
    #     InitialBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no] # Wh
#     FinalBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no+1]  # Wh
#     route_df = pd.read_csv("raw_route_data.csv").iloc[DF_WayPoints[index_no]: DF_WayPoints[index_no+1]]
    return InitialBatteryCapacity, TimeOffset, FinalBatteryCapacity
