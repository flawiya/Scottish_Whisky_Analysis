# whisky-supply-chain-climate

Scaffolded project reproducing the Scottish whisky supply-chain climate analysis as runnable Python scripts (no notebook included).

Structure
- data/                   # (Optional) Add CSVs and shapefiles used by the analysis
- notebook/               # Notebook intentionally omitted; see README note
- outputs/
  - figures/              # Generated PNG figures will be saved here
- src/
  - analysis.py           # Main script reproducing notebook workflow
  - nasa_api.py           # NASA POWER helper (fetch_rainfall_data)
- requirements.txt
- .gitignore

Quick start
1. Create and activate a venv then install dependencies:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Add your input files under `data/` and run:

```powershell
python -m src.analysis --distilleries data\distilleries_cleaned.csv --shapefile "data\Local_Authority_Boundaries_-_Scotland\pub_las.shp" --output outputs
```

Notes
- The notebook is intentionally not included; `src/analysis.py` reproduces the same steps.
- Consider caching NASA POWER responses for development.
