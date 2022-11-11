#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
load_data.py
"""

import os
import numpy as np
import pandas as pd


def open_file(filename):
    """
    temp
    """
    return pd.read_csv(filename)


def convert_time_to_timestamp(data):
    """
    Converting seperate time columns to epoch timestamp
    """

    time_cols = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']

    data["Time"] = pd.to_datetime(data[time_cols])
    data['timestamp'] = pd.to_numeric(data['Time'].values) / 10 ** 9
    data["timestamp"] = data["timestamp"].round(2)
    data.drop(time_cols + ["Time"], axis=1, inplace=True)


def rename_columns(data):
    """
    Renaming the variables
    """

    data.rename(columns={"timestamp":"time",
                         "Height(m)":"z",
                         "Pressure":"pres",
                         "Temperature(C) (Thermistor(2))":"temp",
                         "RH(%) (HYT271(2))":"rh"
                        }, inplace=True)


def save_to_file(data, filename):
    """
    Reorder columns and save to file
    """

    cols = ["time", "z", "pres", "temp", "rh"]

    data["z"] /= 1000.0
    data["temp"] += 273.15

    data[cols].to_csv(filename, index=False)

    return data[cols]


def process_file(raw_filename, save_filename):

    data = open_file(raw_filename)

    convert_time_to_timestamp(data)

    rename_columns(data)

    data = save_to_file(data, save_filename)

    return data


def main():
    """
    main
    """
    data = open_file("../data/raw/20200625_0800_UAV.csv")

    convert_time_to_timestamp(data)

    rename_columns(data)

    save_to_file(data, "../data/processed/test.csv")


if __name__ == "__main__":
    main()