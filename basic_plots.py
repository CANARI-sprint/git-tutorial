# This script works through an example using the CANARI-LE historical data to make various Sea Surface Temperature plots

# Imports the python packages used read in, analyse and plot data:
import xarray as xr  # Lets you read in data
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import glob
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Sea surface data is stored as daily data in the priority variables under the variable name tos and can be taken as the top temperature layer from votemper,
# which is stored as monthly means.
# The CANARI-LE computes years comprising of 12 months containing 30 days each, so there should be 360 days each year.

# Make a list of all temperature files for one ensemble member and one year.
# This should be only one file, but you can edit the command below with wildcards to pick up more of the ensemble.
datadir = '/gws/nopw/j04/canari/shared/large-ensemble/priority/HIST2/'
infiles = glob.glob((datadir + '1/OCN/yearly/1950/*_votemper.nc')) # First ensemble member only, need to make a list of all files

# Lazy load data into xarray (only reads data into memory when needed):
t_data = xr.open_mfdataset(infiles)

# xarray is capable of doing a lot of things but if you just want to use it to read in data and then work with numpy arrays the .to_numpy().
# The example below reads the first time step of the surface temperature data:
sst = t_data['votemper'][0,0,:,:].to_numpy()


# The plot above, while very simple to plot does not have the proper latitudes and longitudes.
# This example will use Cartopy to make a prettier plot.

fig = plt.figure(figsize=(12,7))
# Choose projection:
ax = plt.axes(projection=ccrs.Robinson())
plt.pcolormesh(t_data['nav_lon'],t_data['nav_lat'],sst,transform=ccrs.PlateCarree(),shading='nearest')
# shading='nearest' will use the provided latitude and longitude to be the centre of the grid box.  It's more accurate to provide
# the corners, to nav_lon and nav_lat will be one larger in each direction.
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.5'))
ax.coastlines(color='1')

# Add in gridlines
gl=ax.gridlines(draw_labels=True)
gl.top_labels = False
gl.left_labels = False
gl.xlabel_style = {'fontsize': 14}
gl.ylabel_style = {'fontsize': 14}

plt.title('January 1950 Sea Surface Temperature',fontsize=16)

cb = plt.colorbar(extend='both',orientation='horizontal')
cb.ax.tick_params(labelsize=14)
cb.set_label('temperature ($^{\circ}$C)',size=16)

# Make the latitudes and longitudes be the corner of the grid boxes:
lon_corner = t_data['bounds_nav_lon'][:,:,0].to_numpy()
lat_corner = t_data['bounds_nav_lat'][:,:,0].to_numpy()

# Add extra on right:
lon_corner = np.concatenate((lon_corner,t_data['bounds_nav_lon'][:,-1:,1].to_numpy()),axis=1)
lat_corner = np.concatenate((lat_corner,t_data['bounds_nav_lat'][:,-1:,1].to_numpy()),axis=1)

# Add extra on top:
lon_corner = np.concatenate((lon_corner,np.concatenate((t_data['bounds_nav_lon'][-1:,:,3].to_numpy(),t_data['bounds_nav_lon'][-1:,-1:,2].to_numpy()),axis=1)),axis=0)
lat_corner = np.concatenate((lat_corner,np.concatenate((t_data['bounds_nav_lat'][-1:,:,3].to_numpy(),t_data['bounds_nav_lat'][-1:,-1:,2].to_numpy()),axis=1)),axis=0)

# Different global projection and different data:

fig = plt.figure(figsize=(12,7))
# Choose projection (there are several different things you can change for different projections, see https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html):
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=-60))

# Choose a different colorbar and make it have 21 distinct colours instead continuous colors
cmap = plt.get_cmap('RdBu',21)

plt.pcolormesh(lon_corner,lat_corner,t_data['votemper'][6,0,:,:]-t_data['votemper'][0,0,:,:],transform=ccrs.PlateCarree(),vmin=-1.05*10,vmax=1.05*10,shading='flat',cmap=cmap)
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.75'))
ax.coastlines(color='0')

# Add in gridlines
gl=ax.gridlines(draw_labels=True)
gl.top_labels   = False
gl.right_labels = False
gl.xlabel_style = {'fontsize': 14}
gl.ylabel_style = {'fontsize': 14}

plt.title('July - January 1950 Sea Surface Temperature',fontsize=16)

cb = plt.colorbar(extend='both',orientation='vertical',shrink=0.5)
cb.ax.tick_params(labelsize=14)
cb.set_label('temperature difference ($^{\circ}$C)',size=16)
plt.savefig('july-jan1950sst.png')

# Same plot as above but for Atlantic-Arctic projection:

fig = plt.figure(figsize=(12,7))
# Choose projection (there are several different things you can change for different projections, see https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html):
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-30, central_latitude=50))

# Choose a different colorbar and make it have 21 distinct colours instead continuous colors
cmap = plt.get_cmap('coolwarm',21)

plt.pcolormesh(lon_corner,lat_corner,t_data['votemper'][6,0,:,:]-t_data['votemper'][0,0,:,:],transform=ccrs.PlateCarree(),vmin=-1.05*10,vmax=1.05*10,shading='flat',cmap=cmap)
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.75'))
ax.coastlines(color='0')

# Add in gridlines
gl=ax.gridlines(draw_labels=True)
gl.top_labels   = False
gl.right_labels = False
gl.xlabel_style = {'fontsize': 14}
gl.ylabel_style = {'fontsize': 14}

plt.title('July - January 1950 Sea Surface Temperature',fontsize=16)

cb = plt.colorbar(extend='both',orientation='vertical',shrink=0.75)
cb.ax.tick_params(labelsize=14)
cb.set_label('temperature difference ($^{\circ}$C)',size=16)

plt.savefig('july-jan-1950-sst-atl-arc.png')
