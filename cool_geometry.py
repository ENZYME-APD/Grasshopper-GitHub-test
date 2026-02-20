import Rhino.Geometry as rg
import random
import System.Drawing as drawing

def generate_landscape(width_count, length_count, spacing, max_height):
    points = []
    for i in range(width_count):
        for j in range(length_count):
            z = random.uniform(0, max_height)
            points.append(rg.Point3d(i * spacing, j * spacing, z))
    return points

def draw_mesh(pts, width_count, length_count, max_height):
    mesh = rg.Mesh()
    if not pts: return mesh

    for p in pts:
        mesh.Vertices.Add(p)
        # Color mapping: Green (bottom) to White (top)
        ratio = p.Z / max_height if max_height > 0 else 0
        color = drawing.Color.FromArgb(
            int(255 * ratio + 34 * (1-ratio)),  # Red
            int(255 * ratio + 139 * (1-ratio)), # Green
            int(255 * ratio + 34 * (1-ratio))   # Blue
        )
        mesh.VertexColors.Add(color)

    for i in range(width_count - 1):
        for j in range(length_count - 1):
            v1 = i * length_count + j
            v2 = (i + 1) * length_count + j
            v3 = (i + 1) * length_count + (j + 1)
            v4 = i * length_count + (j + 1)
            mesh.Faces.AddFace(v1, v2, v3, v4)

    mesh.Normals.ComputeNormals()
    return mesh