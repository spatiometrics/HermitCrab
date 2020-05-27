"""Calculates a social distancing score for any analysis point by counting the number of closest travel segments that are less wide than the threshold distance.
            Inputs:
                AS: Analysis Surface - A single planar surface indicating walkable area.
                TS: Test Segments - The circulation segments used in the analysis
                W: Width - The width of the passable area at the midpoint of the test segment
                Th: Threshold Distance - The threshold distance to check for. Defaults to 10.
                TP: Test Points - The analysis points for which scores should be generated
                N: Number of Closest Points - The number of closest points to use to calculate a score
            Output:
                S: Score - The number of the N nearest segments that have a narrower width than the threshold distance. 
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

class MyComponent(component):

    def RunScript(self, AS, TS, W, Th, TP, N):
        # Initialize outputs
        S = []
        
        # Set defaults if no values are provided
        if Th == None:
            Th = 10
        
        # Get midpoints
        midpts = []
        for seg in TS:
            eP, eT, et = ghc.EvaluateLength(seg, 0.5, True)
            midpts.append(eP)

        # Iterate over every test point
        for pt in TP:
            # Get the N closest points
            cpP, cpi, cpD = ghc.ClosestPoints(pt, midpts, N)
            score = 0
            
            # For every closest point index, add 1 to score if its width is less than Th
            for pt_index in cpi:
                if W[pt_index] < Th:
                    score +=1
            
            # Save the score
            S.append(score)

        # Return outputs
        return S
