import os
import argparse
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import folium
from shapely.geometry import Point
from nasa_api import fetch_rainfall_data


def classify_drought(value):
    if value is None:
        return "No Data"
    v = float(value)
    if v < 200:
        return "Severe Drought"
    if v < 300:
        return "Moderate Stress"
    return "Normal Moisture"


def add_map_elements(ax, map_type="standard"):
    title_text = {
        "rain": "Projected Rainfall Gradient",
        "drought": "Drought Risk Assessment",
        "exposure": "Industry Exposure & Terrain",
    }
    ax.text(0.05, 0.97, title_text.get(map_type, "Map"), transform=ax.transAxes,
            fontsize=12, fontweight="bold", verticalalignment="top",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="black", pad=5.0))


def make_outputs(distilleries_csv, shapefile, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    figs_dir = os.path.join(output_dir, "figures")
    os.makedirs(figs_dir, exist_ok=True)

    if not os.path.exists(distilleries_csv):
        print(f"Distilleries CSV not found: {distilleries_csv}")
        return
    if not os.path.exists(shapefile):
        print(f"Shapefile not found: {shapefile}")
        return

    dist_df = pd.read_csv(distilleries_csv)
    if "longitude" not in dist_df.columns or "latitude" not in dist_df.columns:
        print("Distilleries CSV must contain 'longitude' and 'latitude' columns.")
        return

    dist_gdf = gpd.GeoDataFrame(
        dist_df, geometry=gpd.points_from_xy(dist_df.longitude, dist_df.latitude), crs="EPSG:4326"
    )

    regions = gpd.read_file(shapefile).to_crs(epsg=3857)

    # Calculate centroids for API (use projected centroids then convert to WGS84)
    projected = regions.to_crs(epsg=27700)
    centroids = projected.geometry.centroid.to_crs(epsg=4326)
    regions["centroid_lat"] = centroids.y
    regions["centroid_lon"] = centroids.x

    print("Requesting NASA POWER data for each region (this may take a while)...")
    regions["Rainfall_2025"] = regions.apply(
        lambda r: fetch_rainfall_data(r["centroid_lat"], r["centroid_lon"]), axis=1
    )
    regions["Drought_Status"] = regions["Rainfall_2025"].apply(classify_drought)

    # Figure 1: Rainfall choropleth
    fig, ax = plt.subplots(figsize=(8, 10))
    regions.plot(column="Rainfall_2025", ax=ax, cmap="YlGnBu", legend=True,
                 edgecolor="black", linewidth=0.2, alpha=0.8,
                 legend_kwds={"label": "Millimeters (mm)", "shrink": 0.5})
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, crs=regions.crs)
    add_map_elements(ax, "rain")
    ax.set_axis_off()
    f1 = os.path.join(figs_dir, "figure_rainfall.png")
    fig.savefig(f1, dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Figure 2: Drought classification
    regions["Drought_Status"] = pd.Categorical(
        regions["Drought_Status"], categories=["Severe Drought", "Moderate Stress", "Normal Moisture", "No Data"], ordered=True
    )
    fig, ax = plt.subplots(figsize=(8, 10))
    regions.plot(column="Drought_Status", ax=ax, cmap="RdYlGn", legend=True, edgecolor="black", linewidth=0.3)
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, crs=regions.crs)
    add_map_elements(ax, "drought")
    ax.set_axis_off()
    f2 = os.path.join(figs_dir, "figure_drought.png")
    fig.savefig(f2, dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Figure 3: Industry exposure
    fig, ax = plt.subplots(figsize=(8, 10))
    regions.boundary.plot(ax=ax, linewidth=0.8, color="#444444", alpha=0.6)
    dist_gdf.to_crs(regions.crs).plot(ax=ax, color="black", marker="o", markersize=20, label="Distillery")
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, crs=regions.crs)
    ax.legend(loc="lower left", fontsize=8)
    add_map_elements(ax, "exposure")
    ax.set_axis_off()
    f3 = os.path.join(figs_dir, "figure_exposure.png")
    fig.savefig(f3, dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Folium dashboard
    try:
        folium_map = folium.Map(
            location=[56.8, -4.2],
            zoom_start=7,
            tiles='CartoDB Positron',
            control_scale=True
        )

        scotland_folium = regions.to_crs(epsg=4326)
        distilleries_folium = dist_gdf.to_crs(epsg=4326)

        # Attach regional risk values to distilleries for the popup logic
        if 'Drought_Status' not in distilleries_folium.columns or 'Rainfall_2025' not in distilleries_folium.columns:
            distilleries_folium = gpd.sjoin(
                distilleries_folium,
                scotland_folium[['geometry', 'CouncilArea', 'Drought_Status', 'Rainfall_2025']],
                how='left',
                predicate='within'
            )

        choropleth = folium.Choropleth(
            geo_data=scotland_folium,
            name="Regional Rainfall Gradient",
            data=scotland_folium,
            columns=["CouncilArea", "Rainfall_2025"],
            key_on="feature.properties.CouncilArea",
            fill_color="YlGnBu",
            fill_opacity=0.6,
            line_opacity=0.4,
            legend_name="Projected Total Rainfall (mm) - Summer 2025",
            highlight=True
        ).add_to(folium_map)

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=['CouncilArea', 'Rainfall_2025', 'Drought_Status'],
                aliases=['Region:', 'Rainfall (mm):', 'Risk Level:'],
                localize=True,
                sticky=False,
                labels=True,
                style="""
                    background-color: #F0EFEF;
                    border: 1px solid black;
                    border-radius: 3px;
                    box-shadow: 3px;
                """,
                max_width=800,
            )
        )

        distillery_group = folium.FeatureGroup(name="Whisky Distilleries")

        for _, row in distilleries_folium.iterrows():
            drought_status = row.get('Drought_Status', 'Normal Moisture')
            if drought_status == "Severe Drought":
                marker_color = 'red'
                icon_type = 'exclamation-triangle'
            elif drought_status == "Moderate Stress":
                marker_color = 'orange'
                icon_type = 'info-circle'
            else:
                marker_color = 'blue'
                icon_type = 'tint'

            rainfall_value = row.get('Rainfall_2025', None)
            if rainfall_value is None or (isinstance(rainfall_value, float) and pd.isna(rainfall_value)):
                rainfall_text = 'NA'
            else:
                rainfall_text = f"{rainfall_value:.1f} mm"

            folium.Marker(
                location=[row.geometry.y, row.geometry.x],
                popup=folium.Popup(f"""
                    <div style='font-family: Arial; width: 200px;'>
                        <h4 style='color:navy;'>{row.get('name', 'Distillery')}</h4>
                        <hr>
                        <b>Climate Risk:</b> {drought_status}<br>
                        <b>Projected Rain:</b> {rainfall_text}
                    </div>
                """, max_width=250),
                tooltip=row.get('name', 'Distillery'),
                icon=folium.Icon(color=marker_color, icon=icon_type, prefix='fa')
            ).add_to(distillery_group)

        distillery_group.add_to(folium_map)
        folium.LayerControl(collapsed=False).add_to(folium_map)

        out_html = os.path.join(output_dir, "dashboard.html")
        folium_map.save(out_html)
    except Exception as e:
        print("Failed to create folium map:", e)

    print("Outputs saved:")
    print(" -", f1)
    print(" -", f2)
    print(" -", f3)
    print(" - dashboard:", os.path.join(output_dir, "dashboard.html"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--distilleries", default="C:/Users/flavi/Downloads/geovis/Scotch Whisky/distilleries_cleaned.csv")
    parser.add_argument("--shapefile", default="C:/Users/flavi/Downloads/geovis/Scotch Whisky/Local_Authority_Boundaries_-_Scotland/pub_las.shp")
    parser.add_argument("--output", default="outputs")
    args = parser.parse_args()
    make_outputs(args.distilleries, args.shapefile, args.output)


if __name__ == "__main__":
    main()
