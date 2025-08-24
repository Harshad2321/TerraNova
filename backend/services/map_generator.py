"""
City map generator - Creates visual maps of city layouts
"""

import os
import random
from typing import List, Dict, Tuple, Set

try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False

# Define constants for map generation
TILE_SIZE = 50  # Size of each tile in pixels
ROAD_WIDTH = 20  # Width of roads in pixels
BUILDING_MARGIN = 5  # Margin around buildings
MAP_MARGIN = 30  # Margin around the whole map

# Colors for different city elements
COLORS = {
    'road': (80, 80, 80),        # Dark gray
    'road_line': (255, 255, 255),  # White
    'house': (240, 130, 50),     # Orange
    'building': (60, 100, 190),  # Blue
    'park': (50, 180, 50),       # Green
    'market': (240, 170, 60),    # Gold
    'govt': (160, 70, 180),      # Purple
    'water': (100, 160, 230),    # Light blue
    'background': (225, 225, 205), # Light tan
}


def generate_city_map(layout: List[List[str]], city_name: str) -> str:
    """
    Generate a visual map from a city layout grid
    
    Args:
        layout: 2D grid of city elements using codes like 'R', 'H', etc.
        city_name: Name of the city for the filename and title
    
    Returns:
        str: Path to the generated map image
    """
    # Check if we have the required libraries
    if not HAS_DEPENDENCIES:
        print("Warning: numpy or PIL is not installed. Using default map.")
        return "/static/dd_map.png"
        
    height = len(layout)
    width = len(layout[0]) if height > 0 else 0
    
    # Calculate image dimensions with margins
    img_width = width * TILE_SIZE + 2 * MAP_MARGIN
    img_height = height * TILE_SIZE + 2 * MAP_MARGIN + 50  # Extra space for title
    
    # Create base image with background color
    image = Image.new('RGB', (img_width, img_height), COLORS['background'])
    draw = ImageDraw.Draw(image)
    
    # Try to load fonts - fall back to default if not available
    try:
        title_font = ImageFont.truetype("arial", 24)
        label_font = ImageFont.truetype("arial", 12)
    except IOError:
        # Default font if arial isn't available
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Draw title
    draw.text((img_width//2, 20), f"{city_name} - City Map", 
              fill=(50, 50, 100), font=title_font, anchor="mt")
    
    # Add some randomness to make it look more natural
    try:
        add_texture(image)
    except Exception as e:
        print(f"Warning: Could not add texture: {e}")
    
    # First pass: Draw base elements (parks, water)
    for y in range(height):
        for x in range(width):
            cell = layout[y][x]
            px = x * TILE_SIZE + MAP_MARGIN
            py = y * TILE_SIZE + MAP_MARGIN + 50  # Offset for title
            
            if cell == 'P':  # Park
                # Reduce parks by only drawing them with 70% probability
                if random.random() < 0.7:
                    draw_park(draw, px, py, TILE_SIZE)
    
    # Second pass: Draw roads with improved connectivity
    road_network = []
    for y in range(height):
        for x in range(width):
            if layout[y][x] == 'R':
                px = x * TILE_SIZE + MAP_MARGIN
                py = y * TILE_SIZE + MAP_MARGIN + 50
                road_network.append((px, py))
    
    # Now draw the connected road network
    draw_road_network(draw, road_network, layout, width, height)
    
    # Third pass: Draw buildings
    for y in range(height):
        for x in range(width):
            cell = layout[y][x]
            px = x * TILE_SIZE + MAP_MARGIN
            py = y * TILE_SIZE + MAP_MARGIN + 50  # Offset for title
            
            if cell == 'H':  # House
                draw_house(draw, px, py, TILE_SIZE)
            elif cell == 'B':  # Building
                draw_building(draw, px, py, TILE_SIZE)
            elif cell == 'M':  # Market
                draw_market(draw, px, py, TILE_SIZE)
            elif cell == 'G':  # Government
                draw_government(draw, px, py, TILE_SIZE)
    
    # Apply some final enhancements
    image = image.filter(ImageFilter.SMOOTH)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    # Save the image
    os.makedirs("backend/static", exist_ok=True)
    file_path = f"backend/static/{city_name.replace(' ', '_')}_map.png"
    image.save(file_path)
    
    # Return the URL path for the frontend
    return f"/static/{city_name.replace(' ', '_')}_map.png"


def add_texture(image: Image.Image):
    """Add subtle texture to make the map look less digital"""
    try:
        width, height = image.size
        noise = np.random.randint(0, 15, (height, width, 3), dtype=np.uint8)
        noise_img = Image.fromarray(noise)
        
        # Overlay noise with low opacity
        image_array = np.array(image)
        noise_array = np.array(noise_img)
        result = image_array + noise_array - image_array * noise_array / 255
        np.clip(result, 0, 255, out=result)
        return Image.fromarray(result.astype(np.uint8))
    except Exception as e:
        print(f"Warning: Could not add texture: {e}")
        return image  # Return original image if texture application fails


def draw_road_network(draw: ImageDraw.Draw, roads: List[Tuple[int, int]], 
                     layout: List[List[str]], width: int, height: int):
    """Draw a connected road network"""
    if not roads:
        return
    
    # First, fix disconnected roads by connecting them
    connected_roads = connect_roads(roads, width, height)
    
    # Create connections between roads
    for px, py in connected_roads:
        x = (px - MAP_MARGIN) // TILE_SIZE
        y = (py - MAP_MARGIN - 50) // TILE_SIZE
        
        # Draw the road segment
        draw.rectangle([px, py, px + TILE_SIZE, py + TILE_SIZE], 
                       fill=COLORS['road'])
        
        # Draw road lines
        center_x = px + TILE_SIZE // 2
        center_y = py + TILE_SIZE // 2
        
        # Count connected neighbors to determine what kind of road section this is
        neighbors = 0
        for dx, dy in [(TILE_SIZE, 0), (0, TILE_SIZE), (-TILE_SIZE, 0), (0, -TILE_SIZE)]:
            if (px + dx, py + dy) in connected_roads:
                neighbors += 1
        
        # Draw different road markings based on the type of road section
        if neighbors > 2:  # Intersection
            # Draw crosswalk-like marking
            draw.rectangle([center_x - 5, center_y - 5, center_x + 5, center_y + 5],
                          fill=COLORS['road_line'])
        elif neighbors == 2:
            # Check if horizontal road
            is_horizontal = ((px + TILE_SIZE, py) in connected_roads and (px - TILE_SIZE, py) in connected_roads)
            
            if is_horizontal:
                # Dashed center line for horizontal road
                for i in range(3):
                    draw.rectangle([px + i*(TILE_SIZE//3) + 5, center_y - 1, 
                                  px + (i+1)*(TILE_SIZE//3) - 5, center_y + 1], 
                                  fill=COLORS['road_line'])
            else:
                # Dashed center line for vertical road
                for i in range(3):
                    draw.rectangle([center_x - 1, py + i*(TILE_SIZE//3) + 5, 
                                  center_x + 1, py + (i+1)*(TILE_SIZE//3) - 5], 
                                  fill=COLORS['road_line'])
        else:
            # End of road or T-junction
            draw.rectangle([center_x - 1, center_y - 1, center_x + 1, center_y + 1],
                          fill=COLORS['road_line'])

def connect_roads(roads: List[Tuple[int, int]], width: int, height: int) -> List[Tuple[int, int]]:
    """
    Ensure all roads are connected by adding missing road segments
    
    Args:
        roads: List of (x,y) coordinates of road segments
        width: Width of the city in tiles
        height: Height of the city in tiles
        
    Returns:
        List of connected road coordinates
    """
    # Convert to grid coordinates for easier processing
    grid_roads = []
    for px, py in roads:
        x = (px - MAP_MARGIN) // TILE_SIZE
        y = (py - MAP_MARGIN - 50) // TILE_SIZE
        grid_roads.append((x, y))
    
    # Find connected components using BFS
    visited = set()
    components = []
    
    for road in grid_roads:
        if road in visited:
            continue
            
        # Start a new component
        component = []
        queue = [road]
        visited.add(road)
        
        while queue:
            current = queue.pop(0)
            component.append(current)
            
            # Check neighbors (4-directional)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                
                if (neighbor in grid_roads and 
                    neighbor not in visited and 
                    0 <= nx < width and 
                    0 <= ny < height):
                    queue.append(neighbor)
                    visited.add(neighbor)
        
        components.append(component)
    
    # If there are multiple components, connect them
    if len(components) > 1:
        # Sort components by size (largest first)
        components.sort(key=len, reverse=True)  # Largest component first
        main_component = components[0]
        
        for component in components[1:]:
            # Find closest pair between components
            min_dist = float('inf')
            closest_pair = None
            
            for road1 in main_component:
                for road2 in component:
                    dist = abs(road1[0] - road2[0]) + abs(road1[1] - road2[1])
                    if dist < min_dist:
                        min_dist = dist
                        closest_pair = (road1, road2)
            
            if closest_pair:
                # Connect the roads with a straight path
                x1, y1 = closest_pair[0]
                x2, y2 = closest_pair[1]
                
                # Create path (horizontal then vertical)
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid_roads.append((x, y1))
                
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid_roads.append((x2, y))
    
    # Ensure we don't have duplicates
    grid_roads = list(set(grid_roads))
    grid_roads = list(set(grid_roads))
    
    # Convert back to pixel coordinates
    connected_roads = []
    for x, y in grid_roads:
        px = x * TILE_SIZE + MAP_MARGIN
        py = y * TILE_SIZE + MAP_MARGIN + 50
        connected_roads.append((px, py))
    
    return connected_roads


def draw_house(draw: ImageDraw.Draw, x: int, y: int, size: int):
    """Draw a house on the map"""
    margin = BUILDING_MARGIN
    
    # Main house
    house_width = size - 2*margin
    house_height = size - 2*margin
    
    # Make houses slightly different sizes
    random_size = random.uniform(0.8, 1.0)
    house_width = int(house_width * random_size)
    house_height = int(house_height * random_size)
    
    # Randomize position a little
    x_offset = random.randint(0, size - house_width)
    y_offset = random.randint(0, size - house_height)
    
    # Base house
    draw.rectangle(
        [x + margin + x_offset, y + margin + y_offset, 
         x + margin + x_offset + house_width, y + margin + y_offset + house_height], 
        fill=COLORS['house']
    )
    
    # Roof (triangle)
    roof_height = house_height // 3
    draw.polygon(
        [
            (x + margin + x_offset, y + margin + y_offset),
            (x + margin + x_offset + house_width//2, y + margin + y_offset - roof_height),
            (x + margin + x_offset + house_width, y + margin + y_offset)
        ],
        fill=(200, 90, 40)  # Darker orange for roof
    )


def draw_building(draw: ImageDraw.Draw, x: int, y: int, size: int):
    """Draw a commercial building on the map"""
    margin = BUILDING_MARGIN
    
    # Main building
    bldg_width = size - 2*margin
    bldg_height = size - 2*margin
    
    draw.rectangle(
        [x + margin, y + margin, x + margin + bldg_width, y + margin + bldg_height], 
        fill=COLORS['building']
    )
    
    # Windows
    window_size = bldg_width // 4
    for i in range(3):
        for j in range(3):
            if random.random() < 0.8:  # Some windows might be dark
                draw.rectangle(
                    [x + margin + i*window_size + 2, 
                     y + margin + j*window_size + 2,
                     x + margin + (i+1)*window_size - 2, 
                     y + margin + (j+1)*window_size - 2], 
                    fill=(220, 220, 240)  # Light blue-white for windows
                )


def draw_park(draw: ImageDraw.Draw, x: int, y: int, size: int):
    """Draw a park area with trees"""
    # Base green area
    draw.rectangle([x, y, x + size, y + size], fill=COLORS['park'])
    
    # Add some trees and details
    for _ in range(random.randint(2, 5)):
        tree_x = x + random.randint(5, size-10)
        tree_y = y + random.randint(5, size-10)
        tree_size = random.randint(5, 10)
        
        # Tree trunk
        draw.rectangle(
            [tree_x - 1, tree_y, tree_x + 1, tree_y + tree_size], 
            fill=(90, 60, 30)  # Brown
        )
        
        # Tree top
        draw.ellipse(
            [tree_x - tree_size, tree_y - tree_size, 
             tree_x + tree_size, tree_y], 
            fill=(30, 150, 30)  # Darker green
        )


def draw_market(draw: ImageDraw.Draw, x: int, y: int, size: int):
    """Draw a market/shopping area"""
    margin = BUILDING_MARGIN
    
    # Main market building
    draw.rectangle(
        [x + margin, y + margin, x + size - margin, y + size - margin], 
        fill=COLORS['market']
    )
    
    # Market roof (slightly different color)
    draw.rectangle(
        [x + margin, y + margin, x + size - margin, y + margin + 5], 
        fill=(220, 150, 50)  # Slightly darker gold
    )
    
    # Some market stalls
    stall_size = (size - 2*margin) // 3
    for i in range(2):
        for j in range(2):
            if random.random() < 0.8:
                draw.rectangle(
                    [x + margin + i*stall_size + 2, 
                     y + margin + j*stall_size + 8,
                     x + margin + (i+1)*stall_size - 2, 
                     y + margin + (j+1)*stall_size - 2], 
                    fill=(240, 200, 140)  # Lighter color for stalls
                )


def draw_government(draw: ImageDraw.Draw, x: int, y: int, size: int):
    """Draw a government building"""
    margin = BUILDING_MARGIN
    
    # Main government building
    draw.rectangle(
        [x + margin, y + margin, x + size - margin, y + size - margin], 
        fill=COLORS['govt']
    )
    
    # Government building columns
    col_width = (size - 2*margin) // 6
    for i in range(1, 6):
        draw.rectangle(
            [x + margin + i*col_width, y + margin, 
             x + margin + i*col_width + 2, y + size - margin],
            fill=(200, 180, 220)  # Light purple
        )
    
    # Roof/dome
    draw.ellipse(
        [x + size//3, y, x + 2*size//3, y + size//4], 
        fill=(130, 50, 150)  # Darker purple
    )


def get_city_map_url(layout: List[List[str]], city_name: str) -> str:
    """Wrapper function to generate map and return URL"""
    return generate_city_map(layout, city_name)
