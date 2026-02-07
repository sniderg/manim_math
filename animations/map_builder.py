import json
import numpy as np
from manim import *

class MapBuilder:
    def __init__(self, geojson_path):
        with open(geojson_path, "r") as f:
            self.data = json.load(f)
        
        # Determine bounds to center the map
        self.min_lat = 90
        self.max_lat = -90
        self.min_lon = 180
        self.max_lon = -180
        
        self._calculate_bounds()
        
        # Center of the map in Lat/Lon
        self.center_lat = (self.min_lat + self.max_lat) / 2
        self.center_lon = (self.min_lon + self.max_lon) / 2
        
        # Scale factor (approximate, to fit in Manim frame)
        # Frame height is 8.0
        lat_span = self.max_lat - self.min_lat
        lon_span = self.max_lon - self.min_lon
        
        # Scale to match frame height roughly
        self.scale = 7.0 / max(lat_span, lon_span)  

    def _calculate_bounds(self):
        def update_bounds(coords):
            # coords is list of [lon, lat]
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            self.min_lon = min(self.min_lon, min(lons))
            self.max_lon = max(self.max_lon, max(lons))
            self.min_lat = min(self.min_lat, min(lats))
            self.max_lat = max(self.max_lat, max(lats))

        for feature in self.data['features']:
            geometry = feature['geometry']
            coords = geometry['coordinates']
            geo_type = geometry['type']
            
            if geo_type == 'Polygon':
                for ring in coords:
                    update_bounds(ring)
            elif geo_type == 'MultiPolygon':
                for polygon in coords:
                    for ring in polygon:
                        update_bounds(ring)

    def lat_lon_to_point(self, lat, lon):
        # Simple Equirectangular projection relative to center
        # x = (lon - lon0) * cos(lat0)
        # y = (lat - lat0)
        
        x = (lon - self.center_lon) * np.cos(np.radians(self.center_lat))
        y = (lat - self.center_lat)
        
        return np.array([x * self.scale, y * self.scale, 0])

    def build_map_mobjects(self, fill_color='#1c1c1c', stroke_color='#444444', stroke_width=2):
        sw = stroke_width
        group = VGroup()
        
        for feature in self.data['features']:
            geometry = feature['geometry']
            coords = geometry['coordinates']
            geo_type = geometry['type']
            
            polys = []
            if geo_type == 'Polygon':
                polys = [coords]
            elif geo_type == 'MultiPolygon':
                polys = coords
                
            for poly_coords in polys:
                # Exterior ring is first
                exterior = poly_coords[0]
                points = [self.lat_lon_to_point(c[1], c[0]) for c in exterior]
                
                # Manim Polygon
                poly = Polygon(*points, color=stroke_color, stroke_width=sw)
                poly.set_fill(fill_color, opacity=1)
                group.add(poly)
                
                # Interior rings (holes) - Manim Polygon doesn't support holes natively easily 
                # without Cutout, but for a base map simply drawing them on top 
                # in background color might work, or just ignoring small lakes.
                # For now, we render just the main landmass shapes.
                
        return group
