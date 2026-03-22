#!/usr/bin/env python3
"""
Download OSM data using Overpass API
Downloads restaurant POIs and buildings around a specified place
with a configurable bounding box. Outputs GeoJSON format.
"""

import argparse
import overpy
import json
import os
import urllib.request
import urllib.parse
import math


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


def create_geojson_feature_collection(features):
    """Create a GeoJSON FeatureCollection."""
    return {
        "type": "FeatureCollection",
        "features": features
    }


def download_osm_data(place_name, distance_km):
    """Download restaurant POIs and buildings around a specified place."""
    
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
    print()
    
    # Initialize Overpass API
    overpass_url = "https://overpass-api.de/api/interpreter"
    api = overpy.Overpass(url=overpass_url)
    
    # Query for restaurants
    restaurant_query = f"""
    (
        node["amenity"="restaurant"]({bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']});
        way["amenity"="restaurant"]({bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']});
    );
    out body;
    >;
    out skel qt;
    """
    
    # Query for buildings
    building_query = f"""
    (
        way["building"]({bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']});
    );
    out body;
    >;
    out skel qt;
    """
    
    # Download restaurants
    print("Downloading restaurants...")
    restaurant_features = []
    try:
        restaurants_result = api.query(restaurant_query)
        print(f"  Found {len(restaurants_result.nodes)} restaurant nodes")
        print(f"  Found {len(restaurants_result.ways)} restaurant ways")
        
        for node in restaurants_result.nodes:
            feature = node_to_geojson_feature(node)
            restaurant_features.append(feature)
        
        for way in restaurants_result.ways:
            feature = way_to_geojson_feature(way, is_building=False)
            restaurant_features.append(feature)
            
    except Exception as e:
        print(f"  Error downloading restaurants: {e}")
    
    # Download buildings
    print("\nDownloading buildings...")
    building_features = []
    try:
        buildings_result = api.query(building_query)
        print(f"  Found {len(buildings_result.ways)} building ways")
        
        for way in buildings_result.ways:
            feature = way_to_geojson_feature(way, is_building=True)
            building_features.append(feature)
            
    except Exception as e:
        print(f"  Error downloading buildings: {e}")
    
    # Save data to GeoJSON files
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Create safe filename prefix from place name
    safe_place = place_name.replace(' ', '_').replace('/', '_').lower()
    
    # Save restaurants
    if restaurant_features:
        restaurants_geojson = create_geojson_feature_collection(restaurant_features)
        filepath = os.path.join(data_dir, f'{safe_place}_restaurants.geojson')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(restaurants_geojson, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(restaurant_features)} restaurants to {filepath}")
    
    # Save buildings
    if building_features:
        buildings_geojson = create_geojson_feature_collection(building_features)
        filepath = os.path.join(data_dir, f'{safe_place}_buildings.geojson')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(buildings_geojson, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(building_features)} buildings to {filepath}")
    
    print("\nDone!")


def main():
    parser = argparse.ArgumentParser(
        description='Download OSM restaurant and building data around a place.'
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
    
    args = parser.parse_args()
    
    download_osm_data(args.place, args.distance)


if __name__ == "__main__":
    main()
