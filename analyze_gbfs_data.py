#!/usr/bin/env python3
"""
Analyze Columbus GBFS snapshots to generate demand forecast patterns.

Processes historical GBFS CSV snapshots to extract:
- Hourly availability patterns
- Day-of-week effects
- Geographic demand distribution
- Vehicle type splits

Outputs JSON data suitable for consumption by forecast.html dashboard.
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import statistics

def parse_timestamp(filename):
    """Extract datetime from filename like columbus_scooters_20260807T203100Z.csv"""
    parts = filename.split('_')
    if len(parts) >= 3:
        ts_str = parts[2].replace('.csv', '')
        try:
            return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        except:
            return None
    return None

def load_snapshots(snapshots_dir):
    """Load all GBFS CSV snapshots and return data grouped by hour."""
    snapshots_dir = Path(snapshots_dir)

    hourly_data = defaultdict(lambda: {
        'available_count': 0,
        'total_count': 0,
        'disabled_count': 0,
        'reserved_count': 0,
        'by_type': defaultdict(int),
        'by_company': defaultdict(int),
        'locations': [],
        'timestamps': []
    })

    daily_data = defaultdict(lambda: {
        'available_count': 0,
        'total_count': 0,
        'snapshots': 0
    })

    csv_files = sorted(snapshots_dir.glob('columbus_scooters_*.csv'))

    print(f"Found {len(csv_files)} GBFS snapshots")

    for csv_file in csv_files[:60]:  # Limit to last 60 snapshots (~30 days at 2× daily)
        ts = parse_timestamp(csv_file.name)
        if not ts:
            continue

        hour_key = ts.strftime('%A_%H')  # "Monday_08", "Tuesday_14", etc.
        day_key = ts.strftime('%Y-%m-%d')

        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    is_available = row.get('Is_Available', 'False') == 'True'
                    is_disabled = row.get('Is_Disabled', 'False') == 'True'
                    is_reserved = row.get('Is_Reserved', 'False') == 'True'
                    vehicle_type = row.get('Type', 'unknown').lower()
                    company = row.get('Company', 'unknown')

                    # Aggregate hourly
                    hourly_data[hour_key]['total_count'] += 1
                    if is_available:
                        hourly_data[hour_key]['available_count'] += 1
                    if is_disabled:
                        hourly_data[hour_key]['disabled_count'] += 1
                    if is_reserved:
                        hourly_data[hour_key]['reserved_count'] += 1

                    hourly_data[hour_key]['by_type'][vehicle_type] += 1
                    hourly_data[hour_key]['by_company'][company] += 1

                    # Store location for geographic analysis
                    try:
                        lat = float(row.get('Latitude', 0))
                        lon = float(row.get('Longitude', 0))
                        if lat and lon:
                            hourly_data[hour_key]['locations'].append((lat, lon))
                    except:
                        pass

                    # Aggregate daily
                    daily_data[day_key]['total_count'] += 1
                    if is_available:
                        daily_data[day_key]['available_count'] += 1

                hourly_data[hour_key]['timestamps'].append(ts.isoformat())
                daily_data[day_key]['snapshots'] += 1

        except Exception as e:
            print(f"Error reading {csv_file.name}: {e}")
            continue

    return dict(hourly_data), dict(daily_data)

def generate_forecast_patterns(hourly_data):
    """Convert hourly aggregates into 24-hour demand forecast patterns."""

    # Map hour keys back to hour numbers
    patterns = {}
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for day_name in day_names:
        day_pattern = []

        for hour in range(24):
            hour_key = f"{day_name}_{hour:02d}"
            data = hourly_data.get(hour_key, {})

            if data.get('total_count', 0) > 0:
                # Infer demand from availability ratio
                # Higher availability often means less demand (more vehicles parked/available)
                # Lower availability means more vehicles in use (high demand)
                availability_ratio = data['available_count'] / data['total_count']
                disabled_ratio = data['disabled_count'] / data['total_count']

                # Inverse availability as proxy for demand (used vehicles = demand)
                demand_proxy = (1 - availability_ratio) * 100

                # Normalize to typical trip patterns (0-400 range)
                # Apply smoothing based on day type
                if day_name in ['Saturday', 'Sunday']:
                    demand = demand_proxy * 1.5  # Weekend boost
                else:
                    demand = demand_proxy * 1.2

                demand = max(30, min(400, demand))  # Clamp to realistic range
            else:
                # Estimate based on typical patterns
                if 6 <= hour < 10 or 16 <= hour < 19:
                    demand = 280 * (1.3 if day_name in ['Saturday', 'Sunday'] else 1.0)
                elif 10 <= hour < 16:
                    demand = 150
                elif 19 <= hour < 22:
                    demand = 200
                else:
                    demand = 40

            snapshot_count = len(data.get('timestamps', []))
            confidence = min(0.95, 0.70 + (snapshot_count * 0.05))  # More snapshots = higher confidence

            day_pattern.append({
                'hour': f"{hour:02d}:00",
                'demand': round(demand),
                'confidence': round(confidence, 2),
                'sample_size': data.get('total_count', 0)
            })

        # Smooth the pattern using moving average
        if day_pattern:
            for i in range(len(day_pattern)):
                neighbors = []
                for j in range(max(0, i-1), min(len(day_pattern), i+2)):
                    neighbors.append(day_pattern[j]['demand'])
                day_pattern[i]['demand'] = round(statistics.mean(neighbors))

        patterns[day_name] = day_pattern

    return patterns

def analyze_geographic_demand(hourly_data):
    """Identify geographic hotspots from location data."""

    # Simplified zone mapping based on Columbus geography
    zones = {
        'Downtown Core': {'bounds': (40.7576, 40.7476, -83.0014, -82.9914)},  # High St / 3rd St
        'University District': {'bounds': (40.0050, 39.9850, -83.0100, -82.9900)},  # OSU area
        'Transit Hubs': {'bounds': (40.0000, 39.9700, -82.9900, -82.9600)},  # COTA central
        'Residential North': {'bounds': (40.1000, 40.0500, -83.0500, -82.9500)},
        'Residential East': {'bounds': (40.0000, 39.9500, -82.9000, -82.8500)},
    }

    # Aggregate all locations from hourly data
    all_locations = []
    for data in hourly_data.values():
        all_locations.extend(data.get('locations', []))

    geographic_demand = {}
    for zone_name, zone_info in zones.items():
        min_lat, max_lat, min_lon, max_lon = zone_info['bounds']
        count = sum(1 for lat, lon in all_locations
                   if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon)
        geographic_demand[zone_name] = count

    # Normalize to percentages
    total = sum(geographic_demand.values())
    if total > 0:
        geographic_demand = {k: round((v / total) * 100, 1)
                           for k, v in geographic_demand.items()}

    return geographic_demand

def main():
    # Path to snapshots
    snapshots_dir = Path('/workspace/steveneedham/columbus-micromobility-data/snapshots')

    if not snapshots_dir.exists():
        print(f"Error: Snapshots directory not found at {snapshots_dir}")
        return

    print("Analyzing GBFS snapshots...")
    hourly_data, daily_data = load_snapshots(snapshots_dir)

    print("Generating forecast patterns...")
    patterns = generate_forecast_patterns(hourly_data)

    print("Analyzing geographic demand...")
    geographic = analyze_geographic_demand(hourly_data)

    # Compile output
    output = {
        'analysis_date': datetime.utcnow().isoformat() + 'Z',
        'snapshot_count': len(list(snapshots_dir.glob('columbus_scooters_*.csv'))),
        'hourly_patterns': patterns,
        'geographic_demand': geographic,
        'summary': {
            'days_analyzed': len(daily_data),
            'total_observations': sum(d['total_count'] for d in hourly_data.values()),
            'avg_fleet_size': round(sum(d['total_count'] for d in hourly_data.values()) /
                                   len(hourly_data) if hourly_data else 0)
        }
    }

    # Write to JSON
    output_file = Path('/home/user/urban-transit-lab-predictor/gbfs_forecast_data.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✓ Forecast data written to {output_file}")
    print(f"  - Patterns for {len(patterns)} day types")
    print(f"  - {len(geographic)} geographic zones")
    print(f"  - {output['summary']['days_analyzed']} days analyzed")
    print(f"  - {output['summary']['total_observations']} vehicle observations")
    print(f"  - Avg fleet size: {output['summary']['avg_fleet_size']} vehicles")

if __name__ == '__main__':
    main()
