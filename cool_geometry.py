import Rhino.Geometry as rg
import math
import random
import System.Drawing as drawing

def noise(x, y, seed):
    """Layered sine waves to simulate Perlin noise"""
    # Using different frequencies to break the grid pattern
    d1 = math.sin(x * 1.0 + seed) * math.cos(y * 1.0 + seed)
    d2 = math.sin(x * 0.5 + seed * 2) * math.cos(y * 0.5 + seed * 2) * 0.5
    d3 = math.sin(x * 2.1 + seed * 0.5) * math.cos(y * 1.7 + seed * 0.5) * 0.25
    combined = (d1 + d2 + d3) / 1.75
    return combined * 0.5 + 0.5

def generate_landscape(width_count, length_count, spacing, max_height, seed, frequency, round_peaks):
    points = []
    min_offset = 0.5
    # Scale down the frequency so standard slider values (1-20) look natural
    f = frequency * 0.05 
    
    for i in range(width_count):
        for j in range(length_count):
            nx = i * f
            ny = j * f
            z_raw = noise(nx, ny, seed)
            
            if round_peaks:
                # Smoothly plateau the higher values
                z_raw = math.pow(z_raw, 0.6)
                if z_raw > 0.75:
                    z_raw = 0.75 + (z_raw - 0.75) * 0.1
            
            z = (z_raw * max_height) + min_offset
            points.append(rg.Point3d(i * spacing, j * spacing, z))
    return points

def draw_mesh(pts, width_count, length_count, max_height):
    mesh = rg.Mesh()
    if not pts or len(pts) < 4: return mesh

    # 1. ADD VERTICES (Top then Bottom)
    for p in pts:
        mesh.Vertices.Add(p) # Top
        ratio = (p.Z - 0.5) / max_height if max_height > 0 else 0
        mesh.VertexColors.Add(drawing.Color.FromArgb(int(255*ratio), 200, 100))

    base_offset = len(pts)
    for p in pts:
        mesh.Vertices.Add(p.X, p.Y, 0) # Bottom
        mesh.VertexColors.Add(drawing.Color.FromArgb(80, 80, 80))

    # 2. FACES (Top and Bottom)
    for i in range(width_count - 1):
        for j in range(length_count - 1):
            v1 = i * length_count + j
            v2 = (i + 1) * length_count + j
            v3 = (i + 1) * length_count + (j + 1)
            v4 = i * length_count + (j + 1)
            mesh.Faces.AddFace(v1, v2, v3, v4) # Top
            
            b1, b2, b3, b4 = v1+base_offset, v2+base_offset, v3+base_offset, v4+base_offset
            mesh.Faces.AddFace(b1, b4, b3, b2) # Bottom (Reversed)

    # 3. SIDE FACES (The Skirt)
    # West & East
    for i in range(width_count - 1):
        # West
        v_curr, v_next = i * length_count, (i + 1) * length_count
        mesh.Faces.AddFace(v_curr, v_curr + base_offset, v_next + base_offset, v_next)
        # East
        v_curr, v_next = i * length_count + (length_count - 1), (i + 1) * length_count + (length_count - 1)
        mesh.Faces.AddFace(v_curr, v_next, v_next + base_offset, v_curr + base_offset)

    # South & North
    for j in range(length_count - 1):
        # South
        v_curr, v_next = j, j + 1
        mesh.Faces.AddFace(v_curr, v_next, v_next + base_offset, v_curr + base_offset)
        # North
        v_curr, v_next = (width_count-1)*length_count + j, (width_count-1)*length_count + j+1
        mesh.Faces.AddFace(v_curr, v_curr + base_offset, v_next + base_offset, v_next)

    mesh.Normals.ComputeNormals()
    mesh.Compact()
    return mesh