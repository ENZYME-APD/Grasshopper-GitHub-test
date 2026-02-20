import Rhino.Geometry as rg
import math
import random
import System.Drawing as drawing

def noise(x, y, seed):
    d1 = math.sin(x * 1.0 + seed) * math.cos(y * 1.0 + seed)
    d2 = math.sin(x * 0.5 + seed * 2) * math.cos(y * 0.5 + seed * 2) * 0.5
    d3 = math.sin(x * 2.1 + seed * 0.5) * math.cos(y * 1.7 + seed * 0.5) * 0.25
    combined = (d1 + d2 + d3) / 1.75
    return combined * 0.5 + 0.5

def generate_landscape(width_count, length_count, spacing, max_height, seed, frequency, round_peaks):
    points = []
    min_offset = 0.5
    f = frequency * 0.05 
    
    # Calculate center for falloff
    cx, cy = (width_count - 1) / 2.0, (length_count - 1) / 2.0
    max_dist = math.sqrt(cx**2 + cy**2)

    for i in range(width_count):
        for j in range(length_count):
            nx, ny = i * f, j * f
            z_raw = noise(nx, ny, seed)
            
            # --- FALLOFF LOGIC ---
            # Calculate distance from center (0 to 1)
            dist = math.sqrt((i - cx)**2 + (j - cy)**2) / max_dist
            # Create a smooth bell curve for the falloff
            falloff = math.cos(dist * math.pi * 0.5)
            falloff = math.pow(max(0, falloff), 1.5)
            
            z_val = z_raw * falloff
            
            if round_peaks:
                z_val = math.pow(z_val, 0.6)
                if z_val > 0.75: z_val = 0.75 + (z_val - 0.75) * 0.1
            
            z = (z_val * max_height) + min_offset
            points.append(rg.Point3d(i * spacing, j * spacing, z))
    return points

def draw_mesh(pts, width_count, length_count, max_height):
    mesh = rg.Mesh()
    if not pts or len(pts) < 4: return mesh

    # 1. ADD VERTICES
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
            v1, v2 = i * length_count + j, (i + 1) * length_count + j
            v3, v4 = (i + 1) * length_count + (j + 1), i * length_count + (j + 1)
            mesh.Faces.AddFace(v1, v2, v3, v4) # Top
            
            b1, b2, b3, b4 = v1+base_offset, v2+base_offset, v3+base_offset, v4+base_offset
            mesh.Faces.AddFace(b1, b4, b3, b2) # Bottom

    # 3. SIDES
    for i in range(width_count - 1):
        v_w, v_wn = i * length_count, (i+1) * length_count
        mesh.Faces.AddFace(v_w, v_w + base_offset, v_wn + base_offset, v_wn)
        v_e, v_en = i * length_count + (length_count-1), (i+1) * length_count + (length_count-1)
        mesh.Faces.AddFace(v_e, v_en, v_en + base_offset, v_e + base_offset)

    for j in range(length_count - 1):
        v_s, v_sn = j, j + 1
        mesh.Faces.AddFace(v_s, v_sn, v_sn + base_offset, v_s + base_offset)
        v_n, v_nn = (width_count-1)*length_count + j, (width_count-1)*length_count + j+1
        mesh.Faces.AddFace(v_n, v_n + base_offset, v_nn + base_offset, v_nn)

    mesh.Normals.ComputeNormals()
    mesh.Compact()
    return mesh