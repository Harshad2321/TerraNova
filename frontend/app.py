import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="TerraNova – City Builder", page_icon="🏙️", layout="wide")
st.title("🏙️ TerraNova – AI Future City Builder")

API = "http://127.0.0.1:8000/city/generate_plan"

# ---------------- sidebar controls ----------------
with st.sidebar:
    st.header("City Inputs")
    city_name = st.text_input("City Name", "Neo Greenfield")
    population = st.number_input("Population", min_value=50_000, max_value=30_000_000, value=13_000_000, step=100_000)
    terrain = st.selectbox("Terrain", ["coastal", "plains", "mountain"], index=0)
    eco_priority = st.slider("Eco Priority", 1, 10, 9)
    size = st.slider("Grid Size (N x N)", 36, 96, 60, step=12)
    render_style = st.selectbox("Render Style", ["Pro Map", "Simple Grid"], index=0)
    run = st.button("Generate Plan")

# ---------------- color palette ----------------
palette = {
    "EMPTY": (1,1,1),
    "WATER": (0.55,0.78,1.0),
    "MOUNTAIN": (0.55,0.45,0.35),
    "FARM": (0.85,1.0,0.6),
    "PARK": (0.2,0.8,0.2),
    "HOME": (0.62,0.77,1.0),
    "OFFICE": (1.0,0.65,0.2),
    "HOSPITAL": (1.0,0.35,0.35),
    "SCHOOL": (1.0,1.0,0.45),
    "METRO": (0.45,0.0,0.55),
    "STATION": (0.0,0.6,0.6),
    "WALK": (0.6,1.0,0.6),
    "ROAD": (0.55,0.55,0.55),
}

def grid_to_rgb(grid, legend_map):
    grid = np.array(grid)
    id2name = legend_map
    h, w = grid.shape
    rgb = np.zeros((h, w, 3))
    for y in range(h):
        for x in range(w):
            name = id2name.get(int(grid[y, x]), "EMPTY")
            rgb[y, x] = palette.get(name, (0,0,0))
    return rgb

def draw_simple_grid(data):
    rgb = grid_to_rgb(data["plan_grid"], data["legend"])
    fig, ax = plt.subplots()
    ax.imshow(rgb, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    handles = [Patch(facecolor=palette[k], edgecolor="black", label=k) for k in palette.keys()]
    ax.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    return fig

def draw_pro_map(data, city_title):
    plan = np.array(data["plan_grid"])
    id2name = data["legend"]
    H, W = plan.shape

    # base: softened color blocks
    rgb = grid_to_rgb(plan, id2name)

    # upscale to make it smooth
    scale = 10
    big = np.kron(rgb, np.ones((scale, scale, 1)))

    fig = plt.figure(figsize=(12, 9))
    ax = plt.axes([0.05, 0.05, 0.72, 0.9])
    ax.imshow(big, interpolation="bilinear")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{city_title} — Coastal Eco-City Plan", fontsize=16, pad=12)

    # coastline glossy rim on the very left (water)
    # draw a translucent vertical gradient overlay to mimic shoreline glow
    water_cols = np.where(plan[0, :] == 1)[0]
    if len(water_cols) > 0:
        # left strip
        ax.add_patch(Rectangle((0, 0), 60, big.shape[0], linewidth=0, facecolor=(1,1,1,0.08)))

    # extract roads, metro, stations for crisp overlays
    def where_eq(val):
        ys, xs = np.where(plan == val)
        return list(zip((ys*scale).tolist(), (xs*scale).tolist()))

    roads = where_eq(12)
    metro = where_eq(9)
    stations = where_eq(10)

    # draw roads as thin lines (follow grid rows/cols)
    # horizontal roads
    for y in range(0, H, 1):
        if 12 in plan[y, :]:
            xs = np.where(plan[y, :] == 12)[0]
            if xs.size:
                ax.plot(xs*scale, np.full_like(xs, y*scale), linewidth=1.2, color=(0.3,0.3,0.3,0.9))
    # vertical roads
    for x in range(0, W, 1):
        if 12 in plan[:, x]:
            ys = np.where(plan[:, x] == 12)[0]
            if ys.size:
                ax.plot(np.full_like(ys, x*scale), ys*scale, linewidth=1.2, color=(0.3,0.3,0.3,0.9))

    # metro line thicker with stations
    # we detect each metro column and draw a spine
    for x in range(W):
        col = plan[:, x]
        if np.any((col == 9) | (col == 10)):
            ys = np.where((col == 9) | (col == 10))[0]
            ax.plot([x*scale]*len(ys), ys*scale, linewidth=3.0, color=palette["METRO"], alpha=0.95)
    for (yy, xx) in stations:
        ax.scatter(xx, yy, s=28, color=palette["STATION"], edgecolors="white", linewidths=0.7, zorder=5)

    # legend card
    legend_ax = plt.axes([0.80, 0.18, 0.18, 0.75])
    legend_ax.axis('off')
    legend_ax.text(0, 1.02, "Legend", fontsize=14, weight='bold')
    y0 = 0.95
    dy = 0.06
    for k in ["WATER","MOUNTAIN","PARK","FARM","HOME","OFFICE","HOSPITAL","SCHOOL","WALK","ROAD","METRO","STATION"]:
        c = palette[k]
        legend_ax.add_patch(Rectangle((0, y0-0.03), 0.05, 0.04, color=c, transform=legend_ax.transAxes))
        legend_ax.text(0.07, y0-0.01, k.title(), transform=legend_ax.transAxes, fontsize=11)
        y0 -= dy

    # metrics card
    m = data["metrics"]
    meta_ax = plt.axes([0.80, 0.03, 0.18, 0.12])
    meta_ax.axis('off')
    meta_ax.text(0, 1.05, "Key Metrics", fontsize=12, weight='bold')
    lines = [
        f"Green Cover: {m['green_cover_pct']}%",
        f"Walkability: {m['walkability_index']}%",
        f"Transit Coverage: {m['transit_coverage_pct']}%",
        f"Renewable Potential: {m['renewable_potential']}/100",
        f"Est. CO₂ / cap: {m['est_co2_per_capita']} kg/day"
    ]
    for i, line in enumerate(lines):
        meta_ax.text(0, 0.9 - i*0.2, line, fontsize=10)

    return fig

# ---------------- UI logic ----------------
col_left, col_right = st.columns([3, 2])

if run:
    payload = {
        "city_name": city_name,
        "population": int(population),
        "terrain": terrain,
        "eco_priority": int(eco_priority),
        "size": int(size),
    }
    try:
        r = requests.post(API, json=payload, timeout=45)
        r.raise_for_status()
        data = r.json()

        with col_left:
            st.subheader("🗺️ City Map")
            if render_style == "Pro Map":
                fig = draw_pro_map(data, city_name)
            else:
                fig = draw_simple_grid(data)

            st.pyplot(fig, use_container_width=True)

            # export PNG
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=220, bbox_inches="tight")
            buf.seek(0)
            st.download_button(
                label="⬇️ Download Map PNG",
                data=buf,
                file_name=f"{city_name.replace(' ','_')}_map.png",
                mime="image/png"
            )

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
    st.info("Choose inputs in the sidebar and click **Generate Plan**.")
