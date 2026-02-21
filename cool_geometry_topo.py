import Rhino.Geometry as rg
from topologicpy.Cell import Cell
from topologicpy.CellComplex import CellComplex
from topologicpy.Graph import Graph
from topologicpy.Topology import Topology
from topologicpy.Vertex import Vertex

def find_shortest_path(x_count, y_count, spacing, ini_pt, end_pt):
    # 1. Create the Grid
    cells = []
    for i in range(x_count):
        for j in range(y_count):
            # Create box at origin then translate
            box = Cell.Box(origin=None, width=spacing, length=spacing, height=spacing)
            box = Topology.Translate(box, i * spacing, j * spacing, 0)
            cells.append(box)
    
    # 2. Fuse into a CellComplex (Shared walls)
    cell_complex = CellComplex.ByCells(cells)
    
    # 3. Create a Dual Graph (Nodes = Center of Boxes)
    # This allows pathfinding from cell-to-cell
    graph = Graph.ByTopology(cell_complex, direct=False, external=False)
    
    # 4. Map Rhino Points to the nearest Topologic Vertices/Cells
    v_start = Vertex.ByCoordinates(ini_pt.X, ini_pt.Y, ini_pt.Z)
    v_end = Vertex.ByCoordinates(end_pt.X, end_pt.Y, end_pt.Z)
    
    # Find the cells containing or nearest to these points
    t_start = Topology.NearestVertex(v_start, cell_complex)
    t_end = Topology.NearestVertex(v_end, cell_complex)
    
    # 5. Solve Shortest Path
    path_vertices = Graph.ShortestPath(graph, t_start, t_end)
    
    if not path_vertices:
        return None
        
    # 6. Convert to Rhino Polyline
    path_pts = [rg.Point3d(v.X(), v.Y(), v.Z()) for v in path_vertices]
    return rg.Polyline(path_pts).ToPolylineCurve()