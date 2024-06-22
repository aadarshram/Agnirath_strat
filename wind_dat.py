import pandas as pd
import numpy as np
df1=pd.read_csv('wind_speed.csv')
df2=pd.read_csv('processed_route_data.csv')
df3=pd.DataFrame()
for i in range(len(df1)):
    dfk=pd.concat([df1.iloc[i]] * 600, ignore_index=True,axis=1)
    df3=pd.concat([df3,dfk],ignore_index=True,axis=1)
df3=df3.transpose()    
print((df3.iloc[1:3]))    
df3.to_csv('wind_data.csv',index=False)    
