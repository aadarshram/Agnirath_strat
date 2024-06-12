import pandas as pd

route_df = pd.read_csv("raw_route_data.csv")

for i in range(0, len(route_df), 680):
    route_df['Slope (deg)'][i: (i+680)] = route_df['Slope (deg)'][i: (i+680)].mean()

route_df.to_csv("processed_route_data.csv", index=False)
