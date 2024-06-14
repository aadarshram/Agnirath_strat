import pandas as pd
import numpy as np
from d_solar import calc_solar_irradiance
from d_config import PANEL_AREA, PANEL_EFFICIENCY, BATTERY_CAPACITY

route_df = pd.read_csv("raw_route_data.csv")
run_dat = pd.read_csv("run_dat.csv")

def set_at_sampling_rate(route_df):

    for i in range(0, len(route_df), 680):
        route_df.loc[i: (i+680),'Slope (deg)'] = route_df['Slope (deg)'][i: (i+680)].mean()

    route_df.to_csv("processed_route_data.csv", index=False)

def find_control_stops(run_dat):
    d_control_stops = [322., 588., 987., 1210., 1493., 1766., 2178., 2432., 2720.]
    
    nearest_cum_dist = pd.merge_asof(pd.DataFrame({'Stop distances': d_control_stops}), run_dat['Cumulative Distance'], left_on = 'Stop distances',  right_on = 'Cumulative Distance', direction = 'nearest')
    result = pd.merge(nearest_cum_dist, run_dat, on = 'Cumulative Distance')
    
    return np.array(result['Time'])

def format_data(run_dat):
    time = find_control_stops(run_dat)
    i_list = []
    for t in time:
        i = run_dat.index.get_loc(run_dat['Time'].eq(t).idxmax())
        i_list.append(i + 2)
    for i in i_list[::-1]:
        run_dat.loc[(i + 1):,'Time'] += (0.5 * 3600)

    return run_dat


def add_control_stops(run_dat):
    time = find_control_stops(run_dat)
    i_list = []
    for t in time:
        i = run_dat.index.get_loc(run_dat['Time'].eq(t).idxmax())
        i_list.append(i+2)

    for i in i_list:
        time_array = np.array([(run_dat._get_value(i, 'Time') + j) for j in range(200, 2000, 200)])
        acc_array = [0 for j in range(len(time_array))]
        v_array = [0 for j in range(len(time_array))]
        cum_d_array = [(run_dat._get_value(i, 'Cumulative Distance')) for _ in range(len(time_array))]
        solar_array = np.array([(run_dat._get_value(i, 'Solar') + (200 / 3600) * PANEL_EFFICIENCY * PANEL_AREA * calc_solar_irradiance(t1 % (9 * 3600))) for t1 in time_array])
        energy_consumption_array = [0 for j in range(len(time_array))]
        battery_array = ((run_dat._get_value(i, 'Battery') / 100 * BATTERY_CAPACITY) + solar_array) / BATTERY_CAPACITY * 100
        new_dat = pd.DataFrame({'Time': time_array, 'Velocity': v_array, 'Acceleration': acc_array, 'Battery': battery_array, 'EnergyConsumption': energy_consumption_array, 'Solar': solar_array, 'Cumulative Distance': cum_d_array})
        run_dat = pd.concat([run_dat, new_dat])
    run_dat = run_dat.sort_values(by = 'Time', ignore_index = True)

    return run_dat

def find_reachtime(cum_dt, cum_d):
    for i  in range(len(cum_d)):
        if cum_d[i] > 3000:
            return cum_dt[i]
    return None