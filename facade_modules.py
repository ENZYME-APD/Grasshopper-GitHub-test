"""
FACADE ENGINE core MODULES LIBRARY
================================================================================
Contains explicit algorithmic operations for procedural envelope generation.
Optimized for clean 3D generation inside Rhino 8 CPython runtime environments.
================================================================================
"""
import Rhino.Geometry as rg

def generate_horizontal_bands(base_curves, floor_heights, band_thickness=0.3, division_count=3):
    """
    Extrudes clean architectural horizontal ribbons around a series of footprints.
    """
    output_bands = []
    if not base_curves: return []

    for i, crv in enumerate(base_curves):
        # Safely capture index bounds for variable height parameters
        h = floor_heights[i % len(floor_heights)]
        step_z = h / float(division_count)
        
        # Generate bands at structural intersections
        for j in range(division_count + 1):
            z_offset = j * step_z
            
            # Create a localized transformation matrix
            move_matrix = rg.Transform.Translation(0, 0, z_offset)
            moved_crv = crv.Duplicate()
            moved_crv.Transform(move_matrix)
            
            # Generate solid ribbon bands using vertical extrusions
            extrusion_path = rg.Line(moved_crv.PointAtStart, moved_crv.PointAtStart + rg.Vector3d(0, 0, band_thickness)).ToNurbsCurve()
            ext = rg.Extrusion.Create(moved_crv, band_thickness, True)
            if ext:
                output_bands.append(ext.ToBrep())
                
    return output_bands

def generate_storefront(base_curves, floor_heights, mullion_spacing=1.5, glass_inset=0.05):
    """
    Explodes floor profiles to create coordinated structural frame extrusions and window glass surfaces.
    """
    mullion_breps = []
    glass_surfaces = []
    
    for i, crv in enumerate(base_curves):
        h = floor_heights[i % len(floor_heights)]
        
        # Explode curves into individual linear or arc segments
        segments = crv.DuplicateSegments()
        if not segments: segments = [crv]
        
        for seg in segments:
            length = seg.GetLength()
            divisions = max(1, int(length / mullion_spacing))
            
            # Calculate panel spans along the path segment
            for d in range(divisions):
                t0 = float(d) / divisions
                t1 = float(d + 1) / divisions
                
                p0 = seg.PointAtNormalizedLength(t0)
                p1 = seg.PointAtNormalizedLength(t1)
                
                # 1. Structural Mullion Extrusions (Vertical posts)
                post_line = rg.LineCurve(p0, p0 + rg.Vector3d(0, 0, h))
                post_pipe = rg.Brep.CreatePipe(post_line, 0.05, False, rg.PipeCapMode.Flat, True, 0.01, 0.1)
                if post_pipe: mullion_breps.extend(post_pipe)
                
                # 2. Procedural Glass Planes
                # Generate localized plane system for the individual glass panels
                plane_vector = p1 - p0
                normal_vector = rg.Vector3d.CrossProduct(plane_vector, rg.Vector3d.ZAxis)
                normal_vector.Unitize()
                
                # Displace the panel slightly inward matching structural framing standards
                offset_vector = normal_vector * glass_inset
                inset_p0 = p0 + offset_vector
                inset_p1 = p1 + offset_vector
                
                # Build the planar window surface boundaries
                glass_profile = rg.Polyline([
                    inset_p0, 
                    inset_p1, 
                    inset_p1 + rg.Vector3d(0, 0, h), 
                    inset_p0 + rg.Vector3d(0, 0, h), 
                    inset_p0
                ]).ToNurbsCurve()
                
                planar_breps = rg.Brep.CreatePlanarBreps(glass_profile, 0.01)
                if planar_breps: glass_surfaces.extend(planar_breps)
                
    return mullion_breps, glass_surfaces