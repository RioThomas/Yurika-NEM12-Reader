import os
from os import walk, path

import numpy as np
import pandas as pd
from nemreader import output_as_data_frames


def startup():
    folders = ["input", "output", "processed"]

    print("""
 ███╗   ██╗███████╗███╗   ███╗       ██╗██████╗     ██████╗ ███████╗ █████╗ ██████╗ ███████╗██████╗ 
 ████╗  ██║██╔════╝████╗ ████║      ███║╚════██╗    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗
 ██╔██╗ ██║█████╗  ██╔████╔██║█████╗╚██║ █████╔╝    ██████╔╝█████╗  ███████║██║  ██║█████╗  ██████╔╝
 ██║╚██╗██║██╔══╝  ██║╚██╔╝██║╚════╝ ██║██╔═══╝     ██╔══██╗██╔══╝  ██╔══██║██║  ██║██╔══╝  ██╔══██╗
 ██║ ╚████║███████╗██║ ╚═╝ ██║       ██║███████╗    ██║  ██║███████╗██║  ██║██████╔╝███████╗██║  ██║
 ╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝       ╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
""")
    print(" By Rio Thomas.")

    for folder in folders:
        if not path.isdir(folder):
            os.mkdir(folder)
            print(f"Subdirectory /{folder}/ did not exist and was created.")

    while True:
        input(f"\nPress Enter to process the NEM12 files in /input/:")
        process("input/")


def process(folder_path):
    dfs = {}
    pvs = {}

    # For each NEM12 File:
    (_, _, nem12_file_list) = next(walk(folder_path))

    if len(nem12_file_list) == 0:
        print(" [X] No files detected!")
        return

    print("\nDetected Files: ")
    [print(f"  |  {i}") for i in nem12_file_list]
    print("")

    for file in nem12_file_list:
        file_path = folder_path + file
        nmi, df = output_as_data_frames(file_path)[0]
        df.insert(1, "Date", df["t_start"].dt.date)
        df.insert(2, "Time", df["t_start"].dt.time)

        # Group data based on NMI:
        if nmi in dfs.keys():
            dfs[nmi] = pd.concat([dfs[nmi], df], sort=True)
        else:
            dfs[nmi] = df

        try:
            os.rename(file_path, f"processed/{file}")
        except FileExistsError as E:
            # File has already been processed.
            os.remove(file_path)

    print("NMIs processed:")
    for nmi, df in dfs.items():
        print(f"  |  {nmi} ({min(df['Date'])} to {max(df['Date'])})")

        pv = pd.pivot_table(df, values='E1', index='Date', columns='Time', aggfunc=np.max)
        pv.to_csv(f"output/{nmi}_load_profile.csv")
        pvs[nmi] = pv


startup()
