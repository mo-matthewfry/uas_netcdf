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


class NetCDF:
    """
    A class to represent NetCDF files.

    Attributes:
        file (obj): A netCDF file
        shape (tuple): Dimension of the variables

    Methods:
        create(): Generates a NetCDF file with no data, but with
                  the relevant structure and metadata to hold
                  UAS data
        add_metadata(): Adds metadata for a given variable
        add_data(): Adds data to a given variable or list of variables
    """

    def create(self, args):
        """
        Creates an empty (no data) netcdf file with a set structure
        and metadata, ready to be populated with UAS data.

        Parameters:
            args: Command line arguments
        """

        filename = os.path.join(args.datadir, args.save_file)

        self.file = nc.Dataset(filename, 'w', format="NETCDF4")

        #---MANDATORY GLOBAL ATTRIBUTES---#
        self.file.featureType = "trajectory"
        self.file.Conventions = "CF-1.8, WM= CF-1.0, ACDD-1.3"
        self.file.wmo__cf_profile = "FM 303-2024"

        #---RECOMMENDED GLOBAL ATTRIBUTES---#
        self.file.platform_name = ""
        self.file.Platform_ID = ""
        self.file.flight_id = ""

        #---DIMENSIONS---#
        self.obs = self.file.createDimension('obs', args.obs_len)
        self.shape = ('obs',)

        # Set up the optional trajectory dimension if requried
        if args.traj_len is not None:

            #---DIMENSIONS---#
            self.trajectory_dim = self.file.createDimension('trajectory', args.traj_len)

            #---TRAJECTORY VARIABLES---#
            self.trajectory_var = self.file.createVariable('trajectory', 'S1',
                                                           ('trajectory',))
            self.trajectory_var.cf_role = "trajectory_id"
            self.trajectory_var.long_name = "trajectory name"

            self.trajectory_info = self.file.createVariable('trajectory_info',
                                                            np.int64,
                                                            ('trajectory',))
            self.trajectory_info.long_name = "some kind of trajectory info"

            self.shape = ('trajectory', 'obs',)

        #---COORDINATE VARIABLES---#
        self.time = self.file.createVariable('time', np.float64, self.shape)
        self.lat = self.file.createVariable('lat', np.float32, self.shape)
        self.lon = self.file.createVariable('lon', np.float32, self.shape)
        self.z = self.file.createVariable('z', np.float32, self.shape)

        #---GEOPHYSICAL VARIABLES---#
        self.temp = self.file.createVariable('temp', np.float32, self.shape)
        self.rh = self.file.createVariable('rh', np.float32, self.shape)
        self.pres = self.file.createVariable('pres', np.float32, self.shape)

        #---COORDINATE VARIABLE METADATA---#
        self.add_metadata(self.time, "time", "time", "days since 1970-01-01 00:00:00")
        self.add_metadata(self.lat, "latitude", "latitude", "degrees_north")
        self.add_metadata(self.lon, "longitude", "longitude", "degrees_east")
        self.add_metadata(self.z, "altitude", "height above mean sea level", "km",
                          positive="up", axis="Z")

        #---GEOPHYSICAL VARIABLE METADATA---#
        self.add_metadata(self.temp, "air_temperature", "bulk temperature of the air",
                          "K", coords="time lon lat z")
        self.add_metadata(self.pres, "air_pressure", "air pressure",
                          "Pa", coords="time lon lat z")
        self.add_metadata(self.rh, "relative_humidity", "relative humidity"\
                          + " - percentage water vapour content of air",
                          "%", coords="time lon lat z")


    def add_metadata(self, var, std_name, long_name, units,
                     coords=None, positive=None, axis=None):
        """
        Adds metadata for the given variable.

        Parameters:
            var: The variable to be edited
            std_name (str): The standard name
            long_name (str): The long name
            units (str): The units
            coords (optional): The coordinates of the variable
            positive (str, optional): Which direction is positive
            axis (str, optional): The axis
        """

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


    def add_data(self, data, variables):
        """
        Adds data to a variable, or a list of variables.
        !! Variable names must be the same between the netcdf file
        and the dataframe !!

        Parameters:
            data (DataFrame): A dataframe holding the variables
            variables (str/list): A single variable, or list of variables
                                  to add to the netcdf file
        """

        if not isinstance(variables, list):
            variables = [variables]

        for variable in variables:
            self.file[variable][:] = data[variable]


def main():
    """
    main
    """

    args = parse_args(sys.argv[1:])

    ncfile = NetCDF()
    ncfile.create(args)

    print(ncfile.file)
    print(ncfile.time[:])


if __name__ == "__main__":
    main()
