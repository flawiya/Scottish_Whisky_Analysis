# 🥃 Satellite Monitoring of Soil Moisture in the Scottish Whisky Supply Chain

A reproducible Python project for analyzing Scottish whisky supply chain climate risk.

This repository converts a notebook-style workflow into a script-based analysis that:
- loads distillery location and regional boundary data
- fetches rainfall projections from NASA POWER
- calculates regional drought risk
- creates GIS visualizations and a Folium dashboard

## Repository structure

- `data/` - input datasets (CSV and shapefile data)
- `notebook/` - notebook is intentionally omitted from this repo
- `outputs/` - generated charts and dashboard files
  - `figures/` - saved PNG map figures
- `src/`
  - `analysis.py` - main analysis script
  - `nasa_api.py` - helper module for NASA POWER rainfall requests
- `requirements.txt` - Python dependencies
- `.gitignore` - ignored files and folders

## Setup

1. Create and activate a virtual environment:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Usage

Place your inputs in the `data/` folder, then run the analysis script.

```powershell
python src/analysis.py --distilleries data\distilleries_cleaned.csv --shapefile "data\Local_Authority_Boundaries_-_Scotland\pub_las.shp" --output outputs
```

If you prefer the default paths set inside `src/analysis.py`, simply run:

```powershell
python src/analysis.py
```

## Output

The script produces:
- `outputs/dashboard.html` — interactive Folium dashboard
- `outputs/figures/figure_rainfall.png`
- `outputs/figures/figure_drought.png`
- `outputs/figures/figure_exposure.png`

Open `outputs/dashboard.html` in your browser to inspect the map and distillery markers.

## Notes

- The notebook version is omitted by design; this repo uses `src/analysis.py` instead.
- The script expects the shapefile to contain regional attributes such as `CouncilArea`.
- If the shapefile uses a different region name field, the dashboard code may need adjustment.
- Caching NASA POWER responses is recommended to avoid repeated API requests during development.

## License

Add a license file if you want this repository to be open source.

## 📑 References
- Scotch Whisky Association (2024) Economic Impact Report.
- NASA POWER API Documentation.
