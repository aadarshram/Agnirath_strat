import d_config
import pandas as pd

# Model Settings
ModelMethod = "COBYLA"
InitialGuessVelocity = 25 # kmph (Total average speed)

# Day-wise race time
RaceStartTime = 8 * 3600  # 8:00 am
RaceEndTime = 17 * 3600  # 5:00 pm
DT = RaceEndTime - RaceStartTime

Day = 1
TimeOffset = 0

# Waypoints for battery and distance at control stops

# BatteryLevel
BatteryLevelWayPoints = [1, 0.4994, 0.808, 0.2543, 0.488, 0.2276, 0.408, 0.2410, 0.27, 0.2393, 0.22] # Found by anoter optimization model on battery
# Route DF
DF_WayPoints = [0, 57, 102, 169, 207, 254, 301, 371, 415, 464, 520]

InitialBatteryCapacity = None
FinalBatteryCapacity = None
route_df = None

# We work with a day-wise optimization model
def set_day_state(day_no, index_no, time_offset = 0):
    '''
    Set day-wise appropriate values
    '''
    global InitialBatteryCapacity, FinalBatteryCapacity, route_df, Day, TimeOffset
    Day = day_no
    TimeOffset = time_offset
    InitialBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no] # Wh
    FinalBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no+1]  # Wh
    route_df = pd.read_csv("raw_route_data.csv").iloc[DF_WayPoints[index_no]: DF_WayPoints[index_no+1]]
    
    return None