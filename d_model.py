'''
Main day-wise model
'''

# Import necessary modules
import numpy as np
from scipy.optimize import fmin_cobyla, minimize
import pandas as pd
<<<<<<< HEAD
from d_car_dynamics import calculate_dx,convert_domain_d2t
import d_setting
from d_constraints import get_bounds, objective, battery_and_acc_constraint, final_battery_constraint, v_end#control_stop_constraint
=======
from d_config import KM, HR
from d_car_dynamics import calculate_dx
from d_setting import ModelMethod, InitialGuessVelocity, DT, STEP, route_df
from d_constraints import get_bounds, objective, battery_and_acc_constraint #, v_end
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05
from d_profiles import extract_profiles



<<<<<<< HEAD
def main(route_df, cum_d, i):
    iter_list=[8000,5000,9000,7000,9000]
    # choose dt in whatevr resolution
    DT = d_setting.DT
    step = 200 # s
=======
def main(route_df, cum_d, i, InitialBatteryCapacity, FinalBatteryCapacity):
    
    step = STEP
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05
    N = DT // step
    dt = np.full(int(N), step) # Set race time scale

    # Get data
    cum_d_array = route_df.iloc[:, 1].to_numpy()
    slope_array = route_df.iloc[:, 2].to_numpy()
    lattitude_array = route_df.iloc[:, 3].to_numpy()
    longitude_array = route_df.iloc[:, 4].to_numpy()
    ws_array = route_df.iloc[:, 5].to_numpy()
    wd_array = route_df.iloc[:, 6].to_numpy()

    N_V = int(N) + 1
    
    initial_velocity_profile = np.concatenate((np.array([0]), np.ones(N_V - 2) * InitialGuessVelocity, np.array([0])))

    bounds = get_bounds(N_V)

    constraints = [
        {
            "type": "ineq",
            "fun": battery_and_acc_constraint,
            "args": (
<<<<<<< HEAD
                dt, cum_d_array, slope_array, lattitude_array, longitude_array,ws_array,wd_array, cum_d, i
            )
        },
       # {
          #  "type": "ineq",
           # "fun": control_stop_constraint,
            ##  cum_d,
            #)
        #},
         {
             "type": "ineq",
          "fun": final_battery_constraint,
             "args": (
                dt, cum_d_array, slope_array, lattitude_array, longitude_array,ws_array,wd_array
             )
              
               },
        {
            "type": "ineq",
            "fun": v_end,
            "args": (
                dt, cum_d,
            )     
=======
                dt, cum_d_array, slope_array, lattitude_array, longitude_array, cum_d, i, InitialBatteryCapacity, FinalBatteryCapacity
            )
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05
        }
     ]


    print("Starting Optimisation")

    optimised_velocity_profile = minimize(
        objective, 
        initial_velocity_profile,
<<<<<<< HEAD
        args = (dt,  cum_d_array, slope_array, lattitude_array, longitude_array,ws_array,wd_array, cum_d, i
                ),
=======
        args = (dt, cum_d_array, slope_array, lattitude_array, longitude_array, cum_d),
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05
        bounds = bounds,
        method = ModelMethod,
        constraints = constraints,
<<<<<<< HEAD
         options = {'tol':1e-8,'disp':True,'maxiter':30000}
        #options = {'verbose': 3}
=======
        #options = {'catol': 10 ** -6, 'disp': True, 'maxiter': 10 ** 5}
        #options = {'maxiter': 3}
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05
    )

    # optimised_velocity_profile = fmin_cobyla(
    #     objective,
    #     initial_velocity_profile,
    #     constraints,
    #     (),
    #     rhobeg,
    #     rhoend,
    #     maxfun,

    # )
    optimised_velocity_profile = np.array(optimised_velocity_profile.x) * 1 # derive the velocity profile

    dx = calculate_dx(optimised_velocity_profile[:-1], optimised_velocity_profile[1:], dt) # Find total distance travelled
    distance_travelled = np.sum(dx) / KM # km

    print("done.")
    print("Total distance travelled in day", (i+1), " :", distance_travelled, "km in travel time:", dt.sum() / HR, 'hrs')

   
  
    outdf = pd.DataFrame(
        dict(zip(
            ['Time', 'Velocity', 'Acceleration', 'Battery', 'EnergyConsumption', 'Solar', 'Cumulative Distance'],
<<<<<<< HEAD
            extract_profiles(optimised_velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array,ws_array,wd_array)
=======
            extract_profiles(optimised_velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array, cum_d, i, InitialBatteryCapacity)
>>>>>>> 5899c6c00abac063e9dfe9c54ef49803a0b4fe05
        ))
    )
    outdf['Cumulative Distance'] = np.concatenate([[0], dx.cumsum() / KM])
    return outdf, dt.sum()

if __name__ == "__main__":
    outdf, _ = main(route_df)
    outdf.to_csv('run_dat.csv', index=False)

    print("Written results to `run_dat.csv`")