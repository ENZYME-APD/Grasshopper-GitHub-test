import Rhino.Geometry as rg
import random

def generate_landscape(width_count, length_count, spacing, max_height):
    """Generates a grid of points with randomized Z values"""
    points = []
    for i in range(width_count):
        for j in range(length_count):
            x = i * spacing
            y = j * spacing
            # Create a random height
            z = random.uniform(0, max_height)
            points.append(rg.Point3d(x, y, z))
    return points

def draw_mesh(pts, width_count, length_count):
    """Connects a grid of points into a mountain mesh"""
    mesh = rg.Mesh()
    if not pts: return mesh

    # Add all vertices to mesh
    for p in pts:
        mesh.Vertices.Add(p)

    # Generate faces by iterating through the grid
    for i in range(width_count - 1):
        for j in range(length_count - 1):
            # Calculate vertex indices for a quad face
            v1 = i * length_count + j
            v2 = (i + 1) * length_count + j
            v3 = (i + 1) * length_count + (j + 1)
            v4 = i * length_count + (j + 1)
            
            mesh.Faces.AddFace(v1, v2, v3, v4)

    mesh.Normals.ComputeNormals()
    mesh.Compact()
    return mesh