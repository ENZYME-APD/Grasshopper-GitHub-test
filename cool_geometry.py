import Rhino.Geometry as rg

def generate_points(count):
    points = []
    for i in range(count):
        points.append(rg.Point3d(i, i * 2, 0))
    return points

def draw_mesh(pts):
    """Creates a simple mesh strip from points"""
    mesh = rg.Mesh()
    if len(pts) < 2: return mesh
    
    for i, p in enumerate(pts):
        mesh.Vertices.Add(p.X, p.Y, p.Z)
        mesh.Vertices.Add(p.X, p.Y + 2, p.Z + 5) # Add an upper ridge
        
        if i > 0:
            # Connect vertices into faces (Quads)
            v_count = mesh.Vertices.Count
            mesh.Faces.AddFace(v_count-4, v_count-3, v_count-1, v_count-2)
            
    mesh.Normals.ComputeNormals()
    mesh.Compact()
    return mesh