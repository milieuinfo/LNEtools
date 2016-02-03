import sys, os

def findOGRtype(fName):
      ext = os.path.splitext( fName )[1]
      if "SHP" in ext.upper():
        flType = "ESRI Shapefile"
      elif "GPKG" in ext.upper():
        flType = "GPKG"
      elif "SQLITE" in ext.upper():
        flType = "SQLite"
      elif "JSON" in ext.upper():
        flType = "GeoJSON"
      elif "GML" in ext.upper():
        flType = "GML"
      elif 'TAB' in ext.upper():
        flType = 'MapInfo File'
      elif 'KML' in ext.upper():
        flType = 'KML'
      elif 'DXF' in ext.upper():
        flType = 'DXF'
      elif 'CSV' in ext.upper():
        flType = 'CSV'
      else:
        flType = "ESRI Shapefile"
      return  flType