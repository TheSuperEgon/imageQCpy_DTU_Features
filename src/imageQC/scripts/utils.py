# utils.py

import math
import random

def calculate_grid_dimensions(image_width_mm, image_height_mm, roi_size_mm, zoom_level=1.0, zoom_center_x=0.0, zoom_center_y=0.0, call_id=None):
    """Beregn antal af rows og columns baseret på billedets dimensions, zoom og rotation."""
    
    # Generer et tilfældigt ID, hvis der ikke er angivet et call_id
    if call_id is None:
        call_id = random.randint(1000, 9999)

    print(f"[DEBUG calculate_grid_dimensions()] Call ID: {call_id}")
    print(f"[DEBUG calculate_grid_dimensions()] Beregning af grid-dimensioner for call ID {call_id}")

    # Tilføjer grænse for at sikre grid kun genereres ved zoom-level >= 4
    if zoom_level < 4:
        print(f"[INFO calculate_grid_dimensions()] Call ID: {call_id} - Zoom-niveau er for lavt til auto-generering af grid.")
        return 0, 0, 0.0, 0.0, 0.0, 0.0  # returnerer tomme værdier hvis zoom er for lavt
        

    print(f"[DEBUG calculate_grid_dimensions()] Beregning af grid-dimensioner")
    print(f"  ROI size (mm): {roi_size_mm}")
    print(f"  Zoom level: {zoom_level}")
    print(f"  Zoom center: ({zoom_center_x}, {zoom_center_y})")
    
    # Bruger zoom-faktor ved at justere billedbredde og -højde direkte efter zoom_level
    zoom_factor = 1 + (zoom_level - 1) * 0.7

    # Juster billeds dimensioner baseret på zoomniveau
    zoomed_width_mm = image_width_mm / zoom_factor
    zoomed_height_mm = image_height_mm / zoom_factor
    
    # Tilføj debugging-print for at sikre korrekt zoom
    print(f"[DEBUG calculate_grid_dimensions()] Zoomet bredde: {zoomed_width_mm} mm, Zoomet højde: {zoomed_height_mm} mm")
    
    # Kontroller at ROI-størrelsen er valid
    if roi_size_mm <= 0:
        print("[ERROR calculate_grid_dimensions()] Ugyldig ROI-størrelse, skal være større end 0.")
        return 0, 0, 0.0, 0.0
    
    # Beregn hvor mange ROIs der kan være i det zoomede område
    rows = math.floor(zoomed_height_mm / roi_size_mm)
    cols = math.floor(zoomed_width_mm / roi_size_mm)

    # Beregn hvor meget plads der er tilbage i sidste række og kolonne
    last_row_height = zoomed_height_mm - rows * roi_size_mm
    last_col_width = zoomed_width_mm - cols * roi_size_mm

    print(f"[calculate_grid_dimensions()]  Sidste række højde: {last_row_height}, Sidste kolonne bredde: {last_col_width}")

    # Juestering af sidste række og kolonne
    if last_row_height >= 0.5 * roi_size_mm:
        rows += 1  # inkluderer ekstra række hvis højde er stor nok
    if last_col_width >= 0.5 * roi_size_mm:
        cols += 1 # samme for kolonne

    print(f"[DEBUG calculate_grid_dimensions()] Endelige rækker: {rows}, Endelige kolonner: {cols}")

    return rows, cols, last_row_height, last_col_width, zoomed_width_mm, zoomed_height_mm