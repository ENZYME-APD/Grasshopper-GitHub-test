import Rhino.Geometry as rg
from topologicpy.Cell import Cell
from topologicpy.CellComplex import CellComplex
from topologicpy.Graph import Graph
from topologicpy.Topology import Topology
from topologicpy.Vertex import Vertex

def find_shortest_path(x_count, y_count, spacing, ini_pt, end_pt, run_toggle):
    # 1. ALWAYS Generate the Grid Geometry (Fast)
    cells = []
    for i in range(x_count):
        for j in range(y_count):
            box = Cell.Box(origin=None, width=spacing, length=spacing, height=spacing)
            box = Topology.Translate(box, i * spacing, j * spacing, 0)
            cells.append(box)
    
    cell_complex = CellComplex.ByCells(cells)
    
    # Extract wires for constant preview
    grid_wires = []
    edges = Topology.Edges(cell_complex)
    for e in edges:
        v = Topology.Vertices(e)
        grid_wires.append(rg.LineCurve(rg.Point3d(v[0].X(), v[0].Y(), v[0].Z()), 
                                      rg.Point3d(v[1].X(), v[1].Y(), v[1].Z())))

    # 2. ONLY calculate path if Run is True and points exist
    path_curve = None
    if run_toggle and ini_pt and end_pt:
        # Build the Graph (The heavy part)
        graph = Graph.ByTopology(cell_complex, direct=False)
        
        v_start = Vertex.ByCoordinates(ini_pt.X, ini_pt.Y, ini_pt.Z)
        v_end = Vertex.ByCoordinates(end_pt.X, end_pt.Y, end_pt.Z)
        
        t_start = Topology.NearestVertex(v_start, cell_complex)
        t_end = Topology.NearestVertex(v_end, cell_complex)
        
        path_vertices = Graph.ShortestPath(graph, t_start, t_end)
        
        if path_vertices:
            path_pts = [rg.Point3d(v.X(), v.Y(), v.Z()) for v in path_vertices]
            path_curve = rg.Polyline(path_pts).ToPolylineCurve()
            
    return path_curve, grid_wires