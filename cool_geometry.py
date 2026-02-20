import Rhino.Geometry as rg
import random
import System.Drawing as drawing

def generate_landscape(width_count, length_count, spacing, max_height):
    points = []
    min_offset = 0.5 # As requested
    for i in range(width_count):
        for j in range(length_count):
            # Height starts at 0.5 minimum
            z = random.uniform(min_offset, max_height + min_offset)
            points.append(rg.Point3d(i * spacing, j * spacing, z))
    return points

def draw_mesh(pts, width_count, length_count, max_height):
    mesh = rg.Mesh()
    if not pts: return mesh

    # 1. Add Top Surface Vertices & Colors
    for p in pts:
        mesh.Vertices.Add(p)
        ratio = (p.Z - 0.5) / max_height if max_height > 0 else 0
        mesh.VertexColors.Add(drawing.Color.FromArgb(
            int(255 * ratio + 34 * (1-ratio)), 
            int(255 * ratio + 139 * (1-ratio)), 
            int(255 * ratio + 34 * (1-ratio))
        ))

    # 2. Add Top Surface Faces
    for i in range(width_count - 1):
        for j in range(length_count - 1):
            v1 = i * length_count + j
            v2 = (i + 1) * length_count + j
            v3 = (i + 1) * length_count + (j + 1)
            v4 = i * length_count + (j + 1)
            mesh.Faces.AddFace(v1, v2, v3, v4)

    # 3. Create the Base (Solidify)
    # Create bottom vertices at Z=0
    base_start_idx = mesh.Vertices.Count
    for p in pts:
        mesh.Vertices.Add(p.X, p.Y, 0)
        mesh.VertexColors.Add(drawing.Color.DimGray)

    # 4. Add Bottom Face (reversed order for normals)
    for i in range(width_count - 1):
        for j in range(length_count - 1):
            v1 = base_start_idx + i * length_count + j
            v2 = base_start_idx + (i + 1) * length_count + j
            v3 = base_start_idx + (i + 1) * length_count + (j + 1)
            v4 = base_start_idx + i * length_count + (j + 1)
            mesh.Faces.AddFace(v1, v4, v3, v2) # Reversed order

    # 5. Add Side Faces (The "Skirt")
    def add_skirt(idx_a, idx_b):
        # idx_a and idx_b are top indices, their base versions are +base_start_idx
        mesh.Faces.AddFace(idx_a, idx_a + base_start_idx, idx_b + base_start_idx, idx_b)

    for i in range(width_count - 1):
        # Edge 1 (Along X)
        add_skirt(i * length_count, (i + 1) * length_count)
        # Edge 2 (Opposite side)
        add_skirt((i + 1) * length_count + (length_count - 1), i * length_count + (length_count - 1))

    for j in range(length_count - 1):
        # Edge 3 (Along Y)
        add_skirt((width_count - 1) * length_count + j, (width_count - 1) * length_count + (j + 1))
        # Edge 4 (Opposite side)
        add_skirt(j + 1, j)

    mesh.Normals.ComputeNormals()
    mesh.Compact()
    return mesh