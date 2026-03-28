#!/usr/bin/env python3
"""
Download OSM data using Overpass API
Downloads various OSM features around a specified place with a configurable
bounding box. Outputs GeoJSON format.

Reference: https://wiki.openstreetmap.org/wiki/Map_features

Available features:
  ## AMENITY
  - restaurant: amenity=restaurant
  - cafe: amenity=cafe
  - bar: amenity=bar
  - fast_food: amenity=fast_food
  - pub: amenity=pub
  - school: amenity=school
  - university: amenity=university
  - hospital: amenity=hospital
  - pharmacy: amenity=pharmacy
  - bank: amenity=bank
  - atm: amenity=atm
  - parking: amenity=parking
  - fuel: amenity=fuel
  - library: amenity=library
  - cinema: amenity=cinema
  - theatre: amenity=theatre
  - police: amenity=police
  - fire_station: amenity=fire_station
  - post_office: amenity=post_office
  - toilets: amenity=toilets
  - drinking_water: amenity=drinking_water
  
  ## BUILDING
  - building: building=*
  - residential: building=residential
  - commercial: building=commercial
  - industrial: building=industrial
  - church: building=church
  - school: building=school
  - hospital: building=hospital
  - retail: building=retail
  
  ## SHOP
  - supermarket: shop=supermarket
  - convenience: shop=convenience
  - bakery: shop=bakery
  - pharmacy_shop: shop=pharmacy
  - clothes: shop=clothes
  - electronics: shop=electronics
  - restaurant_shop: shop=restaurant
  - cafe_shop: shop=cafe
  
  ## HIGHWAY
  - bus_stop: highway=bus_stop
  - traffic_signals: highway=traffic_signals
  - crosswalk: highway=crosswalk
  - turning_circle: highway=turning_circle
  - mini_roundabout: highway=mini_roundabout
  
  ## LEISURE/TOURISM
  - park: leisure=park
  - playground: leisure=playground
  - sports_centre: leisure=sports_centre
  - swimming_pool: leisure=swimming_pool
  - hotel: tourism=hotel
  - hostel: tourism=hostel
  - museum: tourism=museum
  - attraction: tourism=attraction
  - viewpoint: tourism=viewpoint
  
  ## NATURAL/LANDUSE
  - forest: landuse=forest
  - residential_area: landuse=residential
  - commercial_area: landuse=commercial
  - industrial_area: landuse=industrial
  - retail_area: landuse=retail
  - water: natural=water
  - wood: natural=wood
  - tree: natural=tree
  
  ## RAILWAY
  - railway_station: railway=station
  - tram_stop: railway=tram_stop
  - railway_halt: railway=halt
  
  ## POWER
  - power_tower: power=tower
  - power_pole: power=pole
  - power_plant: power=plant
  - power_substation: power=substation
"""

import argparse
import overpy
import json
import os
import urllib.request
import urllib.parse
import math


# OSM feature definitions with their Overpass queries
# Format: key, value, output_name, is_building, has_nodes
FEATURE_DEFINITIONS = {
    # AMENITY
    'restaurant': {
        'name': 'restaurants',
        'query_template': '''(
            node["amenity"="restaurant"]({south},{west},{north},{east});
            way["amenity"="restaurant"]({south},{west},{north},{east});
            relation["amenity"="restaurant"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'cafe': {
        'name': 'cafes',
        'query_template': '''(
            node["amenity"="cafe"]({south},{west},{north},{east});
            way["amenity"="cafe"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'bar': {
        'name': 'bars',
        'query_template': '''(
            node["amenity"="bar"]({south},{west},{north},{east});
            way["amenity"="bar"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'fast_food': {
        'name': 'fast_food',
        'query_template': '''(
            node["amenity"="fast_food"]({south},{west},{north},{east});
            way["amenity"="fast_food"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'pub': {
        'name': 'pubs',
        'query_template': '''(
            node["amenity"="pub"]({south},{west},{north},{east});
            way["amenity"="pub"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'school': {
        'name': 'schools',
        'query_template': '''(
            node["amenity"="school"]({south},{west},{north},{east});
            way["amenity"="school"]({south},{west},{north},{east});
            relation["amenity"="school"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'university': {
        'name': 'universities',
        'query_template': '''(
            node["amenity"="university"]({south},{west},{north},{east});
            way["amenity"="university"]({south},{west},{north},{east});
            relation["amenity"="university"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'hospital': {
        'name': 'hospitals',
        'query_template': '''(
            node["amenity"="hospital"]({south},{west},{north},{east});
            way["amenity"="hospital"]({south},{west},{north},{east});
            relation["amenity"="hospital"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'pharmacy': {
        'name': 'pharmacies',
        'query_template': '''(
            node["amenity"="pharmacy"]({south},{west},{north},{east});
            way["amenity"="pharmacy"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'bank': {
        'name': 'banks',
        'query_template': '''(
            node["amenity"="bank"]({south},{west},{north},{east});
            way["amenity"="bank"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'atm': {
        'name': 'atms',
        'query_template': '''(
            node["amenity"="atm"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'parking': {
        'name': 'parking',
        'query_template': '''(
            node["amenity"="parking"]({south},{west},{north},{east});
            way["amenity"="parking"]({south},{west},{north},{east});
            relation["amenity"="parking"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'fuel': {
        'name': 'fuel_stations',
        'query_template': '''(
            node["amenity"="fuel"]({south},{west},{north},{east});
            way["amenity"="fuel"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'library': {
        'name': 'libraries',
        'query_template': '''(
            node["amenity"="library"]({south},{west},{north},{east});
            way["amenity"="library"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'cinema': {
        'name': 'cinemas',
        'query_template': '''(
            node["amenity"="cinema"]({south},{west},{north},{east});
            way["amenity"="cinema"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'theatre': {
        'name': 'theatres',
        'query_template': '''(
            node["amenity"="theatre"]({south},{west},{north},{east});
            way["amenity"="theatre"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'police': {
        'name': 'police',
        'query_template': '''(
            node["amenity"="police"]({south},{west},{north},{east});
            way["amenity"="police"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'fire_station': {
        'name': 'fire_stations',
        'query_template': '''(
            node["amenity"="fire_station"]({south},{west},{north},{east});
            way["amenity"="fire_station"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'post_office': {
        'name': 'post_offices',
        'query_template': '''(
            node["amenity"="post_office"]({south},{west},{north},{east});
            way["amenity"="post_office"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'toilets': {
        'name': 'toilets',
        'query_template': '''(
            node["amenity"="toilets"]({south},{west},{north},{east});
            way["amenity"="toilets"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'drinking_water': {
        'name': 'drinking_water',
        'query_template': '''(
            node["amenity"="drinking_water"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'bus_station': {
        'name': 'bus_stations',
        'query_template': '''(
            node["amenity"="bus_station"]({south},{west},{north},{east});
            way["amenity"="bus_station"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    
    # BUILDING
    'building': {
        'name': 'buildings',
        'query_template': '''(
            way["building"]({south},{west},{north},{east});
            relation["building"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': True,
        'has_nodes': False
    },
    'building_residential': {
        'name': 'residential_buildings',
        'query_template': '''(
            way["building"="residential"]({south},{west},{north},{east});
            relation["building"="residential"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': True,
        'has_nodes': False
    },
    'building_commercial': {
        'name': 'commercial_buildings',
        'query_template': '''(
            way["building"="commercial"]({south},{west},{north},{east});
            relation["building"="commercial"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': True,
        'has_nodes': False
    },
    'building_industrial': {
        'name': 'industrial_buildings',
        'query_template': '''(
            way["building"="industrial"]({south},{west},{north},{east});
            relation["building"="industrial"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': True,
        'has_nodes': False
    },
    'building_retail': {
        'name': 'retail_buildings',
        'query_template': '''(
            way["building"="retail"]({south},{west},{north},{east});
            relation["building"="retail"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': True,
        'has_nodes': False
    },
    'building_church': {
        'name': 'churches',
        'query_template': '''(
            way["building"="church"]({south},{west},{north},{east});
            relation["building"="church"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': True,
        'has_nodes': False
    },
    'building_school': {
        'name': 'school_buildings',
        'query_template': '''(
            way["building"="school"]({south},{west},{north},{east});
            relation["building"="school"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': True,
        'has_nodes': False
    },
    'building_hospital': {
        'name': 'hospital_buildings',
        'query_template': '''(
            way["building"="hospital"]({south},{west},{north},{east});
            relation["building"="hospital"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': True,
        'has_nodes': False
    },
    
    # SHOP
    'shop': {
        'name': 'shops',
        'query_template': '''(
            node["shop"]({south},{west},{north},{east});
            way["shop"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'supermarket': {
        'name': 'supermarkets',
        'query_template': '''(
            node["shop"="supermarket"]({south},{west},{north},{east});
            way["shop"="supermarket"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'convenience': {
        'name': 'convenience_stores',
        'query_template': '''(
            node["shop"="convenience"]({south},{west},{north},{east});
            way["shop"="convenience"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'bakery': {
        'name': 'bakeries',
        'query_template': '''(
            node["shop"="bakery"]({south},{west},{north},{east});
            way["shop"="bakery"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'clothes': {
        'name': 'clothes_shops',
        'query_template': '''(
            node["shop"="clothes"]({south},{west},{north},{east});
            way["shop"="clothes"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'electronics': {
        'name': 'electronics_shops',
        'query_template': '''(
            node["shop"="electronics"]({south},{west},{north},{east});
            way["shop"="electronics"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    
    # HIGHWAY
    'bus_stop': {
        'name': 'bus_stops',
        'query_template': '''(
            node["highway"="bus_stop"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'traffic_signals': {
        'name': 'traffic_signals',
        'query_template': '''(
            node["highway"="traffic_signals"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'crosswalk': {
        'name': 'crosswalks',
        'query_template': '''(
            node["highway"="crossing"]({south},{west},{north},{east});
            way["highway"="crossing"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    
    # LEISURE
    'park': {
        'name': 'parks',
        'query_template': '''(
            node["leisure"="park"]({south},{west},{north},{east});
            way["leisure"="park"]({south},{west},{north},{east});
            relation["leisure"="park"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'playground': {
        'name': 'playgrounds',
        'query_template': '''(
            node["leisure"="playground"]({south},{west},{north},{east});
            way["leisure"="playground"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'sports_centre': {
        'name': 'sports_centres',
        'query_template': '''(
            node["leisure"="sports_centre"]({south},{west},{north},{east});
            way["leisure"="sports_centre"]({south},{west},{north},{east});
            relation["leisure"="sports_centre"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'swimming_pool': {
        'name': 'swimming_pools',
        'query_template': '''(
            node["leisure"="swimming_pool"]({south},{west},{north},{east});
            way["leisure"="swimming_pool"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    
    # TOURISM
    'hotel': {
        'name': 'hotels',
        'query_template': '''(
            node["tourism"="hotel"]({south},{west},{north},{east});
            way["tourism"="hotel"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'hostel': {
        'name': 'hostels',
        'query_template': '''(
            node["tourism"="hostel"]({south},{west},{north},{east});
            way["tourism"="hostel"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'museum': {
        'name': 'museums',
        'query_template': '''(
            node["tourism"="museum"]({south},{west},{north},{east});
            way["tourism"="museum"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'attraction': {
        'name': 'attractions',
        'query_template': '''(
            node["tourism"="attraction"]({south},{west},{north},{east});
            way["tourism"="attraction"]({south},{west},{north},{east});
            relation["tourism"="attraction"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'viewpoint': {
        'name': 'viewpoints',
        'query_template': '''(
            node["tourism"="viewpoint"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    
    # LANDUSE
    'landuse_forest': {
        'name': 'forests',
        'query_template': '''(
            way["landuse"="forest"]({south},{west},{north},{east});
            relation["landuse"="forest"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': False
    },
    'landuse_residential': {
        'name': 'residential_areas',
        'query_template': '''(
            way["landuse"="residential"]({south},{west},{north},{east});
            relation["landuse"="residential"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': False
    },
    'landuse_commercial': {
        'name': 'commercial_areas',
        'query_template': '''(
            way["landuse"="commercial"]({south},{west},{north},{east});
            relation["landuse"="commercial"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': False
    },
    'landuse_industrial': {
        'name': 'industrial_areas',
        'query_template': '''(
            way["landuse"="industrial"]({south},{west},{north},{east});
            relation["landuse"="industrial"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': False
    },
    'landuse_retail': {
        'name': 'retail_areas',
        'query_template': '''(
            way["landuse"="retail"]({south},{west},{north},{east});
            relation["landuse"="retail"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': False
    },
    
    # NATURAL
    'water': {
        'name': 'water',
        'query_template': '''(
            way["natural"="water"]({south},{west},{north},{east});
            relation["natural"="water"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': False
    },
    'wood': {
        'name': 'woods',
        'query_template': '''(
            way["natural"="wood"]({south},{west},{north},{east});
            relation["natural"="wood"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': False
    },
    'tree': {
        'name': 'trees',
        'query_template': '''(
            node["natural"="tree"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    
    # RAILWAY
    'railway_station': {
        'name': 'railway_stations',
        'query_template': '''(
            node["railway"="station"]({south},{west},{north},{east});
            way["railway"="station"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'tram_stop': {
        'name': 'tram_stops',
        'query_template': '''(
            node["railway"="tram_stop"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    
    # POWER
    'power_tower': {
        'name': 'power_towers',
        'query_template': '''(
            node["power"="tower"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
    'power_pole': {
        'name': 'power_poles',
        'query_template': '''(
            node["power"="pole"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;''',
        'is_building': False,
        'has_nodes': True
    },
}


def geocode_place(place_name):
    """Geocode a place name to get lat/lon coordinates using Nominatim."""
    encoded_name = urllib.parse.quote(place_name)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_name}&format=json&limit=1"
    
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'OSM-Downloader/1.0'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and len(data) > 0:
                return float(data[0]['lat']), float(data[0]['lon'])
            else:
                raise ValueError(f"Could not geocode place: {place_name}")
    except Exception as e:
        raise ValueError(f"Geocoding error for '{place_name}': {e}")


def calculate_bbox(lat, lon, distance_km):
    """Calculate bounding box from center point and distance.
    
    Args:
        lat: Center latitude
        lon: Center longitude
        distance_km: Distance in kilometers (half-width of the box)
    
    Returns:
        dict with south, west, north, east bounds
    """
    # Approximate degrees per km
    # 1 degree lat ≈ 111 km
    # 1 degree lon ≈ 111 km * cos(lat)
    
    lat_delta = distance_km / 111.0
    lon_delta = distance_km / (111.0 * abs(math.cos(math.radians(lat))))
    
    return {
        'south': lat - lat_delta,
        'west': lon - lon_delta,
        'north': lat + lat_delta,
        'east': lon + lon_delta
    }


def node_to_geojson_feature(node, tags=None):
    """Convert an Overpass node to a GeoJSON Feature."""
    properties = dict(node.tags) if tags is None else tags
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(node.lon), float(node.lat)]
        },
        "properties": properties
    }


def way_to_geojson_feature(way, is_building=False):
    """Convert an Overpass way to a GeoJSON Feature (Polygon or LineString)."""
    coordinates = []
    for node in way.nodes:
        coordinates.append([float(node.lon), float(node.lat)])
    
    if len(coordinates) >= 3:
        if is_building or (coordinates[0] == coordinates[-1]):
            geometry_type = "Polygon"
            if coordinates[0] != coordinates[-1]:
                coordinates.append(coordinates[0])
            geo_coordinates = [coordinates]
        else:
            geometry_type = "LineString"
            geo_coordinates = coordinates
    else:
        geometry_type = "LineString"
        geo_coordinates = coordinates
    
    return {
        "type": "Feature",
        "geometry": {
            "type": geometry_type,
            "coordinates": geo_coordinates
        },
        "properties": dict(way.tags)
    }


def relation_to_geojson_feature(relation):
    """Convert an Overpass relation to a GeoJSON Feature (MultiPolygon or GeometryCollection)."""
    # For relations, we'll create a simplified representation
    # Relations can be complex, so we'll just store the tags and a reference
    properties = dict(relation.tags)
    properties['_type'] = 'relation'
    properties['_id'] = relation.id
    
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [0, 0]  # Placeholder - relations don't have simple geometry
        },
        "properties": properties
    }


def create_geojson_feature_collection(features):
    """Create a GeoJSON FeatureCollection."""
    return {
        "type": "FeatureCollection",
        "features": features
    }


def download_feature(api, bbox, feature_key, config):
    """Download a specific OSM feature type and return GeoJSON features."""
    features = []
    
    # Format the query with bbox values
    query = config['query_template'].format(
        south=bbox['south'],
        west=bbox['west'],
        north=bbox['north'],
        east=bbox['east']
    )
    
    print(f"\nDownloading {config['name']}...")
    try:
        result = api.query(query)
        
        # Process nodes (if applicable)
        if config['has_nodes'] and hasattr(result, 'nodes'):
            print(f"  Found {len(result.nodes)} {config['name']} nodes")
            for node in result.nodes:
                feature = node_to_geojson_feature(node)
                features.append(feature)
        
        # Process ways
        if hasattr(result, 'ways'):
            print(f"  Found {len(result.ways)} {config['name']} ways")
            for way in result.ways:
                feature = way_to_geojson_feature(way, is_building=config['is_building'])
                features.append(feature)
        
        # Process relations
        if hasattr(result, 'relations'):
            print(f"  Found {len(result.relations)} {config['name']} relations")
            for relation in result.relations:
                feature = relation_to_geojson_feature(relation)
                features.append(feature)
        
    except Exception as e:
        print(f"  Error downloading {config['name']}: {e}")
    
    return features


def download_osm_data(place_name, distance_km, features_to_download):
    """Download specified OSM features around a place."""
    
    print(f"Geocoding place: {place_name}...")
    try:
        lat, lon = geocode_place(place_name)
        print(f"  Coordinates: {lat:.6f}, {lon:.6f}")
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Calculate bounding box
    bbox = calculate_bbox(lat, lon, distance_km)
    
    print(f"\nBounding box ({distance_km}km x {distance_km}km):")
    print(f"  South: {bbox['south']:.6f}")
    print(f"  West:  {bbox['west']:.6f}")
    print(f"  North: {bbox['north']:.6f}")
    print(f"  East:  {bbox['east']:.6f}")
    
    # Initialize Overpass API
    overpass_url = "https://overpass-api.de/api/interpreter"
    api = overpy.Overpass(url=overpass_url)
    
    # Download each feature type
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Create safe filename prefix from place name
    safe_place = place_name.replace(' ', '_').replace('/', '_').lower()
    
    total_features = 0
    
    for feature_key in features_to_download:
        if feature_key not in FEATURE_DEFINITIONS:
            print(f"\nWarning: Unknown feature '{feature_key}', skipping...")
            print(f"  Use --list-features to see available features")
            continue
        
        config = FEATURE_DEFINITIONS[feature_key]
        features = download_feature(api, bbox, feature_key, config)
        
        # Save data to GeoJSON file
        if features:
            geojson = create_geojson_feature_collection(features)
            filepath = os.path.join(data_dir, f"{safe_place}_{config['name']}.geojson")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(geojson, f, indent=2, ensure_ascii=False)
            print(f"  Saved {len(features)} {config['name']} to {filepath}")
            total_features += len(features)
    
    print(f"\nDone! Downloaded {total_features} total features.")


def list_features():
    """Print a list of all available features."""
    print("\nAvailable OSM features:\n")
    print("=" * 60)
    
    categories = {
        'AMENITY': ['restaurant', 'cafe', 'bar', 'fast_food', 'pub', 'school', 'university', 
                    'hospital', 'pharmacy', 'bank', 'atm', 'parking', 'fuel', 'library',
                    'cinema', 'theatre', 'police', 'fire_station', 'post_office', 'toilets',
                    'drinking_water', 'bus_station'],
        'BUILDING': ['building', 'building_residential', 'building_commercial', 'building_industrial',
                     'building_retail', 'building_church', 'building_school', 'building_hospital'],
        'SHOP': ['shop', 'supermarket', 'convenience', 'bakery', 'clothes', 'electronics'],
        'HIGHWAY': ['bus_stop', 'traffic_signals', 'crosswalk'],
        'LEISURE': ['park', 'playground', 'sports_centre', 'swimming_pool'],
        'TOURISM': ['hotel', 'hostel', 'museum', 'attraction', 'viewpoint'],
        'LANDUSE': ['landuse_forest', 'landuse_residential', 'landuse_commercial', 
                    'landuse_industrial', 'landuse_retail'],
        'NATURAL': ['water', 'wood', 'tree'],
        'RAILWAY': ['railway_station', 'tram_stop'],
        'POWER': ['power_tower', 'power_pole'],
    }
    
    for category, features in categories.items():
        print(f"\n{category}:")
        print("-" * 60)
        for feature in features:
            if feature in FEATURE_DEFINITIONS:
                config = FEATURE_DEFINITIONS[feature]
                print(f"  {feature:25} -> {config['name']}")
    
    print("\n" + "=" * 60)
    print("\nDefault features (if none specified): restaurant, building")


def main():
    parser = argparse.ArgumentParser(
        description='Download OSM data around a place. By default downloads restaurants and buildings.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  # Download default features (restaurant + building)
  python download_osm_using_overpass.py -p "Manila"

  # Download only cafes
  python download_osm_using_overpass.py -p "Manila" -f cafe

  # Download multiple specific features
  python download_osm_using_overpass.py -p "Manila" -f restaurant cafe bank

  # List all available features
  python download_osm_using_overpass.py --list-features

  # Download all restaurants, buildings, and schools
  python download_osm_using_overpass.py -p "Manila" -f restaurant building school
'''
    )
    parser.add_argument(
        '-p', '--place',
        type=str,
        default='De La Salle University Manila',
        help='Name of the place to center the search on (default: "De La Salle University Manila")'
    )
    parser.add_argument(
        '-d', '--distance',
        type=float,
        default=1.0,
        help='Distance in kilometers for the bounding box (default: 1.0)'
    )
    parser.add_argument(
        '-f', '--features',
        nargs='+',
        default=['restaurant', 'building'],
        help='OSM features to download. Defaults: restaurant building'
    )
    parser.add_argument(
        '-l', '--list-features',
        action='store_true',
        help='List all available features and exit'
    )
    
    args = parser.parse_args()
    
    if args.list_features:
        list_features()
        return
    
    download_osm_data(args.place, args.distance, args.features)


if __name__ == "__main__":
    main()
