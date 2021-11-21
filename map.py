import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point
from folium import plugins
from auth import spreadsheet_service

def create():
    range_name = 'Sheet1!A1:G1000'
    spreadsheet_id = '1zB9WAxgGIbhyWlLpj6g1Fhnke1Rrf5EQmduipE1pq34'
    result = spreadsheet_service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    df = pd.DataFrame(rows)
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    pdt = df['country'].value_counts()

    map = folium.Map(location = [9.0820, 8.6753], tiles = "OpenStreetMap", 
                 zoom_start = 6, min_zoom = 2, max_zoom = 10)

    geometry = gpd.points_from_xy(df.long, df.lat)
    geo_df = gpd.GeoDataFrame(df, geometry=geometry)
    geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry ]

    i = 1
    for coordinates in geo_df_list:
        if geo_df.country[i] == "United States":
            type_color = "green"
        elif geo_df.country[i] == "Nigeria":
            type_color = "blue"
        else:
            type_color = "purple"

        #now place the markers with the popup labels and data
        map.add_child(folium.Marker(location = coordinates,
                                popup =
                                "Continent: " + str(geo_df.continent[i]) + '<br>' +
                                "Country: " + str(geo_df.country[i]) + '<br>' +
                                "Total: " + str(pdt[geo_df.country[i]]) + '<br>' +
                                "State: " + str(geo_df.state[i]),
                                icon = folium.Icon(color = "%s" % type_color)))
        i = i + 1
    map.save('./static/map/locations.html')

    map2 = folium.Map(location = [15, 30], tiles = "Cartodb dark_matter", 
                 zoom_start = 2)

    heat_data = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry ]

    heat_data
    plugins.HeatMap(heat_data).add_to(map2)

    map2.save('./static/map/locationsHeatMap.html')

