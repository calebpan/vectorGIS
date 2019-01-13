#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 09:05:44 2018

@author: calebpan
"""

"""
Caleb G. Pan
Unviersity of Montana
Numerical Terradynamic Simulation Group
Missoula, MT, USA
caleb.pan@mso.umt.edu

IT IS OFTEN THE CASE THAT YOU HAVE A SHAPEFILE THAT IS COMPRISED OF MANY 
FEATURES. SOMETIMES IT IS EASIER TO WORK WITH EACH FEATURE IF IT IS ITS OWN
SHAPEFILE, HOWEVER TO GET THESE FEATURE TO A SHAPEFILE CAN BE MANUALLY TAXING.

THE PURPOSE OF THIS SCRIPT IS TO ITERATE THROUGH A SHAPEFILE THAT HAS MANY
FEATURES AND TO EXPORT EACH FEATURE TO ITS OWN SHAPEFILE USING ITS PROPERTIES.

"""

#==============================================================================
# IMPORT FIONA AND GLOB
#==============================================================================
import fiona,glob

#==============================================================================
# IN THIS EXAMPLE, WE ARE USING A POINT SHP THAT HAS BEEN BUFFERED TO 50 KM.
# THE SHP IS MADE OF 50 FEATURES, EACH REPRESENTING A WMO STATION IN MONGOLIA
#==============================================================================

shp = '/anx_lagr2/caleb/GitHub/WMO_50km_buffer.shp'
outfoldershp = '/anx_lagr2/caleb/GitHub//Buffer_wmo/'
wmo = fiona.open(shp)
for i in range((len(wmo))):
    with fiona.drivers():
        with fiona.open(shp) as src:
            meta = src.meta ##GET EACH FEATURE'S METADATA
            
            z= src[i] ## i REPRESENTS THE NUMERIC INDEX OF THE SHP
            wmoname = z['properties']['station'] ## EXTARCT THE WMO STATION NAME
            
        name = wmoname
#==============================================================================
#         WRITE OUT THE FEATURE (z) TO SHP ASSIGN THE META DATA, AND NAME THE
#         FILE USING THE WMO NAME
#==============================================================================
        with fiona.open(outfoldershp,'w',layer = name,**meta) as dst:
            dst.write(z)
        del name, z


count = []           
for files in glob.glob(outfoldershp + '*'):
    if files.endswith('shp'):
        count.append(files)
print len(count)

