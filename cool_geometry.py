import Rhino.Geometry as rg
import math
import random
import System.Drawing as drawing

def generate_landscape(width_count, length_count, spacing, max_height, seed, frequency, round_peaks):
    points = []
    min_offset = 0.5
    for i in range(width_count):
        for j in range(length_count):
            nx = i * frequency
            ny = j * frequency
            # Use a slightly better sine-based noise
            z_raw = (math.sin(nx + seed) * math.cos(ny + seed)) * 0.5 + 0.5
            
            if round_peaks:
                z_raw = math.pow(z_raw, 0.5)
                if z_raw > 0.8: z_raw = 0.8
            
            z = (z_raw * max_height) + min_offset
            points.append(rg.Point3d(i * spacing, j * spacing, z))
    return points

def draw_mesh(pts, width_count, length_count, max_height):
    mesh = rg.Mesh()
    if not pts or len(pts) < 4: return mesh

    # 1. ADD ALL VERTICES (Top then Bottom)
    # Top vertices (0 to N-1)
    for p in pts:
        mesh.Vertices.Add(p)
        ratio = (p.Z - 0.5) / max_height if max_height > 0 else 0
        mesh.VertexColors.Add(drawing.Color.FromArgb(int(255*ratio), 180, int(255*(1-ratio))))

    # Bottom vertices (N to 2N-1)
    base_offset = len(pts)
    for p in pts:
        mesh.Vertices.Add(p.X, p.Y, 0) # Flat base at Z=0
        mesh.VertexColors.Add(drawing.Color.DimGray)

    # 2. ADD TOP & BOTTOM FACES
    for i in range(width_count - 1):
        for j in range(length_count - 1):
            # Top Face
            v1 = i * length_count + j
            v2 = (i + 1) * length_count + j
            v3 = (i + 1) * length_count + (j + 1)
            v4 = i * length_count + (j + 1)
            mesh.Faces.AddFace(v1, v2, v3, v4)

            # Bottom Face (Reversed for correct normal)
            b1 = v1 + base_offset
            b2 = v2 + base_offset
            b3 = v3 + base_offset
            b4 = v4 + base_offset
            mesh.Faces.AddFace(b1, b4, b3, b2)

    # 3. ADD SIDE FACES (SKIRT)
    # Side 1: West (j = 0)
    for i in range(width_count - 1):
        v_curr = i * length_count
        v_next = (i + 1) * length_count
        mesh.Faces.AddFace(v_curr, v_curr + base_offset, v_next + base_offset, v_next)

    # Side 2: East (j = length_count - 1)
    for i in range(width_count - 1):
        v_curr = i * length_count + (length_count - 1)
        v_next = (i + 1) * length_count + (length_count - 1)
        mesh.Faces.AddFace(v_curr, v_next, v_next + base_offset, v_curr + base_offset)

    # Side 3: South (i = 0)
    for j in range(length_count - 1):
        v_curr = j
        v_next = j + 1
        mesh.Faces.AddFace(v_curr, v_next, v_next + base_offset, v_curr + base_offset)

    # Side 4: North (i = width_count - 1)
    for j in range(length_count - 1):
        v_curr = (width_count - 1) * length_count + j
        v_next = (width_count - 1) * length_count + j + 1
        mesh.Faces.AddFace(v_curr, v_curr + base_offset, v_next + base_offset, v_next)

    # 4. FINAL CLEANUP
    mesh.Normals.ComputeNormals()
    mesh.Compact()
    
    if mesh.IsValid:
        return mesh
    else:
        # If it's still invalid, this will help you see why in the GH panel
        return "Mesh Error: " + mesh.IsValidDetailed()