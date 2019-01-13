#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:08:10 2018

@author: calebpan
"""


"""
Caleb G. Pan
Unviersity of Montana
Numerical Terradynamic Simulation Group
Missoula, MT, USA
caleb.pan@mso.umt.edu

THE PURPOSE OF THIS SCRIPT IT TO BATCH PROCESS X NUMBER OF POINT SHAPEFILES
AND CREATE A DEFINED BUFFERED REGION.

IT IS HELPFUL TO USE THE Feature_to_Shp.py SCRIPT IN CONJUNCTION.

"""
import glob,os

#==============================================================================

#==============================================================================
# DEFINE YOUR OUTFOLDER
#==============================================================================
outfolder = '/anx_lagr2/caleb/GitHub/data/Buffer_wmo/'

#==============================================================================
# USING OGR CREATE 50 KM BUFFER AROUND EACH CLIMATE POINT AND EXPORT TO NEW SHP
#==============================================================================
for files in glob.glob(outfolder + '*'):
    
    if files.endswith('shp'):
#==============================================================================
#         INDEX THE STRING TO EXTRACT THE STATION NAME
#==============================================================================
        station = files[32:-4]
#==============================================================================
#         SET THE OUTFILE NAME
#==============================================================================
        outfiles = outfolder + station + '50kmbuffer.shp'
        infiles = files
        command = 'ogr2ogr ' + outfiles + ' ' + infiles + ' ' + station + \
        ' -dialect sqlite -sql "SELECT ST_Buffer( geometry , 50000 ),* FROM ' \
        + "'" +station +"'" + '"' 
        
#==============================================================================
#         CALL THE COMMAND
#==============================================================================
        os.system(command)        
