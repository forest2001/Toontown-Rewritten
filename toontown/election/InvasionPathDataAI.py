import math
from InvasionPathfinderAI import InvasionPathfinderAI

# Some helper functions for below:
def rect(x1, y1, x2, y2):
    minX = min(x1, x2)
    maxX = max(x1, x2)
    minY = min(y1, y2)
    maxY = max(y1, y2)

    return [(minX, minY), (minX, maxY), (maxX, maxY), (maxX, minY)]

def circle(x, y, radius, vertices=5):
    # Doesn't actually define a "circle" -- more of a pentagon. :)
    result = []
    for theta in range(0, 360, 360/vertices):
        theta *= math.pi/180 # Degrees to radians
        result.append((x + math.sin(theta)*radius, y + math.cos(theta)*radius))
    return result

LampPostRadius = 2
SmallTreeRadius = 2
FatTreeRadius = 4

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

    # ------Playground structure------
    # East hedges + vase plateau
    [
        (8.959,  -52.802),
        (21.272,  -36.824),
        (31.399,  -49.620),
        (22.512,  -61.303),
        (30.619,  -70.424),
        (49.778,  -71.356),
        (49.492,  -77.399),
        (27.020,  -77.335),
        (16.039,  -64.547),
    ],
    # West hedges, vase plateau + Toon HQ:
    [
        (9.888,  50.510),
        (16.599,  64.437),
        (27.340,  77.828),
        (64.581,  77.371),
        (65.007,  71.412),
        (29.839,  71.132),
        (21.573,  60.877),
        (47.202,  30.517),
        (31.546,  14.884),
        (15.470,  31.820),
        (19.444,  38.602),
    ],
    # Gazebo, west wall:
    [
        (-67.242,  -7.562),
        (-75.214,  -4.731),
        (-74.251,  -1.214),
        (-69.356,  1.903),
        (-48.325,  -0.739),
        (-46.772,  -4.773),
        (-55.003,  -7.259),
    ],
    # Gazebo, east wall:
    [
        (-55.031,  -10.064),
        (-46.126,  -11.580),
        (-48.464,  -17.958),
        (-73.640,  -18.398),
        (-76.184,  -12.535),
        (-67.085,  -10.405),
    ],
    # Lake, west of bridge, plus west bridge arch:
    [
        (-101.7, -4.5),
        (-101.7, -0.4),
        (-97.206,  19.945),
        (-99.302,  31.242),
        (-93.146,  44.609),
        (-85.646,  50.163),
        (-60.777,  48.316),
        (-50.997,  26.928),
        (-49.979,  17.245),
        (-57.210,  13.057),
        (-72.451,  15.295),
        (-82.538,  5.710),
        (-80.0, -0.4),
        (-80.0, -4.5)
    ],
    # Lake, east of bridge, plus east bridge arch:
    [
        (-80.0, -11.2),
        (-81.416,  -23.633),
        (-69.558,  -30.282),
        (-54.587,  -27.265),
        (-57.747,  -37.523),
        (-74.652,  -46.688),
        (-84.467,  -47.163),
        (-95.107,  -30.514),
        (-101.7, -11.2),
        (-101.7, -7.1),
        (-80.0, -7.1),
    ],

    # Mickey statue:
    rect(82.2, 128.0, 65.6, 113.6),

    # Goofy fountain:
    circle(93.2, -106.4, 16, 8),

    # Lamp posts:
    circle(3.8, 118.5, LampPostRadius),
    circle(117.0, 147.0, LampPostRadius),
    circle(86.8, 164.8, LampPostRadius),
    circle(43.7, -86.2, LampPostRadius),
    circle(77.3, -86.4, LampPostRadius),
    circle(58.9, 93.7, LampPostRadius),
    circle(92.8, 93.7, LampPostRadius),
    circle(132.8, -122.5, LampPostRadius),
    circle(5.0, -116.2, LampPostRadius),
    circle(109.0, -28.1, LampPostRadius),
    circle(108.2, 32.1, LampPostRadius),
    circle(33.0, 61.9, LampPostRadius),
    circle(28.9, -57.0, LampPostRadius),
    circle(-102.0, -70.5, LampPostRadius),
    circle(-129.9, -39.6, LampPostRadius),
    circle(-125, 60, LampPostRadius),

    # Trees:
    circle(-79.8, 79.5, SmallTreeRadius),
    circle(-127.0, 30.4, SmallTreeRadius),
    circle(-128.2, -24.0, SmallTreeRadius),
    circle(119.6, -127.9, SmallTreeRadius),
    circle(127.4, -59.1, SmallTreeRadius),
    circle(120.1, -44.5, SmallTreeRadius),
    circle(96.9, -146.4, SmallTreeRadius),
    circle(114.1, -57.3, SmallTreeRadius),
    circle(142.7, 108.7, FatTreeRadius),
    circle(6.3, 100.9, FatTreeRadius),
    circle(-24.0, 74.2, SmallTreeRadius),
    circle(103.4, 79.4, FatTreeRadius),
    circle(116.1, 54.8, FatTreeRadius),
    circle(6.5, -96.7, FatTreeRadius),
    circle(-53.7, -73.3, SmallTreeRadius),
    circle(55.4, 154.7, FatTreeRadius),

    # ------ Buildings ------
    # Library:
    [
        (43.596,  -19.401),
        (78.205,  -19.732),
        (86.742,  -32.561),
        (87.124,  -55.755),
        (78.209,  -65.005),
        (43.309,  -65.455),
        (34.761,  -56.078),
        (34.408,  -32.424),
    ],
    # Bank:
    [
        (55.057,  59.839),
        (58.309,  68.780),
        (93.410,  68.583),
        (97.441,  59.121),
        (97.421,  34.923),
        (93.758,  20.878),
        (58.610,  20.347),
        (54.879,  33.076),
    ],
]

# This is created globally so that all initialization path-tests are done at
# server startup rather than when the invasion begins.
pathfinder = InvasionPathfinderAI(InvasionPathPolygons)
