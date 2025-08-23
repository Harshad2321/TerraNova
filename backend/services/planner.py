from backend.schemas.planner import CityRequest, CityPlan, Zone, Road, Amenity, Infrastructure
import folium
import os

def generate_city_plan(req: CityRequest) -> CityPlan:
    # Example industrial-level logic
    zones = {
        "residential": [
            Zone(id="res1", name="Residential Zone A", coordinates=[19.0760, 72.8777], capacity=5000),
            Zone(id="res2", name="Residential Zone B", coordinates=[19.1660, 72.9477], capacity=7000),
        ],
        "commercial": [
            Zone(id="com1", name="Commercial Zone A", coordinates=[19.0960, 72.9077], capacity=3000),
        ]
    }

    roads = [
        Road(id="r1", type="highway", from_="res1", to="com1", length_km=5.2),
        Road(id="r2", type="local", from_="res2", to="res1", length_km=3.1)
    ]

    amenities = [
        Amenity(id="a1", type="hospital", name="City Hospital", coordinates=[19.085, 72.88]),
        Amenity(id="a2", type="school", name="Central School", coordinates=[19.095, 72.90])
    ]

    infrastructure = Infrastructure(
        river=req.river,
        railway_station=req.railway_station,
        airports=1,
        metro_lines=2
    )

    return CityPlan(
        city_name=req.city_name,
        population=req.population,
        zones=zones,
        roads=roads,
        public_amenities=amenities,
        infrastructure=infrastructure
    )


def generate_city_map(plan: CityPlan, output_dir="static"):
    os.makedirs(output_dir, exist_ok=True)
    m = folium.Map(location=[19.0760, 72.8777], zoom_start=12)

    for zone_type, zones in plan.zones.items():
        for z in zones:
            folium.Marker(
                location=z.coordinates,
                popup=f"{z.name} ({zone_type})"
            ).add_to(m)

    for a in plan.public_amenities:
        folium.Marker(
            location=a.coordinates,
            popup=f"{a.type.capitalize()}: {a.name}",
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

    map_path = os.path.join(output_dir, f"{plan.city_name}_map.html")
    m.save(map_path)
    return map_path
