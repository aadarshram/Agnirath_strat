import pandas as pd

route_df = pd.read_csv("raw_route_data.csv")
run_dat = pd.read_csv("run_dat.csv")

def set_at_sampling_rate(route_df):

    for i in range(0, len(route_df), 680):
        route_df.loc[i: (i+680),'Slope (deg)'] = route_df['Slope (deg)'][i: (i+680)].mean()

    route_df.to_csv("processed_route_data.csv", index=False)

def find_control_stops(run_data):
    d_control_stops = [322., 588., 987., 1210., 1493., 1766., 2178., 2432., 2720.]
    
    nearest_cum_dist = pd.merge_asof(pd.DataFrame({'Stop distances': d_control_stops}), run_dat['Cumulative Distance'], left_on = 'Stop distances',  right_on = 'Cumulative Distance', direction = 'nearest')
    result = pd.merge(nearest_cum_dist, run_dat, on = 'Cumulative Distance')
    
    return result['Time']