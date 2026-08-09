# Urban Transit Lab — Micromobility Demand Forecasting

A research platform that combines GBFS fleet telemetry with event and weather data to forecast micromobility demand patterns in Columbus, OH.

## What This System Does

**Current focus:** Research-grade demand forecasting and analysis built on public GBFS data (Veo + Spin scooters).

- **forecast.html** — Interactive 24-hour demand forecast dashboard with geographic hotspots
- **comparison.html** — Forecast accuracy reporting and performance metrics  
- **weather.html** — Weather pattern correlation analysis and seasonal demand signals
- **case-study.html** — Event-readiness analytics (e.g., festival demand planning)
- **research-library.html** — Methodology, data sources, and integrated events viewer
- **analyze_gbfs_data.py** — Data processing pipeline (historical snapshot analysis)

## System Architecture

See [system-architecture.html](./system-architecture.html) for a complete data flow diagram showing:
- **Active components** (solid) — GBFS analysis, research dashboards
- **Planned features** (dashed) — City 311 integration, operator APIs, community feedback loops

## Data Sources

- **GBFS Telemetry** — Live + historical snapshots from Veo and Spin (1+ year)
- **Event Data** — Festival and event calendars
- **Weather Data** — Seasonal patterns and weather correlation

## Planned (v2+)

Future phases will integrate:
- City 311 complaint data and mapping
- Operator fleet management APIs
- Community feedback mechanisms
- Real-time operational dashboards for city and operators

## Research Question

Using public GBFS data and what we know about demand drivers (events, weather, time patterns), what can we accurately forecast about micromobility demand?
