'''
Main model
'''
import numpy as np
from scipy.optimize import minimize
import pandas as pd
from d_car_dynamics import calculate_dx
import d_setting
from d_constraints import get_bounds, objective, battery_and_acc_constraint, final_battery_constraint, v_end
from d_profiles import extract_profiles



def main(route_df, cum_d, i):
    # choose dt in whatevr resolution
    DT = d_setting.DT
    step = 200 # s
    N = DT // step
    dt = np.full(int(N), step)

    cum_d_array = route_df.iloc[:, 1].to_numpy()
    slope_array = route_df.iloc[:, 2].to_numpy()
    lattitude_array = route_df.iloc[:, 3].to_numpy()
    longitude_array = route_df.iloc[:, 4].to_numpy()

    N_V = int(N) + 1
    
    initial_velocity_profile = np.concatenate((np.array([0]), np.ones(N_V - 2) * d_setting.InitialGuessVelocity, np.array([0])))

    bounds = get_bounds(N_V)

    constraints = [
        {
            "type": "ineq",
            "fun": battery_and_acc_constraint,
            "args": (
                dt, cum_d_array, slope_array, lattitude_array, longitude_array, cum_d, i
            )
        },
        # {
        #     "type": "ineq",
        #     "fun": final_battery_constraint,
        #     "args": (
        #         dt, cum_d_array, slope_array, lattitude_array, longitude_array
        #     )
        # },
        {
            "type": "ineq",
            "fun": v_end,
            "args": (
                dt, cum_d,
            )     
        }
     ]


    print("Starting Optimisation")
    print("=" * 60)

    optimised_velocity_profile = minimize(
        objective, 
        initial_velocity_profile,
        args = (dt, cum_d_array, slope_array, lattitude_array, longitude_array, cum_d
                ),
        bounds = bounds,
        method = d_setting.ModelMethod,
        constraints = constraints,
        # options = {'catol': 10 ** -6, 'disp': True, 'maxiter': 10 ** 5}
        #options = {'verbose': 3}
    )
    optimised_velocity_profile = np.array(optimised_velocity_profile.x) * 1 # derive the velocity profile

    dx = calculate_dx(optimised_velocity_profile[:-1], optimised_velocity_profile[1:], dt) 
    dx = dx / 1000 # in km
    distance_travelled = np.sum(dx)
    print("done.")
    print("Total distance travelled for race:", distance_travelled, "km in travel time:", dt.sum() / 3600, 'hrs')

    outdf = pd.DataFrame(
        dict(zip(
            ['Time', 'Velocity', 'Acceleration', 'Battery', 'EnergyConsumption', 'Solar', 'Cumulative Distance'],
            extract_profiles(optimised_velocity_profile, dt, cum_d_array, slope_array, lattitude_array, longitude_array)
        ))
    )
    outdf['Cumulative Distance'] = np.concatenate([[0], dx.cumsum()])
    return outdf, dt.sum()

if __name__ == "__main__":
    outdf, _ = main(d_setting.route_df)
    outdf.to_csv('run_dat.csv', index=False)
    print("Written results to `run_dat.csv`")