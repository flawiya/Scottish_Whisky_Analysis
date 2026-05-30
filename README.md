# 🥃 Satellite-Driven Drought Risk Assessment: Scotch Whisky Supply Chain

An integrated geospatial analysis tool evaluating climate vulnerability across 140+ Scottish distilleries using NASA SMAP satellite data.

## 🔗 [View Live Interactive Dashboard](https://flawiya.github.io/Scottish_Whisky_Analysis/)

---

## 📊 Executive Summary
This project bridges environmental science and industrial logistics. By integrating **NASA POWER API** climate proxies with spatial industrial data, we identify a critical "Speyside Paradox": the highest concentration of distilling infrastructure is located in the eastern grain belts most susceptible to projected 2025 moisture deficits.

### Key Visualizations
| Rainfall Gradient (Fig 1) | Drought Risk (Fig 2) | Industry Exposure (Fig 3) |
|---|---|---|
| ![Rainfall](./outputs/rain_map.png) | ![Risk](./outputs/risk_map.png) | ![Exposure](./outputs/exposure_map.png) |

## 🛠️ Technical Implementation
- **Data Sourcing:** Automated extraction of `PRECTOTCORR` (corrected precipitation) via NASA's API.
- **Geoprocessing:** Dual-projection workflow (EPSG:27700 for accuracy, EPSG:4326 for web) with **Douglas-Peucker geometry simplification** to optimize dashboard performance.
- **Interactivity:** A custom Folium assemblage featuring conditional marker logic (Red/Orange/Blue) based on regional drought thresholds.

## 📁 Repository Structure
- `index.html`: The optimized interactive dashboard (GitHub Pages).
- `notebooks/`: Comprehensive `.ipynb` analysis and code.
- `data/`: Cleaned CSVs and local authority shapefiles.
- `outputs/`: Static map exports for reporting.

## 🚀 Setup
1. Clone the repo: `git clone https://github.com/flawiya/Scottish_Whisky_Analysis.git`
2. Install requirements: `pip install geopandas folium contextily requests`
