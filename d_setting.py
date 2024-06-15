import d_config
import pandas as pd

# Model Settings
ModelMethod = "COBYLA"
# ModelMethod = "trust-constr"
InitialGuessVelocity = 20 # m/s (Total average speed)

# Day-wise race time
RaceStartTime = 8 * 3600  # 8:00 am
RaceEndTime = 17 * 3600  # 5:00 pm
Control_stop_time = 0.5 * 3600 # s
DT = RaceEndTime - RaceStartTime - 2 * Control_stop_time

Day = 1
TimeOffset = 0

# # Waypoints for battery and distance at control stops

# # BatteryLevel
# BatteryLevelWayPoints = [1, 0.4994, 0.808, 0.2543, 0.488, 0.2276, 0.408, 0.2410, 0.27, 0.2393, 0.22] # Found by anoter optimization model on battery
# # Route DF
# DF_WayPoints = [0, 57, 102, 169, 207, 254, 301, 371, 415, 464, 520]

#InitialBatteryCapacity = d_config.BATTERY_CAPACITY
#InitialBatteryCapacity = None
#InitialBatteryCapacity_list = [100, 80.8, 48.8, 40.8, 27.7]
# route_df = pd.read_csv("raw_route_data.csv")
route_df = pd.read_csv("processed_route_data.csv")
discharge_list= [80.8, 48.8, 40.8, 27.7, 20]

def set_day(day_no, present_battery_cent, i, time_offset = 0):
    global InitialBatteryCapacity, Day, TimeOffset,DISCHARGE_CAP
    Day = day_no
    TimeOffset = time_offset
    # DISCHARGE_CAP = discharge_list[i]/100
    DISCHARGE_CAP = 0.2
    present_battery_cap = (present_battery_cent / 100) * d_config.BATTERY_CAPACITY
    InitialBatteryCapacity = present_battery_cap # Wh
    #InitialBatteryCapacity  = InitialBatteryCapacity_list[i] / 100 * d_config.BATTERY_CAPACITY # Wh
    #FinalBatteryCapacity = (FinalBatteryCapacity_list[i] / 100) * d_config.BATTERY_CAPACITY

    #FinalBatteryCapacity = d  # Wh
    
#     return None
# We work with a day-wise optimization model
# def set_day_state(day_no, index_no, time_offset = 0):
#     '''
#     Set day-wise appropriate values
#     '''
#     global InitialBatteryCapacity, FinalBatteryCapacity, route_df, Day, TimeOffset
#     Day = day_no
#     TimeOffset = time_offset
#     InitialBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no] # Wh
#     FinalBatteryCapacity = d_config.BATTERY_CAPACITY * BatteryLevelWayPoints[index_no+1]  # Wh
#     route_df = pd.read_csv("raw_route_data.csv").iloc[DF_WayPoints[index_no]: DF_WayPoints[index_no+1]]
    
#     return None