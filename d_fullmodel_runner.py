import pandas as pd

import d_setting
import d_config
from d_model import main
from d_offrace_solarcalc import calculate_energy

df_list = []

day_counter = 1
time_counter = 0
CONTROL_STOP_DURATION = 30 * 60
stop_gain = 0

for i in range(10):
    if i % 2 == 0:
        d_setting.set_day_state(day_counter, i, time_counter)
        d_setting.InitialBatteryCapacity = min(d_config.BATTERY_CAPACITY, stop_gain + d_setting.InitialBatteryCapacity)
        outdf, timetaken = main(d_setting.route_df)
        df_list.append(outdf)

        time_counter += timetaken
        stop_gain = calculate_energy(time_counter, time_counter + CONTROL_STOP_DURATION)
        time_counter += CONTROL_STOP_DURATION

    else:
        d_setting.set_day_state(day_counter, i, time_counter)
        d_setting.InitialBatteryCapacity = min(d_config.BATTERY_CAPACITY, stop_gain + d_setting.InitialBatteryCapacity)

        outdf, timetaken = main(d_setting.route_df)

        df_list.append(outdf)
        time_counter += timetaken

        stop_time = d_setting.DT - (time_counter % d_setting.DT)
        stop_gain = calculate_energy(time_counter, time_counter + stop_time)
        time_counter += stop_time

        day_counter += 1

dfnet = pd.concat(df_list)

dfnet.to_csv('run_dat.csv', index=False)
print("Written 5days data to `run_dat.csv`")