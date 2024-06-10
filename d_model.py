'''
Main model
'''
import numpy as np
from scipy.optimize import minimize
import pandas as pd
from d_car_dynamics import calculate_dx
import d_setting
from d_constraints import get_bounds, objective, battery_and_acc_constraint, final_battery_constraint
from profiles import extract_profiles



def main(route_df):
    # choose dt in whatevr resolution
    DT = d_setting.RaceEndTime - d_setting.RaceStartTime
    step = 600 # s
    N = DT // step
    dt = np.full(N, step)
    
    slope_array = route_df.iloc[:, 2].to_numpy()
    cum_d_array = route_df.iloc[:, 1].to_numpy()
    lattitude_array = route_df.iloc[:, 3].to_numpy()
    longitude_array = route_df.iloc[:, 4].to_numpy()

    N_V = N + 1
    
    initial_velocity_profile = np.ones(N_V) * d_setting.InitialGuessVelocity

    bounds = get_bounds(N_V)

    constraints = [
        {
            "type": "ineq",
            "fun": battery_and_acc_constraint,
            "args": (
                dt, cum_d_array, slope_array, lattitude_array, longitude_array
            )
        },
        {
            "type": "ineq",
            "fun": final_battery_constraint,
            "args": (
                dt, cum_d_array, slope_array, lattitude_array, longitude_array
            )
        },
    ]


    print("Starting Optimisation")
    print("=" * 60)

    optimised_velocity_profile = minimize(
        objective, 
        initial_velocity_profile,
        args = (dt,),
        bounds = bounds,
        method = d_setting.ModelMethod,
        constraints = constraints,
    )
    optimised_velocity_profile = np.array(optimised_velocity_profile.x) * 1 # derive the velocity profile
    dt1 =  np.concatenate((np.array([0]), dt.cumsum())) + d_setting.TimeOffset
    distance_travelled_array = optimised_velocity_profile * dt1
    distance_travelled = distance_travelled_array.sum() / 1000 # km
    print("done.")
    print("Total distance travelled for race:", distance_travelled, "km")

    outdf = pd.DataFrame(
        dict(zip(
            ['CummulativeDistance', 'Velocity', 'Acceleration', 'Battery', 'EnergyConsumption', 'Solar', 'Time'],
            extract_profiles(optimised_velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array)
        ))
    )

    return outdf, distance_travelled

if __name__ == "__main__":
    outdf, _ = main(d_setting.route_df)
    outdf.to_csv('run_dat.csv', index=False)
    print("Written results to `run_dat.csv`")