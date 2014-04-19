#!/usr/bin/env python2

# This is a "pathfinding daemon" for parallelism in the invasion.
import sys
from InvasionPathDataAI import pathfinder

while True:
    navFrom, navTo, radius = input()
    path = pathfinder.planPath(navFrom, navTo, radius)
    print path
    sys.stdout.flush()
