"""
Tile definitions and utilities for city planning visualization
This module provides constants and functions to represent city elements
"""

# Define tile representations for city planning
ROAD = "R"  # Road - 🛣️
HOME = "H"  # Home - 🏠
BUILDING = "B"  # Building - 🏢
PARK = "P"  # Park - 🌳
MARKET = "M"  # Market - 🛍️
GOVERNMENT = "G"  # Government building - 🏛️
EMPTY = "E"  # Empty space - ⬜

# Color mappings for frontend
TILE_COLORS = {
    ROAD: "#7f8c8d",       # Gray
    HOME: "#e74c3c",       # Red
    BUILDING: "#3498db",   # Blue
    PARK: "#2ecc71",       # Green
    MARKET: "#f39c12",     # Orange
    GOVERNMENT: "#9b59b6", # Purple
    EMPTY: "#ecf0f1",      # Light gray
}

# Functions to convert between formats
def get_emoji(tile_code):
    """Convert tile code to emoji representation"""
    emoji_map = {
        ROAD: "🛣️",
        HOME: "🏠",
        BUILDING: "🏢",
        PARK: "🌳",
        MARKET: "🛍️",
        GOVERNMENT: "🏛️",
        EMPTY: "⬜",
    }
    return emoji_map.get(tile_code, "⬜")

def get_description(tile_code):
    """Get human-readable description of a tile"""
    desc_map = {
        ROAD: "Road",
        HOME: "Residential",
        BUILDING: "Commercial Building",
        PARK: "Park/Green Space",
        MARKET: "Market/Shopping",
        GOVERNMENT: "Government/Civic",
        EMPTY: "Undeveloped Land",
    }
    return desc_map.get(tile_code, "Unknown")
