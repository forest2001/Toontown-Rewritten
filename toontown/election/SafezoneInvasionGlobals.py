
SuitSpawnPoints = [
    #   X       Y     Z     H
    ( -59.0,  70.0,   0.0,-149.0),
    (-122.0, -54.0,   0.5, -40.0),
    ( -23.7, -83.1,   0.5,   0.0),
    (-116.1,   7.8,   0.0, -90.0),
    (  14.0,  83.5,   2.5, 140.0),
    (  17.8, -72.4,   2.5,  45.0),
    (  10.0, -81.5,   2.5,  45.0),
    ( -55.1, -35.0,  -3.7, -60.0),
    ( -66.7,  87.8,   0.5,-150.0),
]

SuitWaves = [
    # Suits in a wave can't exceed spawn points.
    # While each index is actually separate wave, they will keep
    # spawning until the intermission wave, which is defined below.
    # TODO: Do full wave setup

    # WAVE 1:
    [('f', 1), ('ms', 4)],
    [('sc', 1), ('cc', 1), ('sc', 1)], # Wait Wave
    [('f', 2), ('bf', 2), ('sc', 2), ('cc', 2), ('f', 2), ('bf', 2), ('sc', 2), ('cc', 2), ('sc', 2)],

    # WAVE 2:
    [('ym', 2), ('dt', 2), ('tw', 2)]
]

# On these waves, no more waves will spawn until all suits are destroyed.
# Once the suits are destroyed, the next wave will spawn again instantly with no intermission.
SuitWaitWaves = [1, 4, 7, 10]
# These waves have a 20 second intermission period after all suits are destroyed.
SuitIntermissionWaves = [2, 5, 8, 11]
# These are the last waves that start turning cogs into Skelecogs.
# TODO: Skelecog fly down animation; figure out why they don't obey collisions
SuitSkelecogWaves = [1, 6, 9, 12]

# This should be at least 6.5 (the suit fly-down time)
WaveBeginningTime = 10
# How long does the intermission last?
IntermissionTime = 20


# How much healing does a pie on a Toon do?
ToonHealAmount = 1

# Let's define some needed files
CogSkyFile = 'phase_3.5/models/props/BR_sky'
InvasionMusicEnter = 'phase_4/audio/bgm/DD_main_temp.ogg' # TODO: Break into separate parts for a better loop
