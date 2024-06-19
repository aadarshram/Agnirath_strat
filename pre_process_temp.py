import pandas as pd
import numpy as np
df11=pd.read_csv("raw_route_data.csv")
df1=pd.read_csv("raw_route_data.csv")
df2=pd.read_csv('windcheck.csv')
df1["WindSpeed(m/s)"]=df2["WindSpeed(m/s)"]*5/18
df1["Winddirection(frmnorth)"]=(df2["Winddirection(frmnorth)"])
df1=df1.fillna(0)
df1.to_csv('raw_route_data_final.csv',index=False)
''''slope_df=df11["Slope (deg)"]
cum_df=df11["CumulativeDistance(km)"]
for j in range(len(df1)//200):
    print(df1.iloc[j*200:200*(j+1)].mean(axis=0).transpose())
    
    df1.iloc[j*200:j*200+200]=pd.concat([df1.iloc[j*200:200*(j+1)].mean(axis=0).transpose()]*200,axis=1).transpose()
def calc_slope(slope_array,step_array):
   df=pd.DataFrame()
   df["Slope (deg)"] =np.arctan([sum(np.tan(np.radians(slope_array))*step_array)/sum(step_array)])*180/np.pi
   return df
for j in range(len(df1)//200):
   
    df1["Slope (deg)"].iloc[j*200:(j+1)*200]=pd.concat([calc_slope(slope_df.iloc[j*200:j*200+200],df1["StepDistance(m)"].iloc[j*200:j*200+200])]*200,axis=0)["Slope (deg)"]
df1["CumulativeDistance(km)"]=cum_df    
df1["Winddirection(frmnorth)"]=np.arccos(df1["Winddirection(frmnorth)"])*180/np.pi

df1.to_csv('processed_route_data_x.csv',index=False)    '''