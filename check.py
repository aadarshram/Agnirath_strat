from d_helper_fns import format_data, add_control_stops,find_control_stops
from d_solar import calculate_incident_solarpower
from d_offrace_solarcalc import calculate_energy
import pandas as pd
import numpy as np
from d_setting import FULL_DAY_TIME
run_dat = pd.read_csv('xxx.csv')

print(sum(calculate_incident_solarpower(np.array(range(55200,14000+1800,200)),0,0)*200/3600))
