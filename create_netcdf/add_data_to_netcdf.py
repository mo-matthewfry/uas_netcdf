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

import create_netcdf
import load_data


def main():

    filename = "../data/processed/test.csv"
    data = load_data.open_file(filename)
    
    args = create_netcdf.parse_args(sys.argv[1:])
    args.obs_len = len(data)
    ncfile = create_netcdf.create_netcdf(args)



if __name__ == "__main__":
    main()
