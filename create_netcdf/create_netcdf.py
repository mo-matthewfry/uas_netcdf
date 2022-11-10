#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
create_netcdf.py
"""

import os
import sys
import argparse

import netCDF4 as nc
import numpy as np


def parse_args(args):
    """
    Parses CLI's
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--datadir", default="../data/", type=str)
    parser.add_argument("--outdir", default="../data/", type=str)
    parser.add_argument("--save_file", default="test.nc", type=str)

    args = parser.parse_args(args)

    return args


def add_var_metadata(var, std_name, long_name, units,
                     coords=None, positive=None, axis=None):
    
    var.standard_name = std_name
    var.long_name = long_name
    var.units = units

    # Niche metadata used for a subset of variables
    if coords:
        var.coordinates = coords
    if positive:
        var.positive = positive
    if axis:
        var.axis = axis






def create_netcdf(args):

    filename = os.path.join(args.datadir, args.save_file)

    ncfile = nc.Dataset(filename, 'w', format="NETCDF4")

    #---MANDATORY GLOBAL ATTRIBUTES---#
    ncfile.featureType = "trajectory"
    ncfile.Conventions = "CF-1.8, WM= CF-1.0, ACDD-1.3"
    ncfile.wmo__cf_profile = "FM 303-2024"

    #---RECOMMENDED GLOBAL ATTRIBUTES---#
    ncfile.platform_name = ""
    ncfile.Platform_ID = ""
    ncfile.flight_id = ""

    #---DIMENSIONS---#
    obs = ncfile.createDimension('obs', 42)

    #---COORDINATE VARIABLES---#
    time = ncfile.createVariable('time', np.float64, ('obs',))
    lat = ncfile.createVariable('lat', np.float32, ('obs',))
    lon = ncfile.createVariable('lon', np.float32, ('obs',))
    z = ncfile.createVariable('z', np.float32, ('obs',))

    #---GEOPHYSICAL VARIABLES---#
    temp = ncfile.createVariable('temp', np.float32, ('obs',))
    rh = ncfile.createVariable('rh', np.float32, ('obs',))

    #---COORDINATE VARIABLE METADATA---#
    add_var_metadata(time, "time", "time", "days since 1970-01-01 00:00:00")
    add_var_metadata(lat, "latitude", "latitude", "degrees_north")
    add_var_metadata(lon, "longitude", "longitude", "degrees_east")
    add_var_metadata(z, "altitude", "height above mean sea level", "km",
                     positive="up", axis="Z")

    #---GEOPHYSICAL VARIABLE METADATA---#
    add_var_metadata(temp, "air_temperature", "bulk temperature of the air",
                     "K", coords="time lon lat z")
    add_var_metadata(rh, "relative_humidity", "relative humidity"\
                     + " - percentage water vapour content of air",
                     "%", coords="time lon lat z")

    return ncfile

def main():
    """
    main
    """

    args = parse_args(sys.argv[1:])

    ncfile = create_netcdf(args)

    print(ncfile)

if __name__ == "__main__":
    main()
