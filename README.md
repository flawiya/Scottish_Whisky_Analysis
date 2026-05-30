# 🥃 Satellite Monitoring of Soil Moisture in the Scottish Whisky Supply Chain

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![GeoPandas](https://img.shields.io/badge/GIS-GeoPandas-green)](https://geopandas.org/)
[![NASA API](https://img.shields.io/badge/Data-NASA%20POWER%20API-orange)](https://power.larc.nasa.gov/)

## 📌 Project Overview
The Scotch Whisky industry contributes £7.1 billion to the UK economy but relies heavily on barley yields vulnerable to moisture stress. This project utilizes **NASA SMAP satellite data** to model the spatial overlap between distillery locations and projected drought risk for the 2025 growing season.

### 🔗 [Live Interactive Climate Dashboard](YOUR_GITHUB_PAGES_LINK_HERE)

## 📊 Key Findings
- **The Speyside Paradox:** While the Western Highlands remain water-secure, the highest density of distilleries in the East aligns with regions projected to face "Moderate to Severe" moisture stress.
- **Risk Exposure:** Over 20% of active distilleries are situated in high-risk agricultural grain belts.

## 🛠️ Tech Stack & Data
- **NASA POWER API:** For satellite-derived precipitation proxies (PRECTOTCORR).
- **GeoPandas & Folium:** For administrative boundary processing and interactive dashboarding.
- **Simplification Algorithms:** Implemented geometry simplification to optimize high-resolution Scottish coastline data for web performance.

## 📁 Repository Structure
- `data/`: Shapefiles and distillery coordinates.
- `notebook/`: The full analysis and visualization workflow.
- `src/`: Modular Python scripts for API calls and data cleaning.
- `outputs/`: Static maps and risk classification reports.

## 🚀 How to Use
1. Clone the repo: `git clone https://github.com/flawiya/Scottish_Whisky_Analysis.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the analysis: `python -m src.analysis`

## 📑 References
- Scotch Whisky Association (2024) Economic Impact Report.
- NASA POWER API Documentation.
