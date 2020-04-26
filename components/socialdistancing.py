import Grasshopper, GhPython
import System
import Rhino
import math 
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc

__author__ = "Jim Peraino"
__version__ = "2020.04.23"

def checkIntersection(seg, AS, tolerance):
    
    surface_intersection, P, uv, N, t, T = ghc.SurfaceXCurve(AS, seg)
    if surface_intersection != None:
        intersect_length = ghc.Length(surface_intersection)
        original_length = ghc.Length(seg)
        print(intersect_length == original_length)
        if (intersect_length == original_length):
#        if (intersect_length > original_length - tolerance) and (intersect_length < original_length + tolerance):
            return 1, surface_intersection
            
    return 0, surface_intersection

class MyComponent(component):

    def RunScript(self, ML, AS, D, T):
        S = []
        GL = []
        BL = []
        
        # Set defaults if no values are provided
        if D == None:
            D = 10
        if T == None:
            T = 0.005



        # Rotate segments, resize, and check for intersection
        test_lines = []
        for seg in ML:
            
            # Rotate
            midpt, TT, t = ghc.EvaluateLength(seg, 0.5, True)
            
            # Resize
            SS, E = ghc.EndPoints(seg)
            V, L = ghc.Vector2Pt(midpt, SS, False)
            vect = ghc.Amplitude(V, D/2)
            G1, X = ghc.Move(midpt, vect)
            G2, X = ghc.Move(midpt, -vect)
            test_line = ghc.Line(G1, G2)
            test_line, X = ghc.Rotate(test_line, math.pi/2, midpt)
            
            # Check for intersection
            score, srf_intersection = checkIntersection(test_line, AS, 0.005)
            S.append(score)
            
            if score == 0:
                BL.append(srf_intersection)
            else:
                GL.append(srf_intersection)
            

        # Return outputs if you have them; here I try it for you:

        return S, GL, BL
