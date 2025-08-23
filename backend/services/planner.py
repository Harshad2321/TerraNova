from __future__ import annotations
import random
from typing import List, Tuple, Optional, Dict
import numpy as np
from . import tiles as T

# --- small internal helpers ---

def seed_everything(seed: Optional[int] = 42):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

def in_bounds(y: int, x: int, size: int) -> bool:
    return 0 <= y < size and 0 <= x < size

def neighbors4(y: int, x: int):
    return [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]

def is_adjacent_to(grid: np.ndarray, y: int, x: int, types: List[int]) -> bool:
    for ny, nx in neighbors4(y, x):
        if 0 <= ny < grid.shape[0] and 0 <= nx < grid.shape[1] and grid[ny, nx] in types:
            return True
    return False

def find_tiles(grid: np.ndarray, t: int) -> List[Tuple[int, int]]:
    ys, xs = np.where(grid == t)
    return list(zip(ys.tolist(), xs.tolist()))

# --- terrain ---

def generate_terrain(size: int, terrain_kind: str) -> np.ndarray:
    g = np.zeros((size, size), dtype=int)  # EMPTY base

    if terrain_kind == "coastal":
        width = max(2, size // 10)
        g[:, :width] = T.TILE["WATER"]

    if terrain_kind in ("coastal", "plains"):
        # river
        x = size // 2 + random.randint(-size//8, size//8)
        for y in range(size):
            x0 = max(1, min(size-2, x))
            g[y, x0-1:x0+2] = T.TILE["WATER"]
            x += random.choice([-1, 0, 1])

    if terrain_kind in ("mountain", "coastal"):
        base = size // 3
        for i in range(size):
            j = (i + base) % size
            g[i, j] = T.TILE["MOUNTAIN"]
            if in_bounds(i, j+1, size) and random.random() < 0.4:
                g[i, j+1] = T.TILE["MOUNTAIN"]

    return g

# --- zoning ---

def allocate_zones(terrain: np.ndarray, population: int, eco_priority: int) -> np.ndarray:
    size = terrain.shape[0]
    plan = terrain.copy()

    # scale quotas from population
    pop_factor = max(1, min(5, population // 40000))  # 1..5

    targets = {
        "HOME": 220 * pop_factor,
        "OFFICE": 120 * pop_factor,
        "FARM": 160 * pop_factor,
        "PARK": 160 + 10 * eco_priority,
        "HOSPITAL": max(2, population // 20000),
        "SCHOOL": max(3, population // 10000),
    }

    # parks near water as buffers
    parks_left = targets["PARK"]
    for y in range(size):
        for x in range(size):
            if plan[y, x] == T.TILE["EMPTY"] and is_adjacent_to(plan, y, x, [T.TILE["WATER"]]):
                plan[y, x] = T.TILE["PARK"]
                parks_left -= 1
                if parks_left <= 0:
                    break
        if parks_left <= 0:
            break

    # farms near water / away from mountains
    farms_left = targets["FARM"]
    for y in range(size):
        for x in range(size):
            if plan[y, x] != T.TILE["EMPTY"]:
                continue
            if is_adjacent_to(plan, y, x, [T.TILE["WATER"], T.TILE["PARK"]]) and not is_adjacent_to(plan, y, x, [T.TILE["MOUNTAIN"]]):
                plan[y, x] = T.TILE["FARM"]
                farms_left -= 1
                if farms_left <= 0:
                    break
        if farms_left <= 0:
            break

    # homes on flat land
    homes_left = targets["HOME"]
    for y in range(size):
        for x in range(size):
            if plan[y, x] == T.TILE["EMPTY"] and not is_adjacent_to(plan, y, x, [T.TILE["MOUNTAIN"]]) and homes_left > 0:
                plan[y, x] = T.TILE["HOME"]
                homes_left -= 1

    # mixed-use bias for eco: offices near homes
    offices_left = targets["OFFICE"]
    bias = 0.55 if eco_priority >= 7 else 0.35
    for y in range(size):
        for x in range(size):
            if plan[y, x] == T.TILE["EMPTY"] and offices_left > 0 and random.random() < bias and is_adjacent_to(plan, y, x, [T.TILE["HOME"]]):
                plan[y, x] = T.TILE["OFFICE"]
                offices_left -= 1

    # public services
    def place_service(tile_id: int, quota: int, near_types: List[int]):
        left = quota
        for y in range(size):
            for x in range(size):
                if plan[y, x] == T.TILE["EMPTY"] and is_adjacent_to(plan, y, x, near_types):
                    plan[y, x] = tile_id
                    left -= 1
                    if left <= 0: return
        for y in range(size):
            for x in range(size):
                if plan[y, x] == T.TILE["EMPTY"] and left > 0:
                    plan[y, x] = tile_id
                    left -= 1
                    if left <= 0: return

    place_service(T.TILE["HOSPITAL"], targets["HOSPITAL"], [T.TILE["HOME"], T.TILE["OFFICE"]])
    place_service(T.TILE["SCHOOL"], targets["SCHOOL"], [T.TILE["HOME"]])

    # green walkways linking homes and parks
    for y in range(1, size-1):
        for x in range(1, size-1):
            if plan[y, x] == T.TILE["EMPTY"] and is_adjacent_to(plan, y, x, [T.TILE["PARK"]]) and is_adjacent_to(plan, y, x, [T.TILE["HOME"]]):
                if random.random() < 0.4:
                    plan[y, x] = T.TILE["WALK"]

    # roads (grid), avoid parks/farms
    step = max(6 - pop_factor, 3)
    for y in range(0, size, step):
        for x in range(size):
            if plan[y, x] in [T.TILE["EMPTY"], T.TILE["WALK"]]:
                plan[y, x] = T.TILE["ROAD"]
    for x in range(0, size, step):
        for y in range(size):
            if plan[y, x] in [T.TILE["EMPTY"], T.TILE["WALK"]]:
                plan[y, x] = T.TILE["ROAD"]

    # metro along densest band of homes/offices
    density = np.zeros_like(plan)
    density[plan == T.TILE["HOME"]] = 2
    density[plan == T.TILE["OFFICE"]] = 3
    band = density.sum(axis=0)
    x_peak = int(np.argmax(band))
    for y in range(size):
        if plan[y, x_peak] in [T.TILE["EMPTY"], T.TILE["ROAD"], T.TILE["WALK"]]:
            plan[y, x_peak] = T.TILE["METRO"]
    for y in range(0, size, 8):
        if is_adjacent_to(plan, y, x_peak, [T.TILE["HOME"], T.TILE["OFFICE"]]):
            plan[y, x_peak] = T.TILE["STATION"]

    return plan

# --- metrics ---

def compute_metrics(plan: np.ndarray) -> Dict[str, float]:
    size = plan.shape[0]
    total = size * size
    green = np.count_nonzero(plan == T.TILE["PARK"]) + np.count_nonzero(plan == T.TILE["WALK"]) + np.count_nonzero(plan == T.TILE["FARM"])
    green_cover_pct = round(100 * green / total, 2)

    home_positions = find_tiles(plan, T.TILE["HOME"])
    walkable_homes = 0
    for y, x in home_positions:
        if is_adjacent_to(plan, y, x, [T.TILE["PARK"], T.TILE["WALK"], T.TILE["STATION"]]):
            walkable_homes += 1
    walkability_index = round(100 * (walkable_homes / max(1, len(home_positions))), 2)

    transit_homes = 0
    for y, x in home_positions:
        if is_adjacent_to(plan, y, x, [T.TILE["METRO"], T.TILE["STATION"]]):
            transit_homes += 1
    transit_coverage_pct = round(100 * (transit_homes / max(1, len(home_positions))), 2)

    renew_proxy = (
        0.3 * np.count_nonzero(plan == T.TILE["FARM"]) +
        0.2 * np.count_nonzero(plan == T.TILE["PARK"]) +
        0.1 * np.count_nonzero(plan == T.TILE["WATER"]) +
        0.1 * np.count_nonzero(plan == T.TILE["MOUNTAIN"]) +
        0.3 * np.count_nonzero(plan == T.TILE["OFFICE"])
    )
    renewable_potential = round(100 * renew_proxy / total, 2)

    co2_index = 100 - (0.4 * green_cover_pct + 0.3 * walkability_index + 0.3 * transit_coverage_pct)
    est_co2_per_capita = round(max(5.0, co2_index / 3), 2)  # kg/day (scaled)

    return {
        "green_cover_pct": green_cover_pct,
        "walkability_index": walkability_index,
        "renewable_potential": renewable_potential,
        "est_co2_per_capita": est_co2_per_capita,
        "transit_coverage_pct": transit_coverage_pct,
    }

# --- public API ---

def build_plan(size: int, terrain_kind: str, population: int, eco_priority: int, seed: int = 42):
    seed_everything(seed)
    terrain = generate_terrain(size, terrain_kind)
    plan = allocate_zones(terrain, population, eco_priority)
    metrics = compute_metrics(plan)

    notes = [
        "Parks buffer coasts/rivers to reduce flood risk and add green cover.",
        "Farms are near water and away from mountains for irrigation and soil.",
        "Homes on flat land; offices biased close to homes for mixed-use.",
        "Hospitals/schools distributed near residential clusters.",
        "Metro follows densest home/office band; stations ~every 8 tiles.",
    ]

    return {
        "legend": T.LEGEND,
        "size": size,
        "terrain_grid": terrain.tolist(),
        "plan_grid": plan.tolist(),
        "metrics": metrics,
        "notes": notes,
    }

# --- tile legend in a separate module-like dict (inline here for import simplicity) ---
# tiles module content
class TILES_:  # only to namespace constants
    pass

TILE = {
    "EMPTY": 0,
    "WATER": 1,
    "MOUNTAIN": 2,
    "FARM": 3,
    "PARK": 4,
    "HOME": 5,
    "OFFICE": 6,
    "HOSPITAL": 7,
    "SCHOOL": 8,
    "METRO": 9,
    "STATION": 10,
    "WALK": 11,
    "ROAD": 12,
}

LEGEND = {v: k for k, v in TILE.items()}

# re-export for imports above as `.tiles`
class tiles:
    TILE = TILE
    LEGEND = LEGEND

# also export under simple name T for convenience
class T:
    TILE = TILE
    LEGEND = LEGEND
