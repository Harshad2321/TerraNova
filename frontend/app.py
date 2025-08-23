import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="TerraNova – City Builder", page_icon="🏙️", layout="wide")
st.title("🏙️ TerraNova – AI Future City Builder")

with st.sidebar:
    st.header("City Inputs")
    city_name = st.text_input("City Name", "Neo Greenfield")
    population = st.number_input("Population", min_value=10000, max_value=2000000, value=120000, step=10000)
    terrain = st.selectbox("Terrain", ["plains", "coastal", "mountain"])
    eco_priority = st.slider("Eco Priority", 1, 10, 8)
    size = st.slider("Grid Size (N x N)", 24, 96, 48, step=12)
    run = st.button("Generate Plan")

API = "http://127.0.0.1:8000/city/generate_plan"

def draw_grid(grid, legend_map):
    grid = np.array(grid)
    # color palette
    palette = {
        "EMPTY": (1,1,1),
        "WATER": (0.6,0.8,1.0),
        "MOUNTAIN": (0.55,0.45,0.35),
        "FARM": (0.85,1.0,0.6),
        "PARK": (0.2,0.8,0.2),
        "HOME": (0.6,0.8,1.0),
        "OFFICE": (1.0,0.6,0.0),
        "HOSPITAL": (1.0,0.3,0.3),
        "SCHOOL": (1.0,1.0,0.4),
        "METRO": (0.55,0.0,0.55),
        "STATION": (0.0,0.6,0.6),
        "WALK": (0.6,1.0,0.6),
        "ROAD": (0.5,0.5,0.5),
    }
    # reverse legend_map: id->name already provided by backend
    id2name = legend_map
    h, w = grid.shape
    rgb = np.zeros((h, w, 3))
    for y in range(h):
        for x in range(w):
            name = id2name.get(int(grid[y, x]), "EMPTY")
            rgb[y, x] = palette.get(name, (0,0,0))

    fig, ax = plt.subplots()
    ax.imshow(rgb)
    ax.set_xticks([])
    ax.set_yticks([])
    # legend
    handles = [Patch(facecolor=palette[k], edgecolor="black", label=k) for k in palette.keys()]
    ax.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    st.pyplot(fig, use_container_width=True)

col_left, col_right = st.columns([3,2])

if run:
    payload = {
        "city_name": city_name,
        "population": population,
        "terrain": terrain,
        "eco_priority": eco_priority,
        "size": size
    }
    try:
        r = requests.post(API, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()

        with col_left:
            st.subheader("🗺️ City Plan")
            draw_grid(data["plan_grid"], data["legend"])

        with col_right:
            st.subheader("📊 Metrics")
            m = data["metrics"]
            st.metric("Green Cover", f"{m['green_cover_pct']}%")
            st.metric("Walkability Index", f"{m['walkability_index']}%")
            st.metric("Transit Coverage", f"{m['transit_coverage_pct']}%")
            st.metric("Renewable Potential", f"{m['renewable_potential']} / 100")
            st.metric("Est. CO₂ per Capita", f"{m['est_co2_per_capita']} kg/day")
            st.divider()
            st.subheader("📝 Notes")
            for note in data.get("notes", []):
                st.write("• " + note)

        st.success("Plan generated successfully.")
    except Exception as e:
        st.error(f"Failed to fetch plan: {e}")
else:
    st.info("Set inputs in the sidebar and click **Generate Plan**.")
