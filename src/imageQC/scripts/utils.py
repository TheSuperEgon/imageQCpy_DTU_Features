# utils.py

import math
import random

def calculate_grid_dimensions(image_width_mm, image_height_mm, roi_size_mm, zoom_level=1.0, zoom_center_x=0.0, zoom_center_y=0.0):
    """Beregn antal af rows og columns baseret på billedets dimensions, zoom og rotation."""

    print(f"  ROI size (mm): {roi_size_mm}")
    print(f"  Zoom level: {zoom_level}")
    
    # Bruger zoom-faktor ved at justere billedbredde/-højde efter zoom_level
    zoom_factor = 1 + (zoom_level - 1) * 0.7

    # Juster billeds dimensioner baseret på zoomniveau
    zoomed_width_mm = image_width_mm / zoom_factor
    zoomed_height_mm = image_height_mm / zoom_factor
    print(f"[calculate_grid_dimensions()] Zommed bredde: {zoomed_width_mm} mm, Zoomet højde: {zoomed_height_mm} mm")
    
    # Kontroller at ROI-størrelsen er valid
    if roi_size_mm <= 0:
        print("[ERROR calculate_grid_dimensions()] Ugyldig ROI-størrelse, skal være større end 0.")
        return 0, 0, 0.0, 0.0
    
    # Beregner hvor mange ROIs der kan være i zoomet område
    rows = math.floor(zoomed_height_mm / roi_size_mm)
    cols = math.floor(zoomed_width_mm / roi_size_mm)

    # Beregner hvor meget plads der er tilbage i sidste række og kolonne
    last_row_height = zoomed_height_mm - rows * roi_size_mm
    last_col_width = zoomed_width_mm - cols * roi_size_mm
    print(f"[calculate_grid_dimensions()]  Sidste række højde: {last_row_height}, Sidste kolonne bredde: {last_col_width}")

    # Juestere sidste række/kolonne, hvis mindre end hel ROI tilbage
    if last_row_height < roi_size_mm:
        print(f"[calculate_grid_dimensions()] Reducerer antal rækker til {rows} for at undgå overlappende ROIs.")
    if last_col_width < roi_size_mm:
        print(f"[calculate_grid_dimensions()] Reducerer antal kolonner til {cols} for at undgå overlappende ROIs.")

    print(f"[DEBUG calculate_grid_dimensions()] Endelige rækker: {rows}, Endelige kolonner: {cols}")

    return rows, cols, last_row_height, last_col_width, zoomed_width_mm, zoomed_height_mm