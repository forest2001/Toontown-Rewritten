from InvasionPathfinderAI import InvasionPathfinderAI

# All of the polygons that define where Cogs can and can't walk.
# NOTE: All of the polygons must have their vertices defined in clockwise order,
# because the pathfinding system uses the winding order to figure out which side
# of a vertex is the "inside" and which side is the "outside". The exception to
# this is the outer boundary, which is wound CCW so that it is inside-out (i.e.
# so that it has the "solid" part on the outside)
InvasionPathPolygons = [
    # Outermost loop, in CCW order
    [
        (-137.450,  -51.427),
        (-119.881,  -74.713),
        (-100.795,  -85.732),
        (-96.119,  -74.947),
        (-83.126,  -78.332),
        (-72.080,  -85.662),
        (-19.082,  -88.174),
        (-6.902,  -97.155),
        (11.642,  -137.324),
        (54.244,  -159.422),
        (62.807,  -140.516),
        (79.758,  -134.607),
        (96.999,  -156.466),
        (111.549,  -140.474),
        (119.513,  -133.021),
        (135.035,  -130.766),
        (146.553,  -103.095),
        (147.000,  -84.488),
        (129.406,  -49.517),
        (98.970,  -77.012),
        (75.199,  -78.546),
        (73.051,  -71.517),
        (92.343,  -69.806),
        (116.840,  -28.886),
        (108.901,  -23.650),
        (110.660,  -12.144),
        (110.660,  14.838),
        (110.663,  25.391),
        (92.463,  69.442),
        (89.146,  78.347),
        (95.889,  78.483),
        (121.791,  38.095),
        (146.897,  80.948),
        (144.111,  119.929),
        (121.629,  147.766),
        (117.107,  140.138),
        (101.144,  151.732),
        (93.266,  156.592),
        (87.937,  160.670),
        (57.207,  162.101),
        (11.816,  135.597),
        (8.116,  118.877),
        (-6.975,  99.351),
        (-15.909,  90.814),
        (-34.585,  84.513),
        (-61.211,  88.873),
        (-79.912,  96.907),
        (-114.612,  74.578),
        (-121.966,  63.502),
        (-133.772,  60.764),
        (-144.778,  28.343),
        (-138.461,  17.461),
        (-138.369,  -8.583),
        (-145.703,  -25.070),
    ],

    # Mickey statue:
    [
        (82.227,  128.010),
        (82.103,  114.525),
        (67.323,  113.691),
        (65.675,  127.920),
    ],
]

# This is created globally so that all initialization path-tests are done at
# server startup rather than when the invasion begins.
pathfinder = InvasionPathfinderAI(InvasionPathPolygons)
