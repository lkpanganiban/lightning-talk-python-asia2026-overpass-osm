# OSM Data Downloader with Overpass Turbo

A Python script to download OpenStreetMap (OSM) data using the Overpass API. It downloads restaurant points of interest and buildings around a specified location with a configurable bounding box, outputting data in GeoJSON format.

## What are OSM, Nominatim, and Overpass?

### OpenStreetMap (OSM)
OpenStreetMap is a free, editable map of the world built by volunteers. It's like the Wikipedia of maps—anyone can view, edit, and use the data. OSM contains detailed information about roads, buildings, points of interest, and more.

### Nominatim
Nominatim is a geocoding service that converts place names (like "De La Salle University Manila") into geographic coordinates (latitude and longitude). It uses OpenStreetMap data to find locations worldwide.

### Overpass API
The Overpass API is a read-only API that lets you query OpenStreetMap data with powerful filters. You can extract specific features like restaurants, buildings, or roads within a specific area using a query language called Overpass QL.

## Features

- Geocodes place names to coordinates using Nominatim
- Downloads restaurants and buildings within a specified distance from the center point
- Outputs data in GeoJSON format
- Configurable via command-line arguments

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

#### Short flags

```bash
python download_osm_using_overpass.py -p "Manila City Hall" -d 0.5
```

#### Show help

```bash
python download_osm_using_overpass.py --help
```

## Output

The script creates a `data/` directory and saves two GeoJSON files:

- `{place_name}_restaurants.geojson` - Restaurant points and areas
- `{place_name}_buildings.geojson` - Building polygons

Where `{place_name}` is the sanitized version of the place name (lowercase, spaces replaced with underscores).

**Example output files:**
```
data/
├── de_la_salle_university_manila_restaurants.geojson
└── de_la_salle_university_manila_buildings.geojson
```

## Data Types

### Restaurants
- **Nodes**: Converted to GeoJSON Points
- **Ways**: Converted to GeoJSON Polygons or LineStrings

### Buildings
- **Ways**: Converted to GeoJSON Polygons

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
- The area may have no mapped restaurants/buildings in OpenStreetMap
- Try increasing the distance value
- Try a different location
