# OSM Data Downloader with Overpass Turbo

A Python script to download OpenStreetMap (OSM) data using the Overpass API. It downloads various OSM features (restaurants, buildings, cafes, shops, etc.) around a specified location with a configurable bounding box, outputting data in GeoJSON format.

## What are OSM, Nominatim, and Overpass?

### OpenStreetMap (OSM)
OpenStreetMap is a free, editable map of the world built by volunteers. It's like the Wikipedia of maps—anyone can view, edit, and use the data. OSM contains detailed information about roads, buildings, points of interest, and more.

### Nominatim
Nominatim is a geocoding service that converts place names (like "De La Salle University Manila") into geographic coordinates (latitude and longitude). It uses OpenStreetMap data to find locations worldwide.

### Overpass API
The Overpass API is a read-only API that lets you query OpenStreetMap data with powerful filters. You can extract specific features like restaurants, buildings, or roads within a specific area using a query language called Overpass QL.

## Features

- Geocodes place names to coordinates using Nominatim
- Downloads various OSM features within a specified distance from the center point
- Outputs data in GeoJSON format
- Configurable via command-line arguments
- Supports **60+ feature types** across **10 categories**

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python download_osm_using_overpass.py [OPTIONS]
```

### Parameters

| Flag | Long Form | Description | Default |
|------|-----------|-------------|---------|
| `-p` | `--place` | Name of the place to center the search on | "De La Salle University Manila" |
| `-d` | `--distance` | Distance in kilometers for the bounding box (half-width from center) | 1.0 |
| `-f` | `--features` | Space-separated list of features to download | restaurant building |
| `-l` | `--list-features` | List all available features and exit | - |

### Examples

#### Use default settings (DLSU Manila, 1km × 1km)

```bash
python download_osm_using_overpass.py
```

#### Download around Mall of Asia with 2km bounding box

```bash
python download_osm_using_overpass.py -p "Mall of Asia" -d 2
```

#### Download around a specific location with default distance

```bash
python download_osm_using_overpass.py --place "University of the Philippines Diliman"
```

#### Download specific features

```bash
# Download only cafes
python download_osm_using_overpass.py -p "Manila" -f cafe

# Download multiple features
python download_osm_using_overpass.py -p "Manila" -f restaurant cafe school hospital

# Download all available features
python download_osm_using_overpass.py -p "Manila" -f restaurant building cafe bar fast_food pub school university hospital pharmacy bank atm parking fuel library cinema theatre police fire_station post_office toilets drinking_water bus_station building_residential building_commercial building_industrial building_retail building_church building_school building_hospital shop supermarket convenience bakery clothes electronics bus_stop traffic_signals crosswalk park playground sports_centre swimming_pool hotel hostel museum attraction viewpoint landuse_forest landuse_residential landuse_commercial landuse_industrial landuse_retail water wood tree railway_station tram_stop power_tower power_pole
```

#### List all available features

```bash
python download_osm_using_overpass.py --list-features
```

#### Short flags

```bash
python download_osm_using_overpass.py -p "Manila City Hall" -d 0.5
```

#### Show help

```bash
python download_osm_using_overpass.py --help
```

## Available Features

The script supports **60+ OSM feature types** across **10 categories**. Use the feature name with the `-f` flag.

### AMENITY (Sustenance, Education, Healthcare, Transportation, Financial, Public Service)

| Feature | Description |
|---------|-------------|
| `restaurant` | Restaurants |
| `cafe` | Cafes and coffee shops |
| `bar` | Bars |
| `fast_food` | Fast food restaurants |
| `pub` | Pubs |
| `school` | Schools (primary, middle, secondary) |
| `university` | University campuses |
| `hospital` | Hospitals |
| `pharmacy` | Pharmacies |
| `bank` | Banks |
| `atm` | ATMs and cash points |
| `parking` | Parking areas |
| `fuel` | Gas/petrol stations |
| `library` | Libraries |
| `cinema` | Cinemas and movie theaters |
| `theatre` | Theaters |
| `police` | Police stations |
| `fire_station` | Fire stations |
| `post_office` | Post offices |
| `toilets` | Public toilets |
| `drinking_water` | Drinking water points |
| `bus_station` | Bus stations |

### BUILDING

| Feature | Description |
|---------|-------------|
| `building` | All buildings (any type) |
| `building_residential` | Residential buildings |
| `building_commercial` | Commercial buildings |
| `building_industrial` | Industrial buildings |
| `building_retail` | Retail buildings |
| `building_church` | Churches and religious buildings |
| `building_school` | School buildings |
| `building_hospital` | Hospital buildings |

### SHOP

| Feature | Description |
|---------|-------------|
| `shop` | All shops (any type) |
| `supermarket` | Supermarkets |
| `convenience` | Convenience stores |
| `bakery` | Bakeries |
| `clothes` | Clothing stores |
| `electronics` | Electronics stores |

### HIGHWAY (Transportation Infrastructure)

| Feature | Description |
|---------|-------------|
| `bus_stop` | Bus stops |
| `traffic_signals` | Traffic lights |
| `crosswalk` | Pedestrian crossings |

### LEISURE

| Feature | Description |
|---------|-------------|
| `park` | Parks and green spaces |
| `playground` | Playgrounds |
| `sports_centre` | Sports centers |
| `swimming_pool` | Swimming pools |

### TOURISM

| Feature | Description |
|---------|-------------|
| `hotel` | Hotels |
| `hostel` | Hostels |
| `museum` | Museums |
| `attraction` | Tourist attractions |
| `viewpoint` | Scenic viewpoints |

### LANDUSE

| Feature | Description |
|---------|-------------|
| `landuse_forest` | Forest areas |
| `landuse_residential` | Residential areas |
| `landuse_commercial` | Commercial zones |
| `landuse_industrial` | Industrial zones |
| `landuse_retail` | Retail zones |

### NATURAL

| Feature | Description |
|---------|-------------|
| `water` | Lakes, rivers, ponds |
| `wood` | Wooded areas |
| `tree` | Individual trees |

### RAILWAY

| Feature | Description |
|---------|-------------|
| `railway_station` | Train stations |
| `tram_stop` | Tram stops |

### POWER

| Feature | Description |
|---------|-------------|
| `power_tower` | Electricity transmission towers |
| `power_pole` | Utility poles |

## Output

The script creates a `data/` directory and saves GeoJSON files for each requested feature type:

- `{place_name}_{feature_name}.geojson`

Where `{place_name}` is the sanitized version of the place name (lowercase, spaces replaced with underscores).

**Example output files:**
```
data/
├── de_la_salle_university_manila_restaurants.geojson
├── de_la_salle_university_manila_buildings.geojson
├── de_la_salle_university_manila_cafes.geojson
└── de_la_salle_university_manila_parking.geojson
```

## Data Types

### Nodes
- Converted to GeoJSON Points
- Example: bus stops, ATMs, trees, drinking water points

### Ways
- Converted to GeoJSON Polygons or LineStrings
- Example: buildings, parks, roads

### Relations
- Simplified representation (stores tags and reference)
- Example: large areas, complex buildings

## Bounding Box Calculation

The script calculates the bounding box from the center coordinates:
- **1° latitude ≈ 111 km**
- **1° longitude ≈ 111 km × cos(latitude)**

For a distance of `d` km, the bounding box extends `d` km in each direction from the center point.

## Requirements

- Python 3.6+
- `overpy` library
- Internet connection (for geocoding and Overpass API)

## API Sources

- **Geocoding**: Nominatim (OpenStreetMap)
- **OSM Data**: Overpass API

## Notes

- Be respectful of the Overpass API rate limits
- Large distance values may result in longer download times
- Place names are sent to Nominatim for geocoding
- The script requires an active internet connection
- Default features are **restaurant** and **building** if `-f` is not specified

## Troubleshooting

**Error: Could not geocode place**
- Try a more specific place name
- Check your internet connection
- Ensure the place exists in OpenStreetMap

**Error: Download timeout**
- Try a smaller distance value
- Check your internet connection
- The Overpass API may be temporarily unavailable

**No results found**
- The area may have no mapped features of the requested type in OpenStreetMap
- Try increasing the distance value
- Try a different location
- Try different feature types

**Unknown feature error**
- Use `--list-features` to see all available feature names
- Check the feature name spelling
