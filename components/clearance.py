"""Calculates the width of the passable area along each segment.
            Inputs:
                AS: Analysis Surface - A single planar surface indicating walkable area.
                CL: Circulation lines - Circulation lines to test the width of
            Output:
                TS: Test Segments - The circulation segments used in the analysis
                W: Width - The width of the passable area at the midpoint of the test segment
                CS: Clearance Segment - A segment representing the passable width
                """

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import math 
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc

__author__ = "Jim Peraino"
__version__ = "2020.05.15"

def checkIntersection(seg, AS, midpt, D):
    
    # Get the intersection of the segment and the analysis surface
    surface_intersection, P, uv, N, t, T = ghc.SurfaceXCurve(AS, seg)
    
    # If there are results:
    if surface_intersection != None:
        
        # There may be multiple intersection segments. Get only the 
        # segment that is closest to the midpoint of the test segment.
        if isinstance(surface_intersection, list):
            min_dist = 999999999
            closest_seg = None
            for intersection_seg in surface_intersection:
                cpP, cpt, cpD = ghc.CurveClosestPoint(midpt, intersection_seg)
                if cpD < min_dist:
                    min_dist = cpD
                    closest_seg = intersection_seg
            surface_intersection = closest_seg

    return surface_intersection

class MyComponent(component):

    def RunScript(self, AS, CL):
        # Initialize outputs
        S = []
        TS = CL
        W = []
        CS = []
        
        # Set defaults if no values are provided
        D = 1000

        # Iterate over each test segment
        for seg in CL:
            
            # Extend line to threshold width
            midpt, TT, t = ghc.EvaluateLength(seg, 0.5, True)
            SS, E = ghc.EndPoints(seg)
            V, L = ghc.Vector2Pt(midpt, SS, False)
            vect = ghc.Amplitude(V, D/2)
            G1, X = ghc.Move(midpt, vect)
            G2, X = ghc.Move(midpt, -vect)
            test_line = ghc.Line(G1, G2)
            
            # Rotate test line 90 degrees
            test_line, X = ghc.Rotate(test_line, math.pi/2, midpt)
            
            # Check for intersection
            srf_intersection = checkIntersection(test_line, AS, midpt, D)
            
            # Store results
            CS.append(srf_intersection)
            W.append(ghc.Length(srf_intersection))

        # Return outputs
        return TS, W, CS
