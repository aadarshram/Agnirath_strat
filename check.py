from d_helper_fns import format_data, add_control_stops,find_control_stops
from d_solar import calculate_incident_solarpower
import pandas as pd

run_dat = pd.read_csv('xxx.csv')

print(find_control_stops(run_dat))