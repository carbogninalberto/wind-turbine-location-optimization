import os
import pandas as pd

from windpowerlib.modelchain import ModelChain
from windpowerlib.wind_turbine import WindTurbine
from windpowerlib import wind_turbine as wt

import logging

logging.getLogger().setLevel(logging.DEBUG)

#datasets\1574977166

def get_weather_data(filename='../datasets/1574977166/dataset.csv', **kwargs):
    if 'datapath' not in kwargs:
        kwargs['datapath'] = os.path.join(os.path.split(
            os.path.dirname(__file__))[0], 'example')
    file = os.path.join(kwargs['datapath'], filename)
    # read csv file
    weather_df = pd.read_csv(
        file, index_col=0, header=[0, 1])

    # change type of index to datetime and set time zone
    # weather_df.index = pd.to_datetime(weather_df.index).tz_convert('Europe/Berlin')

    # change type of height from str to int by resetting columns
    l0 = [_[0] for _ in weather_df.columns]
    print('l0: ' + str(l0))
    l1 = [int(_[1]) for _ in weather_df.columns]
    print('l1: ' + str(l1))
    weather_df.columns = [l0, l1]

    return weather_df

# Read weather data from csv

weather = get_weather_data(filename="../datasets/1574977166/dataset.csv", datapath='')
print(weather[['wind_speed', 'temperature', 'pressure']][0:3])


df = wt.get_turbine_types(print_out=False)

# find all Enercons
print(df[df["manufacturer"].str.contains("Enercon")])

print(df[df["turbine_type"].str.contains("E-101")])


# specification of wind turbine where power curve is provided in the
# oedb turbine library

enercon_e126 = {
        'turbine_type': 'E-126/4200',  # turbine type as in oedb turbine library
        'hub_height': 135  # in m
    }
# initialize WindTurbine object
e126 = WindTurbine(**enercon_e126)

# power output calculation for e126

# own specifications for ModelChain setup
modelchain_data = {
    'wind_speed_model': 'logarithmic',      # 'logarithmic' (default),
                                            # 'hellman' or
                                            # 'interpolation_extrapolation'
    'density_model': 'ideal_gas',           # 'barometric' (default), 'ideal_gas'
                                            #  or 'interpolation_extrapolation'
    'temperature_model': 'linear_gradient', # 'linear_gradient' (def.) or
                                            # 'interpolation_extrapolation'
    'power_output_model': 'power_curve',    # 'power_curve' (default) or
                                            # 'power_coefficient_curve'
    'density_correction': True,             # False (default) or True
    'obstacle_height': 0,                   # default: 0
    'hellman_exp': None}                    # None (default) or None

# initialize ModelChain with own specifications and use run_model method to
# calculate power output
mc_e126 = ModelChain(e126, **modelchain_data).run_model(
    weather)
# write power output time series to WindTurbine object
e126.power_output = mc_e126.power_output

enercon_e115 = {
        'turbine_type': 'E-115/3000',  # turbine type as in oedb turbine library
        'hub_height': 92  # in m
    }
# initialize WindTurbine object
e115 = WindTurbine(**enercon_e115)

# power output calculation for e115

# own specifications for ModelChain setup
modelchain_data_e115 = {
    'wind_speed_model': 'logarithmic',      # 'logarithmic' (default),
                                            # 'hellman' or
                                            # 'interpolation_extrapolation'
    'density_model': 'ideal_gas',           # 'barometric' (default), 'ideal_gas'
                                            #  or 'interpolation_extrapolation'
    'temperature_model': 'linear_gradient', # 'linear_gradient' (def.) or
                                            # 'interpolation_extrapolation'
    'power_output_model': 'power_curve',    # 'power_curve' (default) or
                                            # 'power_coefficient_curve'
    'density_correction': True,             # False (default) or True
    'obstacle_height': 0,                   # default: 0
    'hellman_exp': None}                    # None (default) or None

# initialize ModelChain with own specifications and use run_model method to
# calculate power output
mc_e115 = ModelChain(e115, **modelchain_data_e115).run_model(
    weather)
# write power output time series to WindTurbine object
e115.power_output = mc_e115.power_output



# try to import matplotlib
logging.getLogger().setLevel(logging.WARNING)
try:
    from matplotlib import pyplot as plt
    # matplotlib inline needed in notebook to plot inline
except ImportError:
    plt = None

# plot turbine power output
if plt:
    e126.power_output.plot(legend=True, label='Enercon E126')
    e115.power_output.plot(legend=True, label='Enercon E115')
    plt.xlabel('Time')
    plt.ylabel('Power in W')
    plt.show()