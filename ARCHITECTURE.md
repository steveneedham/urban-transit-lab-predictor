# Urban Transit Lab — System Architecture

## Current Implementation: Research Forecasting Platform

---

## Data Sources

### GBFS Fleet Data (PRIMARY)
**Status:** ✓ Active

- Veo & Spin scooters
- Live + historical snapshots (1+ years)
- Real-time telemetry

### Event & Weather Data
**Status:** ✓ Active

- Seasonal patterns
- Event correlation data
- Festival demand signals

### 311 Complaints (PLANNED)
**Status:** Planned for v2+

- City feedback loops
- Complaint mapping
- Regulatory impact analysis

---

## Data Processing & Analysis

### GBFS Pipeline
**Tool:** `analyze_gbfs_data.py`

- Hourly availability patterns
- Geographic demand zones
- Vehicle type distribution
- Day-of-week effects

### Correlation Analysis
**Active Components:**

- Weather pattern analysis
- Event demand signals
- Seasonal forecasting

### 311 Intelligence (Planned)
**Requirements:**

- City API access
- Complaint pattern mapping
- Regulation impact tracking

---

## Research & Analysis Outputs

### 1. Demand Forecast Dashboard
**File:** `forecast.html`

- 24-hour demand patterns by day-of-week
- Geographic hotspot maps
- Key metrics and confidence scores

### 2. Forecast Accuracy Report
**File:** `comparison.html`

- Performance metrics
- Model validation
- Prediction vs. actual comparisons

### 3. Weather Analysis Dashboard
**File:** `weather.html`

- Correlation patterns
- Seasonal impact analysis
- Weather-demand relationships

### 4. Event Readiness Case Study
**File:** `case-study.html`

- Festival demand analysis
- Event playbook patterns
- Two-event comparison methodology

### 5. Research Library
**File:** `research-library.html`

- Methodology documentation
- Data source guides
- Integrated events viewer

---

## Planned v2+ Features: Operational Intelligence

### City Insight Dashboard (Planned)
**Requirements:** 311 API integration

- Regulation effectiveness analysis
- Enforcement priority data
- Complaint pattern tracking

### Operator Dashboard (Planned)
**Requirements:** Operator fleet APIs

- Weekly rebalancing targets
- Performance gap analysis
- Demand-supply matching

### Community Feedback Loop (Planned)
**Requirements:** Feedback collection system

- 311 complaint status tracking
- Operator response tracking
- Community acknowledgment

---

## Component Status Matrix

| Component | Status | Data Source | Output |
|-----------|--------|-------------|--------|
| GBFS Analysis | ✓ Active | Scooter telemetry | Forecast dashboard |
| Event Correlation | ✓ Active | Event calendar | Weather dashboard |
| Accuracy Reporting | ✓ Active | Historical data | Accuracy report |
| Case Studies | ✓ Active | Research analysis | Event playbook |
| Research Docs | ✓ Active | Methodology | Research library |
| City Integration | Planned | 311 complaints | City insights |
| Operator APIs | Planned | Fleet management | Rebalancing targets |
| Community Loop | Planned | Resident feedback | Feedback status |

---

## Research Question

**Using public GBFS data and what we know about demand drivers (events, weather, time patterns), what can we accurately forecast about micromobility demand?**

### Current Answer

We can accurately forecast:
- Hourly demand patterns by day-of-week
- Geographic demand distribution across Columbus zones
- Weather impact on scooter usage
- Seasonal and event-driven demand spikes
- Fleet availability ratios

### Next Phase

Integration with city and operator data systems to move from research forecasting to operational intelligence that directly informs regulation, rebalancing, and community engagement.

---

## How to Use

1. **Interactive Diagrams**: Open `system-architecture.html` in a browser for the visual system diagram
2. **Text Documentation**: Read this file (`ARCHITECTURE.md`) for detailed component descriptions
3. **Dashboard Access**: Visit each `.html` file to view live forecasts and analysis:
   - `forecast.html` — Current demand forecasts
   - `comparison.html` — Model accuracy metrics
   - `weather.html` — Weather correlation analysis
   - `case-study.html` — Event-readiness playbook
   - `research-library.html` — Complete methodology

---

**Last Updated:** August 9, 2026
