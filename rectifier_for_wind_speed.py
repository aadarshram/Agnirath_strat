import pandas as pd
dfn=pd.read_csv("windcheck.csv")
dfn["WindSpeed(m/s)"]=5/18*dfn["WindSpeed(m/s)"]
dfn.to_csv("wind_checked", index=False)