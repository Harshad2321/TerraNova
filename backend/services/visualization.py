import folium
import os

def generate_visual_map():
    """Generate an interactive city map with folium"""
    map_path = "static/visual_map.html"

    # Create a base map (centered on arbitrary coords)
    city_map = folium.Map(location=[28.6139, 77.2090], zoom_start=12)

    # Add key places (demo)
    folium.Marker([28.61, 77.20], popup="City Center").add_to(city_map)
    folium.Marker([28.62, 77.22], popup="Park").add_to(city_map)
    folium.Marker([28.63, 77.18], popup="Railway Station").add_to(city_map)

    # Add a "river" as polyline
    folium.PolyLine(
        locations=[[28.60, 77.18], [28.65, 77.25]],
        color="blue",
        weight=4,
        opacity=0.8,
    ).add_to(city_map)

    # Save HTML map
    city_map.save(map_path)
    return map_path
