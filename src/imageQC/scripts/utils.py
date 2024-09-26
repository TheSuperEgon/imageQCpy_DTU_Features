# utils.py

import math

def calculate_grid_dimensions(image_width_mm, image_height_mm, roi_size_mm):
    """Beregn antal af rows og columns baseret på billedets dimensions og juster sidste row/column."""
    
    print(f"[DEBUG] Beregning af grid-dimensioner")
    print(f"  Image width (mm): {image_width_mm}")
    print(f"  Image height (mm): {image_height_mm}")
    print(f"  ROI size (mm): {roi_size_mm}")
    
    # Beregn hvor mange hele ROIs der kan være i både bredden og højden
    rows = math.floor(image_height_mm / roi_size_mm)
    cols = math.floor(image_width_mm / roi_size_mm)

    print(f"  Beregnede rækker: {rows}, Beregnede kolonner: {cols}")
    
    # Beregn hvor meget plads der er tilbage i sidste række og kolonne
    last_row_height = image_height_mm - rows * roi_size_mm
    last_col_width = image_width_mm - cols * roi_size_mm

    print(f"  Sidste række højde: {last_row_height}, Sidste kolonne bredde: {last_col_width}")

    # Sørg for at tage højde for minimumsgrænser for sidste række og kolonne
    # Vi fjerner de sidste række og kolonne, hvis de er mindre end halvdelen af ROI-størrelsen
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