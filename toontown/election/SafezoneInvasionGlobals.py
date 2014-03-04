
# The Spawnpoint of the first cog to land
FirstSuitSpawnPoint = (65, 3.6, 4.0, 45.0)
FirstSuitType = 'ym'

# Spawn points for the Invasion Minigame
# There are currently 18 spawnpoints
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
    ( -91.7,  88.8,  -0.7,-140.0),
    (  29.7, 139.8,   2.5, -70.0),
    (  90.0, 106.0,   2.5,-100.0),
    (-127.5,  56.3,   0.5,  30.0),
    (-104.6,  51.0,  0.02, -30.0),
    (-111.3, -67.0,   0.5,  40.0),
    ( 135.0, -98.0,   2.5,-130.0),
    ( 121.6, -52.8,   2.5,  80.0),
    (  46.1,-114.8,   2.5,  60.0),
    (-113.6,  20.0,  0.03,  55.0),
]

SuitWaves = [
    # Suits in a wave can't exceed the number of spawn points.
    # While each index is actually separate wave, they will keep
    # spawning until the intermission wave, which is defined below.
    # TODO: Do full wave setup

    # WAVE 1:
    [('f', 0), ('bf', 1), ('f', 0), ('f', 0), ('cc', 0), ('sc', 0), ('sc', 1), ('bf', 0), ('cc', 1),],
    [('sc', 1), ('cc', 1), ('bf', 0), ('sc', 0), ('f', 1), ('bf', 1)], # Wait Wave
    [('f', 1), ('bf', 0), ('sc', 0), ('cc', 0), ('f', 0), ('bf', 1), ('sc', 0), ('cc', 1), ('sc', 0), ('f', 0), ('bf', 1), ('bf', 0), ('f', 1), ('bf', 0)], # Intermission Wave

    # WAVE 2:
    [('pp', 0), ('dt', 0), ('cc', 1), ('tm', 0), ('bf', 2), ('b', 0), ('p', 1)],
    [('p', 1), ('b', 0), ('b', 0), ('tm', 1), ('tm', 0), ('cc', 0), ('sc', 2), ('nd', 0), ('bf', 1), ('bf', 1), ('p', 0)], # Wait Wave
    [('p', 1), ('b', 0), ('b', 1), ('tm', 1), ('tm', 1), ('cc', 0), ('sc', 2), ('nd', 0), ('bf', 2), ('bf', 2), ('p', 1), ('b', 0), ('b', 0), ('tm', 1), ('tm', 1), ('cc', 0), ('sc', 3)], # Intermission Wave
]

# On these waves, no more waves will spawn until all suits are destroyed.
# Once the suits are destroyed, the next wave will spawn again instantly with no intermission.
SuitWaitWaves = [1, 4, 7, 10]
# These waves have a 20 second intermission period after all suits are destroyed.
SuitIntermissionWaves = [2, 5, 8, 11]
# These are the last waves that start turning cogs into Skelecogs.
# TODO: Stick Skelecogs to the floor
SuitSkelecogWaves = [12]

# This should be at least 6.5 (the suit fly-down time)
WaveBeginningTime = 10
# How long does the intermission last?
IntermissionTime = 20


# How much healing does a pie on a Toon do?
ToonHealAmount = 1

# Let's define some needed files
CogSkyFile = 'phase_3.5/models/props/BR_sky'
InvasionMusicEnter = 'phase_4/audio/bgm/DD_main_temp.ogg' # TODO: Break into separate parts for a better loop

# Leave Toontown Central Alert
LeaveToontownCentralAlert = "You can't leave Tootown Central right now."
