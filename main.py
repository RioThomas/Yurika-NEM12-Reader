import glob

import numpy as np
from nemreader import output_as_data_frames
import pandas as pd

dfs = {}
pvs = {}

# For each NEM12 File:
nem12_file_list = glob.glob('examples/NEM12*')
for file in nem12_file_list:
    nmi, df = output_as_data_frames(file)[0]
    df.insert(1, "Date", df["t_start"].dt.date)
    df.insert(2, "Time", df["t_start"].dt.time)

    if nmi in dfs.keys():
        dfs[nmi] = pd.concat([dfs[nmi], df], sort=True)
    else:
        dfs[nmi] = df

for nmi, df in dfs.items():
    print(f"{nmi} - {df.shape}")
    pv = pd.pivot_table(df, values='E1', index='Date', columns='Time', aggfunc=np.max)
    pv.to_csv(f"output/{nmi}_load_profile.csv")
    pvs[nmi] = pv

print('fin')
