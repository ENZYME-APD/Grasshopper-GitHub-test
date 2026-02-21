import Rhino.Geometry as rg
from topologicpy.Cell import Cell
from topologicpy.Topology import Topology

def create_stacked_boxes(size):
    """Creates three boxes stacked vertically using TopologicPy"""
    cells = []
    
    # Create 3 boxes with an offset in Z
    for i in range(3):
        # Topologic uses a Dictionary or None for the origin (default is 0,0,0)
        # We then move the cell vertically based on the index
        z_offset = i * size
        origin = rg.Point3d(0, 0, z_offset)
        
        # Convert Rhino Point to Topologic-friendly list/dict if needed, 
        # but Cell.Box can take an origin point or be transformed.
        box = Cell.Box(origin=None, width=size, length=size, height=size)
        
        # Move the Topologic geometry
        if z_offset > 0:
            box = Topology.Translate(box, 0, 0, z_offset)
            
        cells.append(box)
    
    return cells

def to_rhino(topology_list):
    """Helper to convert Topologic edges to Rhino Curves"""
    rhino_curves = []
    for topo in topology_list:
        edges = Topology.Edges(topo)
        for edge in edges:
            vertices = Topology.Vertices(edge)
            p1 = rg.Point3d(vertices[0].X(), vertices[0].Y(), vertices[0].Z())
            p2 = rg.Point3d(vertices[1].X(), vertices[1].Y(), vertices[1].Z())
            rhino_curves.append(rg.LineCurve(p1, p2))
    return rhino_curves