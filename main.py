import glob

from nemreader import output_as_data_frames

dfs = {}

# For each NEM12 File:
nem12_file_list = glob.glob('examples/NEM12*')
for file in nem12_file_list:
    nmi, df = output_as_data_frames(file)[0]
    df.insert(1, "Date", df["t_start"].dt.date)
    df.insert(2, "Time", df["t_start"].dt.time)

    if nmi in dfs.keys():
        dfs[nmi] = dfs[nmi].merge(df)
    else:
        dfs[nmi] = df

    # pv = pandas.pivot_table(df, values='E1', index='Date', columns='Time', aggfunc=np.max)

# dfs = output_as_data_frames('examples/examples.zip')
# # Format data for HOMER: day x half-hour:
# for nmi, df in dfs:
#     # print(nmi)
#     df.insert(1, "Date", df["t_start"].dt.date)
#     df.insert(2, "Time", df["t_start"].dt.time)
#     # columns = list(df["t_start"].dt.time.drop_duplicates())
#     pv = pandas.pivot_table(df, values='E1', index='Date', columns='Time', aggfunc=np.max)

print('fin')
