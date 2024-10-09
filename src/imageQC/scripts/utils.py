# utils.py

import math

def calculate_grid_dimensions(image_info, image_width_mm, image_height_mm, roi_size_mm, zoom_level=1.0, zoom_center_x=0.0, zoom_center_y=0.0):
    """Beregn antal af rows og columns baseret på billedets dimensions, zoom og rotation."""
    
    # tjekker om zoom-level er for lavt
    if zoom_level < 4:
        print (f"[DEBUG] Zoom level er for lavt. Returner 0 rows og columns.")
        return 0, 0, 0, 0  # returner 0 for rows og columns

    print(f"[DEBUG] Beregning af grid-dimensioner")
    print(f"  Image width (mm): {image_width_mm}")
    print(f"  Image height (mm): {image_height_mm}")
    print(f"  ROI size (mm): {roi_size_mm}")
    print(f"  Zoom level: {zoom_level}")
    print(f"  Zoom center: ({zoom_center_x}, {zoom_center_y})")

    # Juster billedets dimensioner baseret på zoomniveau
    zoomed_width_mm = image_width_mm / zoom_level
    zoomed_height_mm = image_height_mm / zoom_level

    print(f"  Zoomet område bredde: {zoomed_width_mm}, højde: {zoomed_height_mm}")

    # Beregn hvor mange ROIs der kan være i det zoomede område
    rows = math.floor(zoomed_height_mm / roi_size_mm)
    cols = math.floor(zoomed_width_mm / roi_size_mm)

    # Beregn hvor meget plads der er tilbage i sidste række og kolonne
    last_row_height = zoomed_height_mm - rows * roi_size_mm
    last_col_width = zoomed_width_mm - cols * roi_size_mm

    print(f"  Sidste række højde: {last_row_height}, Sidste kolonne bredde: {last_col_width}")
    
    # Sørg for at ROI størrelse i pixels er baseret på ROI size mm
    roi_width_in_pixels = roi_size_mm / image_info.pix[0]  # konverterer mm til pixels
    roi_height_in_pixels = roi_size_mm / image_info.pix[1]
    print(f"[DEBUG] ROI size in pixels: width: {roi_width_in_pixels}, height: {roi_height_in_pixels}")

    # Sørg for at tage højde for minimumsgrænser for sidste række og kolonne
    if last_row_height < 0.5 * roi_size_mm:
        print(f"[DEBUG] Sidste række ({last_row_height} mm) er for lille. Fjerner den.")
        last_row_height = 0
    else:
        rows += 1

    if last_col_width < 0.5 * roi_size_mm:
        print(f"[DEBUG] Sidste kolonne ({last_col_width} mm) er for lille. Fjerner den.")
        last_col_width = 0
    else:
        cols += 1

    print(f"[DEBUG] Endelige rækker: {rows}, Endelige kolonner: {cols}")

    return rows, cols, last_row_height, last_col_width