from __future__ import annotations
import random
from typing import List, Tuple, Optional, Dict
import numpy as np
from .tiles import TILE, LEGEND

# ---------------- helpers ----------------
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

# ---------------- terrain ----------------
def generate_terrain(size: int, terrain_kind: str) -> np.ndarray:
    g = np.zeros((size, size), dtype=int)  # EMPTY

    # coastline (left)
    if terrain_kind in ("coastal", "plains"):
        width = max(2, size // 8)
        g[:, :width] = TILE["WATER"]

    # meandering river
    x = size // 2 + random.randint(-size//8, size//8)
    for y in range(size):
        x0 = max(1, min(size-2, x))
        g[y, x0-1:x0+2] = TILE["WATER"]
        x += random.choice([-1, 0, 1])

    # mountains diagonal (more if 'mountain')
    base = size // 3
    density = 0.6 if terrain_kind == "mountain" else 0.4
    for i in range(size):
        j = (i + base) % size
        g[i, j] = TILE["MOUNTAIN"]
        if in_bounds(i, j+1, size) and random.random() < density:
            g[i, j+1] = TILE["MOUNTAIN"]

    return g

# ---------------- zoning ----------------
def allocate_zones(terrain: np.ndarray, population: int, eco_priority: int) -> np.ndarray:
    size = terrain.shape[0]
    plan = terrain.copy()

    pop_factor = max(2, min(8, population // 1500000))  # 13M => ~8

    targets = {
        "HOME": 300 * pop_factor,
        "OFFICE": 180 * pop_factor,
        "FARM": 220 * pop_factor,
        "PARK": 220 + 12 * eco_priority,
        "HOSPITAL": max(6, population // 300000),
        "SCHOOL": max(10, population // 150000),
    }

    # 1) park buffers along water
    parks_left = targets["PARK"]
    for y in range(size):
        for x in range(size):
            if plan[y, x] == TILE["EMPTY"] and is_adjacent_to(plan, y, x, [TILE["WATER"]]):
                plan[y, x] = TILE["PARK"]
                parks_left -= 1
                if parks_left <= 0:
                    break
        if parks_left <= 0:
            break

    # 2) farms near water away from mountains
    farms_left = targets["FARM"]
    for y in range(size):
        for x in range(size):
            if plan[y, x] != TILE["EMPTY"]:
                continue
            if is_adjacent_to(plan, y, x, [TILE["WATER"], TILE["PARK"]]) and not is_adjacent_to(plan, y, x, [TILE["MOUNTAIN"]]):
                plan[y, x] = TILE["FARM"]
                farms_left -= 1
                if farms_left <= 0:
                    break
        if farms_left <= 0:
            break

    # 3) homes on flat land
    homes_left = targets["HOME"]
    for y in range(size):
        for x in range(size):
            if plan[y, x] == TILE["EMPTY"] and not is_adjacent_to(plan, y, x, [TILE["MOUNTAIN"]]) and homes_left > 0:
                plan[y, x] = TILE["HOME"]
                homes_left -= 1

    # 4) offices near homes (mixed-use bias with eco)
    offices_left = targets["OFFICE"]
    bias = 0.6 if eco_priority >= 7 else 0.35
    for y in range(size):
        for x in range(size):
            if plan[y, x] == TILE["EMPTY"] and offices_left > 0 and is_adjacent_to(plan, y, x, [TILE["HOME"]]) and random.random() < bias:
                plan[y, x] = TILE["OFFICE"]
                offices_left -= 1

    # 5) hospitals/schools near homes/offices
    def place_service(tile_id: int, quota: int, near_types: List[int]):
        left = quota
        for y in range(size):
            for x in range(size):
                if plan[y, x] == TILE["EMPTY"] and is_adjacent_to(plan, y, x, near_types):
                    plan[y, x] = tile_id
                    left -= 1
                    if left <= 0: return
        for y in range(size):
            for x in range(size):
                if plan[y, x] == TILE["EMPTY"] and left > 0:
                    plan[y, x] = tile_id
                    left -= 1
                    if left <= 0: return
    place_service(TILE["HOSPITAL"], targets["HOSPITAL"], [TILE["HOME"], TILE["OFFICE"]])
    place_service(TILE["SCHOOL"], targets["SCHOOL"], [TILE["HOME"]])

    # 6) walks between homes and parks
    for y in range(1, size-1):
        for x in range(1, size-1):
            if plan[y, x] == TILE["EMPTY"] and is_adjacent_to(plan, y, x, [TILE["PARK"]]) and is_adjacent_to(plan, y, x, [TILE["HOME"]]):
                if random.random() < 0.45:
                    plan[y, x] = TILE["WALK"]

    # 7) roads grid
    step = max(4, 9 - (pop_factor // 2))  # denser for big cities
    for y in range(0, size, step):
        for x in range(size):
            if plan[y, x] in (TILE["EMPTY"], TILE["WALK"]):
                plan[y, x] = TILE["ROAD"]
    for x in range(0, size, step):
        for y in range(size):
            if plan[y, x] in (TILE["EMPTY"], TILE["WALK"]):
                plan[y, x] = TILE["ROAD"]

    # 8) metro on densest column of homes/offices + stations
    density = np.zeros_like(plan)
    density[plan == TILE["HOME"]] = 2
    density[plan == TILE["OFFICE"]] = 3
    x_peak = int(np.argmax(density.sum(axis=0)))
    for y in range(size):
        if plan[y, x_peak] in (TILE["EMPTY"], TILE["WALK"], TILE["ROAD"]):
            plan[y, x_peak] = TILE["METRO"]
    for y in range(0, size, 8):
        if is_adjacent_to(plan, y, x_peak, [TILE["HOME"], TILE["OFFICE"]]):
            plan[y, x_peak] = TILE["STATION"]

    return plan

# ---------------- metrics ----------------
def compute_metrics(plan: np.ndarray) -> Dict[str, float]:
    size = plan.shape[0]
    total = size * size
    green = np.count_nonzero(plan == TILE["PARK"]) + np.count_nonzero(plan == TILE["WALK"]) + np.count_nonzero(plan == TILE["FARM"])
    green_cover_pct = round(100 * green / total, 2)

    homes = find_tiles(plan, TILE["HOME"])
    walkable = sum(1 for (y, x) in homes if is_adjacent_to(plan, y, x, [TILE["PARK"], TILE["WALK"], TILE["STATION"]]))
    walkability_index = round(100 * (walkable / max(1, len(homes))), 2)

    transit = sum(1 for (y, x) in homes if is_adjacent_to(plan, y, x, [TILE["METRO"], TILE["STATION"]]))
    transit_coverage_pct = round(100 * (transit / max(1, len(homes))), 2)

    renew_proxy = (
        0.3 * np.count_nonzero(plan == TILE["FARM"]) +
        0.2 * np.count_nonzero(plan == TILE["PARK"]) +
        0.1 * np.count_nonzero(plan == TILE["WATER"]) +
        0.1 * np.count_nonzero(plan == TILE["MOUNTAIN"]) +
        0.3 * np.count_nonzero(plan == TILE["OFFICE"])
    )
    renewable_potential = round(100 * renew_proxy / total, 2)

    co2_index = 100 - (0.4 * green_cover_pct + 0.3 * walkability_index + 0.3 * transit_coverage_pct)
    est_co2_per_capita = round(max(5.0, co2_index / 3), 2)

    return {
        "green_cover_pct": green_cover_pct,
        "walkability_index": walkability_index,
        "renewable_potential": renewable_potential,
        "est_co2_per_capita": est_co2_per_capita,
        "transit_coverage_pct": transit_coverage_pct,
    }

# ---------------- facade ----------------
def build_plan(size: int, terrain_kind: str, population: int, eco_priority: int, seed: int = 42):
    seed_everything(seed)
    terrain = generate_terrain(size, terrain_kind)
    plan = allocate_zones(terrain, population, eco_priority)
    metrics = compute_metrics(plan)
    notes = [
        "Coastal buffer parks for flood resilience.",
        "Green corridors connect homes to parks and stations.",
        "Metro traces densest mixed-use spine; stations every ~8 blocks.",
    ]
    return {
        "legend": LEGEND,
        "size": size,
        "terrain_grid": terrain.tolist(),
        "plan_grid": plan.tolist(),
        "metrics": metrics,
        "notes": notes,
    }
