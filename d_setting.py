'''
Set day-wise model parameters
'''

# Import necessary modules

from d_config import BATTERY_CAPACITY, KM
import pandas as pd

# Model Settings

ModelMethod = "COBYLA"
<<<<<<< HEAD
# ModelMethod = "trust-constr"
InitialGuessVelocity = 22
# m/s (Total average speed)
=======
InitialGuessVelocity = 20 # m/s (Total average speed)
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05

RunforDays = 5
# Day-wise race time

RACE_START = 8 * 3600  # 8:00 am
RACE_END = 17 * 3600  # 5:00 pm
RACE_DISTANCE = 3037 * KM

CONTROL_STOP_DURATION = int(0.5 * 3600) # s

<<<<<<< HEAD
# # BatteryLevel
# BatteryLevelWayPoints = [1, 0.4994, 0.808, 0.2543, 0.488, 0.2276, 0.408, 0.2410, 0.27, 0.2393, 0.22] # Found by anoter optimization model on battery
# # Route DF
# DF_WayPoints = [0, 57, 102, 169, 207, 254, 301, 371, 415, 464, 520]
FinalBatteryCapacity_list=[60,50,40,30,0]
=======
DT = RACE_END - RACE_START - 2 * CONTROL_STOP_DURATION # Race time for model
# Assuming 2 control stops a day (This is almost always right)

# Control stops
d_control_stops = [322., 588., 987., 1210., 1493., 1766., 2178., 2432., 2720.] # 2023 data

# Resolution 
STEP = 200 # s

# Average velocity

AVG_V = RACE_DISTANCE / (DT * RunforDays)

# Final Battery optimisation way-points
discharge_list= [60, 60, 40, 40, 0]
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05

# route_df = pd.read_csv("raw_route_data.csv")
<<<<<<< HEAD
route_df = pd.read_csv("processed_route_data_x.csv")

def set_day(day_no, present_battery_cent, i, time_offset = 0):
    global InitialBatteryCapacity, Day, TimeOffset,DISCHARGE_CAP,FinalBatteryCapacity
    Day = day_no
    TimeOffset = time_offset
    # DISCHARGE_CAP = discharge_list[i]/100
    DISCHARGE_CAP = 0
    present_battery_cap = (present_battery_cent / 100) * d_config.BATTERY_CAPACITY
    InitialBatteryCapacity = present_battery_cap # Wh
    #InitialBatteryCapacity  = InitialBatteryCapacity_list[i] / 100 * d_config.BATTERY_CAPACITY # Wh
    FinalBatteryCapacity = (FinalBatteryCapacity_list[i] / 100) * d_config.BATTERY_CAPACITY
    
    #FinalBatteryCapacity = d  # Wh
=======
route_df = pd.read_csv("processed_route_data.csv")


def set_day(present_battery_cent, i): # , time_offset = 0
    '''
    Set day-wise parameters
    '''

    global InitialBatteryCapacity
    # global TimeOffset
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05
    
    # TimeOffset = time_offset
    # DISCHARGE_CAP = discharge_list[i]/100
    PresentBatteryCapacity = (present_battery_cent / 100) * BATTERY_CAPACITY
    InitialBatteryCapacity = PresentBatteryCapacity # Wh
    FinalBatteryCapacity = (discharge_list[i] / 100) * BATTERY_CAPACITY
    #     InitialBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no] # Wh
#     FinalBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no+1]  # Wh
#     route_df = pd.read_csv("raw_route_data.csv").iloc[DF_WayPoints[index_no]: DF_WayPoints[index_no+1]]
    return InitialBatteryCapacity, FinalBatteryCapacity, #TimeOffset
