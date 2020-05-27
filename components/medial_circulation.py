"""Generates circulation lines for a surface indicating walkable area.
            Inputs:
                AS: Analysis Surface - A single planar surface indicating walkable area.
                L: Voronoi Segment Length - The spacing of segment samples used to generate the voronoi.
                T: Tolerance: Threshold for cleaning medial lines.
            Output:
                ML: Medial Lines
                V: Voronoi Cells"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import math 
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc

__author__ = "Jim Peraino"
__version__ = "2020.05.15"


def checkIntersection(seg, AS, tolerance):
    
    surface_intersection, P, uv, N, t, T = ghc.SurfaceXCurve(AS, seg)
    if surface_intersection != None:
        intersect_length = ghc.Length(surface_intersection)
        original_length = ghc.Length(seg)
        if (intersect_length > original_length - tolerance) and (intersect_length < original_length + tolerance):
            return 1
            
    return 0

class MyComponent(component):
    
    def RunScript(self, AS, L, T):
        
        ML = None
        V = None

        # Set defaults if no values are provided
        if L == None:
            L = 1
        if T == None:
            T = 0.005

        results = []
        medial_lines = []
        rotated_lines = []
        is_bad_lines = []
        midpoints = []
        scores = []

        # Get the analysis surface edges
        if AS:
            boundary_edges, Ei, Em = ghc.BrepEdges(AS)

        # Create voronoi analysis points
        P, T, t = ghc.DivideLength(boundary_edges, L)
        
        # Create the voronoi
        voronoi = ghc.Voronoi(P)
        voronoi_segs, V = ghc.Explode(voronoi, True)
        
        # Remove segments that are not in the medial line
        tolerance = 0.005
        for voronoi_seg in voronoi_segs:
            if checkIntersection(voronoi_seg, AS, tolerance):
                medial_lines.append(voronoi_seg)

        # Return outputs if you have them; here I try it for you:
        ML = medial_lines
        V = voronoi
        return ML, V
