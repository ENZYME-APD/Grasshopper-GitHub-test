import Rhino.Geometry as rg
import math
import random
import System.Drawing as drawing

def noise(x, y, seed):
    """Better pseudo-random noise by layering sine waves at different scales"""
    # Combine multiple sine waves with different 'prime' frequencies to break the grid
    d1 = math.sin(x * 1.0 + seed) * math.cos(y * 1.0 + seed)
    d2 = math.sin(x * 0.5 + seed * 2) * math.cos(y * 0.5 + seed * 2) * 0.5
    d3 = math.sin(x * 2.1 + seed * 0.5) * math.cos(y * 1.7 + seed * 0.5) * 0.25
    
    # Normalize result to 0-1 range
    combined = (d1 + d2 + d3) / 1.75
    return combined * 0.5 + 0.5

def generate_landscape(width_count, length_count, spacing, max_height, seed, frequency, round_peaks):
    points = []
    min_offset = 0.5
    
    for i in range(width_count):
        for j in range(length_count):
            # Scale the frequency. Usually 0.05 to 0.2 is the 'sweet spot'
            # If your Freq slider is 17 (like in the screenshot), use frequency * 0.01 inside the math
            nx = i * frequency
            ny = j * frequency
            
            z_raw = noise(nx, ny, seed)
            
            if round_peaks:
                # 'Flatten' the tops using a power function
                z_raw = math.pow(z_raw, 0.6)
                if z_raw > 0.8: z_raw = 0.8 + (z_raw - 0.8) * 0.2
            
            z = (z_raw * max_height) + min_offset
            points.append(rg.Point3d(i * spacing, j * spacing, z))
    return points

def draw_mesh(pts, width_count, length_count, max_height):
    # [Keep the rest of your robust draw_mesh code exactly as it was]
    # It ensures the solid base and sides stay intact.