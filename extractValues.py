# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 09:21:19 2019

@author: cpan
"""
'''
Caleb G. Pan
RedCastle Resources, Inc
Salt Lake City, UT
caleb.pan@usda.gov

THIS SCRIPT TAKES A POINTS IN A TABLE AND EXTRACTS VALUES FROM INPUT RASTER
BANDS AT EACH LOCATION - CREATING A TRANSECT PROFILE.

FOR THIS EXAMPLE, WE'RE USING POINTS SPACED 30 M ACROSS AND EXTRACT SENTINEL 2
TOA VALUES FROM SIX BANDS.

THE VALUES ARE OUTPUT AS A DATAFRAME AND EXPORTED TO A CSV.
'''
import pandas as pd
import gdal
import seaborn as sns
import matplotlib.pyplot as plt

bands = ['blue', 'red', 'green', 'nir', 'swir1', 'swir2']

# =============================================================================
# IMPORT YOUR POINTS
# =============================================================================
points = pd.read_csv(r'E:\GitHub\points1table.csv')

# =============================================================================
# SET YOUR WORKING DIRECTORY
# =============================================================================
toaroot = 'E:\\GitHub\\bandstoa\\'
ext = 'toa_clip.tif'

bandlist = []
valuelist = []
distance = []

for band in bands:
    infile = toaroot + band + ext
    openfile = gdal.Open(infile)
    geo = openfile.GetGeoTransform()
    bands = openfile.GetRasterBand(1)
    array = bands.ReadAsArray()

    for index, row in points.iterrows():
            px = int((row['x']-geo[0])/geo[1])
            py = int((row['y']-geo[3])/geo[5])
            print(array[py,px])
            
            valuelist.append(array[py,px])
            bandlist.append(band)
            distance.append(row['distance'])
            
df = pd.DataFrame({'value':valuelist, \
                  'band':bandlist,\
                  'distance':distance})

# =============================================================================
# OUTPUT YOUR DATAFRAME TO CSV OR PLOT USING SEABORN
# =============================================================================
df.to_csv(r'E:\GitHub\TOA_valuelist_p3.csv')

sns.lineplot('distance', 'value', hue= 'band', data = df,lw = 0.2)
plt.ylim(0,1200)
plt.xlim(0,50000)
plt.show()
