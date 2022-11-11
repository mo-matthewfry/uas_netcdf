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
    parser.add_argument("--obs_len", default=0, type=int)
    parser.add_argument("--traj_len", default=None, type=int)

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


def create(self, args):

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
    obs = ncfile.createDimension('obs', args.obs_len)
    shape = ('obs',)

    # Set up the optional trajectory dimension if requried
    if args.traj_len is not None:

        #---DIMENSIONS---#
        trajectory_dim = ncfile.createDimension('trajectory', args.traj_len)

        #---TRAJECTORY VARIABLES---#
        trajectory_var = ncfile.createVariable('trajectory', 'S1',
                                            ('trajectory',))
        trajectory_var.cf_role = "trajectory_id"
        trajectory_var.long_name = "trajectory name"

        trajectory_info = ncfile.createVariable('trajectory_info', 
                                                np.int64,
                                                ('trajectory',))
        trajectory_info.long_name = "some kind of trajectory info"

        shape = ('trajectory', 'obs',)

    #---COORDINATE VARIABLES---#
    time = ncfile.createVariable('time', np.float64, shape)
    lat = ncfile.createVariable('lat', np.float32, shape)
    lon = ncfile.createVariable('lon', np.float32, shape)
    z = ncfile.createVariable('z', np.float32, shape)

    #---GEOPHYSICAL VARIABLES---#
    temp = ncfile.createVariable('temp', np.float32, shape)
    rh = ncfile.createVariable('rh', np.float32, shape)

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

    variable = {"time":time,
                "lat":lat,
                "lon":lon,
                "z":z,
                "temp":temp,
                "rh":rh,
                "obs":obs
            }

    if args.traj_len is not None:
        variable["trajectory_dim"] = trajectory_dim
        variable["trajectory_var"] = trajectory_var
        variable["trajectory_info"] = trajectory_info

    return ncfile, variable


def main():
    """
    main
    """

    args = parse_args(sys.argv[1:])

    ncfile, variable = create_netcdf(args)

    print(ncfile)

    ncfile.close()


if __name__ == "__main__":
    main()
