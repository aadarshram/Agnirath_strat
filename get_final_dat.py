from d_preprocess import format_data, add_control_stops
import pandas as pd

run_dat = pd.read_csv("run_dat1.csv")
run_dat = format_data(run_dat)
run_dat = add_control_stops(run_dat)
run_dat.to_csv('final_run_dat.csv', index = False)