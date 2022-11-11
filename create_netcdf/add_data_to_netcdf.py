#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
add_data_to_netcdf.py
"""

import os
import sys
import argparse

import netCDF4 as nc
import numpy as np

from create_netcdf import NetCDF, parse_args
from load_data import process_file


def add_data():

    args = parse_args(sys.argv[1:])
    raw_path = "../data/raw/"
    save_path = "../data/processed/"
    nc_path = "../data/nc_files/"

    for filename in os.listdir(raw_path):

        if os.path.isdir(raw_path+filename):
            continue

        data = process_file(raw_path+filename,
                            save_path+filename)
        
        args.obs_len = len(data)
        args.save_file = nc_path+filename[:-4]+".nc"

        ncfile = NetCDF()
        ncfile.create(args)
        ncfile.add_data(data, ["time", "z", "temp", "rh", "pres"])

        ncfile.file.close()


if __name__ == "__main__":
    add_data()
