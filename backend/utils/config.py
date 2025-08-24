import os

# Application configuration
APP_NAME = "TerraNova"
VERSION = "0.1.0"

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
MAPS_DIR = os.path.join(BASE_DIR, "..", "maps")
