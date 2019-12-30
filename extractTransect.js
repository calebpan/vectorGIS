//THE PURPOSE OF THIS SCRIPT IS TO CREATE A TRANSECT, DEFINED BY A SHAPEFILE TO
// VISUALIZE THE SPECTRAL VARIABILITY ALONG A SPATIAL GRADIENT.
// THE SCRIPT REQUIRES ONLY AN INPUT POINT SHAPEFILE WITH A COLUMN CALLED 'distance', 
// THIS COLUMN IS A CUMULATIVE SUMMMATION, PREDICATED ON THE SPATIAL RESOULTION OF
// THE INPUT IMAGES (HERE ITS 30 M). 
Map.centerObject(fulltransect);
Map.addLayer(fulltransect, {}, 'Point Transect')

// SUBSET POINT TRANSECT TO BE LESS THAN 5000 POINTS. WE USE THE 'distance' COLUMN TO DO THIS
var shp = fulltransect.filter(ee.Filter.lte('distance', 149000)).sort('distance'); //149000 is closest to 5k
print(shp.size(),'sub size'); //make sure length is less than 5000

// SET VARIABLES
var start = '2019-08-29';
var end = '2019-08-30';
var coll = 'COPERNICUS/S2_SR';
var ylabel = 'Surface Reflectance';

// CREATE IMAGE COLLECTION
var s2coll = ee.ImageCollection(coll)
  .filterDate(start, end)
  .filterBounds(pow);

// MOSAIC COLLECTIONS
var s2 = s2coll.mosaic();

// EXTRACT BANDS
var blue = s2.select('B2');
var green = s2.select('B3');
var red = s2.select('B4');
var nir = s2.select('B8');
var swir = s2.select('B11');
var swir2 = s2.select('B12');

// EXTRACT VALUES AT POINTS
var outcoll = ee.FeatureCollection(shp.map(function(ft){
    var bluestats = blue.reduceRegion({
      reducer: ee.Reducer.median(),
      geometry: ft.geometry(),
      scale: 400,
      crs: 'EPSG:4326'
    });
    var greenstats = green.reduceRegion({
      reducer: ee.Reducer.median(),
      geometry: ft.geometry(),
      scale: 400,
      crs: 'EPSG:4326'
    });
    var redstats = red.reduceRegion({
      reducer: ee.Reducer.median(),
      geometry: ft.geometry(),
      scale: 400,
      crs: 'EPSG:4326'
    });
    var nirstats = nir.reduceRegion({
      reducer: ee.Reducer.median(),
      geometry: ft.geometry(),
      scale: 400,
      crs: 'EPSG:4326'
    });
    var swirstats = swir.reduceRegion({
      reducer: ee.Reducer.median(),
      geometry: ft.geometry(),
      scale: 400,
      crs: 'EPSG:4326'
    });
    var swir2stats = swir2.reduceRegion({
      reducer: ee.Reducer.median(),
      geometry: ft.geometry(),
      scale: 400,
      crs: 'EPSG:4326'
    });
    var stats = ee.Feature(null, {
      'Blue': bluestats.get('B2'),
      'Green': greenstats.get('B3'),
      'Red': redstats.get('B4'),
      'NIR': nirstats.get('B8'),
      'SWIR': swirstats.get('B11'),
      'SWIR2': swir2stats.get('B12'),
      'Distance':ft.get('distance')
    });
    return stats;
  }));
print(outcoll);

// SET PLOT OPTIONS AND PLOT TRANSECT
var options = {
  title: '',
  hAxis: {title: 'Distance [m]'},
  vAxis: {title: ylabel},
};

var chart = ui.Chart.feature.byFeature(outcoll, 'Distance')
  .setChartType('LineChart')
  .setOptions(options);
print(chart,'chart');