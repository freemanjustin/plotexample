# module load pangeo

import netCDF4 as nc4
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob
from scipy import interpolate

def rescale2d(data, scale):
    """
    input 2d matrix
    input scale factor
    """
    # make axis for the original (input) data
    x = np.arange(0, data.shape[1])
    y = np.arange(0, data.shape[0])

    # make axis for the new data that reflects the new scale given by scale arg
    # scale < 1 will reduce the size (ie. sale = 0.5 will reduce the data by half in each dimension (hxw))
    # scale = 1 will return the same data
    # scale > 1 will increase the size (ie scale = 2 will increase the data by doubling each dimension (hxw))
    xn = np.arange(0, data.shape[1], (data.shape[1]/(scale*data.shape[1])))
    yn = np.arange(0, data.shape[0], (data.shape[0]/(scale*data.shape[0])))

    # interp onto new grid
    # settin gthis as cubic interpolation to match the swinir paper
    interp = interpolate.interp2d( x, y, data, kind='cubic')

    interp_data = interp(xn, yn)

    return interp_data


# loop over 1 year of data for temperature screen
# here we are using the high resolution barra-sydney data
filenames = sorted(glob.glob('/g/data/cj37/BARRA/BARRA_SY/v1/forecast/slv/av_temp_scrn/2015/*/*.nc'))

for i in range(0,len(filenames)):
    data = xr.open_mfdataset( filenames[i])

    subset = data

    # convert temperatures to Celsius
    subset['av_temp_scrn'] = subset['av_temp_scrn'] - 273.15

    fname = '%04d.png' % i
    plt.imsave(fname, subset.av_temp_scrn[0,:,:], cmap='Spectral', origin='lower')

    # generate a 2x (ie. half size of the original data -> scale factor = 0.5) smaller image 
    interp = rescale2d(subset.av_temp_scrn[0,:,:], scale=0.5)
    fname = '%04dx2.png' % i
    plt.imsave(fname, interp, cmap='Spectral', origin='lower')
