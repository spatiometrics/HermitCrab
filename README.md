<img src="https://github.com/spatiometrics/HermitCrab/blob/master/tutorial/hermitcrab-01.png" width="150">

Hermit Crab for Grasshopper is an open-source toolkit for Grasshopper that analyzes floorplans to find zones that aren’t conducive to social distancing -- areas like aisles or workstations where there isn’t enough room for two people to pass while maintaining the CDC-recommended six feet apart. It highlights these areas so that designers and owners can help mitigate risks by adjusting furniture or controlling traffic patterns. 

Hermit Crab is a work in progress -- we hope to hear from you with suggestions for improvement!

<img src="https://github.com/spatiometrics/HermitCrab/blob/master/tutorial/Spatio_Social-Distancing-Supermarket-2.jpg">

# Getting Started
Hermit Crab for Grasshopper is currently compatible with Grasshopper for Rhino 6 (Windows/PC). 

## Installing
Get started by downloading the latest version (email us for beta access!). Save the files in your components special folder.

## Tutorial

<img src="https://github.com/spatiometrics/HermitCrab/blob/master/tutorial/Tutorial%20200422.png">

Hermit Crab works by 1) generating circulation paths, 2) calculating clearance widths along the path, and then 3) tabulating a score for each analysis point by summing the number of nearby paths that are too narrow.

Download the sample files to get started, which are provided with the components. Sample output as visualized by Grasshopper in Rhino is below.

<img src="https://github.com/spatiometrics/HermitCrab/blob/master/tutorial/Social-Distancing-Plan.jpg">

# Components

## Circulation
Generates potential circulation paths for a surface indicating the walkable area in a plan.

<img src="https://github.com/spatiometrics/HermitCrab/blob/master/tutorial/hermit_circulation_200512.png" width="150">

### Inputs
* `AS` [**Analysis Surface**](#Analysis-Surface)
* `L` [**Voronoi Segment Length**](#Voronoi-Segment-Length) (Optional, defaults to 1)
* `T` [**Tolerance**](#Voronoi-Threshold) (Optional, defaults to 0.005)

### Outputs
* `ML` **Medial Lines**: The resulting medial line segments, corresponding to the simulated circulation paths.
* `V` **Voronoi**: The resulting voronoi cells.

## Clearance
Calculates the clearance width of a circulation segment. 

<img src="https://github.com/spatiometrics/HermitCrab/blob/master/tutorial/hermit_clearance_200512.png" width="150">

### Inputs
* `AS` [**Analysis Surface**](#Analysis-Surface)
* `CL` [**Circulation Lines**](#Circulation-Lines)

### Outputs
* `TS` **Test Segments**: Updated test segments
* `W` **Clearance Width**: The width of the passable area at the midpoint of the test segment
* `CS` **Clearance Segments**: A segment representing the passable width

## Aggregate Score

<img src="https://github.com/spatiometrics/HermitCrab/blob/master/tutorial/hermit_score_200512.png" width="150">

### Inputs
* `AS` [**Analysis Surface**](#Analysis-Surface)
* `TS` [**Test Segments**](#Test-Segments)
* `W` [**Clearance Widths**](#Clearance-Widths)
* `Th` [**Threshold Distance**](#Threshold-Distance) (Optional, defaults to 10)
* `TP` [**Test Points**](#Test-Points)
* `N` [**Number of Closest Points**](#Number-of-Closest-Points)

### Outputs
* `S` **Score**: The number of the N nearest segments that have a narrower width than the threshold distance. 

# Definitions

### Analysis Surface
A single planar surface indicating the area in which a person can walk. Holes should be cut out for any barriers such as furniture or walls.

### Circulation Lines
See [**Circulation Segments**](#Circulation-Segments)

### Circulation Segments
A list of segments to calculate the clearances at. One sample is taken at the midpoint of every circulation segment, so you may want to divide longer segments into a set of short segments. _Note that this input does not need to come directly from the circulation component -- you can draw your own segments in Rhino._

### Clearance Widths
The width of the passable area at the midpoint of the test segment (Use W, the output of the `Clearance` Component).

### Number of Closest Points
The number of closest points to use to calculate a score.

### Test Points
The analysis points for which scores should be generated.

### Test Segments
The circulation segments used in the analysis (Use TS, the output of the `Clearance` Component).

### Threshold Distance
The threshold distance to check for. 

### Voronoi Segment Length
The distance between sample points along the edge of the surface used to generate the voronoi and medial axis. Lower values will result in more accurate medial lines, but will increase computation time.

### Voronoi Threshold
The threshold for cleaning medial lines. 
