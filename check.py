from d_helper_fns import format_data, add_control_stops,find_control_stops
from d_solar import calculate_incident_solarpower
from d_offrace_solarcalc import calculate_energy
import pandas as pd
import numpy as np
from d_setting import FULL_DAY_TIME, RACE_START
from d_setting import FULL_DAY_TIME
run_dat = pd.read_csv('processed_run_dat.csv')
print(calculate_energy(41000%FULL_DAY_TIME+RACE_START,41000%FULL_DAY_TIME+RACE_START+1800))
print(sum(calculate_incident_solarpower(np.array(range(41000%FULL_DAY_TIME,41000%FULL_DAY_TIME+1800)),0,0))/3600)


