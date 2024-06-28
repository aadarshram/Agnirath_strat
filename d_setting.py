'''
Set day-wise model parameters
'''

# Import necessary modules

from d_config import BATTERY_CAPACITY, KM, HR
import pandas as pd
import numpy as np
# Model Settings

ModelMethod = "COBYLA"
InitialGuessVelocity = 25 # m/s (Total average speed)

RunforDays = 5
# Day-wise race time

RACE_START = 8 * HR  # 8:00 am
RACE_END = 17 * HR  # 5:00 pm
FULL_DAY_TIME=RACE_END-RACE_START

RACE_DISTANCE = 3037 * KM

CONTROL_STOP_DURATION = int(0.5 * 3600) # s

DT = RACE_END - RACE_START - 2 * CONTROL_STOP_DURATION # Race time for model
# Assuming 2 control stops a day (This is almost always right)

# Control stops
d_control_stops = [322., 588., 987., 1210., 1493., 1766., 2178., 2432., 2720.] # 2023 data
control_stop_number=[2, 2, 2, 2, 1]
# Resolution 
STEP = 200 # s
DT_list=np.array([8, 8, 16, 16, 24, 24, 32, 32, 40]) * HR
DT_list_day=np.array([0, 8, 16, 24, 32, 40]) * HR
# Average velocity

AVG_V = RACE_DISTANCE / (DT * RunforDays)

# Final Battery optimisation way-points
discharge_list= [27, 27, 27, 27, 0]


# route_df = pd.read_csv("raw_route_data.csv")



def set_day(present_battery_cent, i): # , time_offset = 0
    '''
    Set day-wise parameters
    '''

    global InitialBatteryCapacity, DT
    # global TimeOffset
    DT = RACE_END - RACE_START - control_stop_number[i] * CONTROL_STOP_DURATION
    # TimeOffset = time_offset
    # DISCHARGE_CAP = discharge_list[i]/100
    PresentBatteryCapacity = (present_battery_cent / 100) * BATTERY_CAPACITY
    InitialBatteryCapacity = PresentBatteryCapacity # Wh
    FinalBatteryCapacity = (discharge_list[i] / 100) * BATTERY_CAPACITY
    #     InitialBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no] # Wh
#     FinalBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no+1]  # Wh
#     route_df = pd.read_csv("raw_route_data.csv").iloc[DF_WayPoints[index_no]: DF_WayPoints[index_no+1]]
    return InitialBatteryCapacity, FinalBatteryCapacity,DT #TimeOffset
