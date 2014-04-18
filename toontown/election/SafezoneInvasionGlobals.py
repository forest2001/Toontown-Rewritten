import random

FirstSuitSpawnPoint = (65, -1, 4.0, 45.0)

# The position of the Finale suit
# Spawns at SuitSpawnPoints # 3
FinaleSuitDestination = (29.3, -5.0)

# Lets give the Finale suit a special name
# This one is surprisingly fitting, because of the election -- http://en.wikipedia.org/wiki/Ambush_marketing
FinaleSuitName = 'Director of\nAmbush Marketing\nSupervisor\nLevel 50'

# Add a few phrases for the cog to say
FinaleSuitPhrases = [
    # The Director has landed
    "Apparently our marketing strategies haven't exactly appealed to you \"Toons\". I've been sent in to give you an offer that you can't refuse.",
    "I suppose you could say that \"I'm the boss.\"",
    # Time to find Flippy, we'll do some brainstorming along the way
    "I'll be needing to speak with your President directly."
    "I'm prepared to close this deal quickly.",
    "Relax, you'll find this is for the best.",
    "At this rate I'll need to liquidate toons from the picture.",
    "I assure you that you'll find no greater offer.",
    "The Chairman won't be happy until you are.",
    # We arrive at Flippy
    "Ah, finally. The toon I've been searching for.",
    "I hope you won't pull out of the deal like your predecessor.",
    "Don't worry, he is in safe keeping now."
]

FinaleSuitAttackDamage = 10
FinaleSuitAttackDelay = 10 # Wait 10 seconds before jumping again

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

suitLevels = [
    0,
    1,
    2,
    3,
    4
]
sellbotSuits = [
    'cc',
    'tm',
    'nd',
    'gh',
    'ms',
    'tf',
    'm',
    'mh'
]
cashbotSuits = [
    'sc',
    'pp',
    'tw',
    'bc',
    'nc',
    'mb',
    'ls',
    'rb'
]
lawbotSuitTypes = [
    'bf',
    'b',
    'dt',
    'ac',
    'bs',
    'sd',
    'le',
    'bw'
]
bossbotSuits = [
    'f',
    'p',
    'ym',
    'mm',
    'ds',
    'hh',
    'cr',
    'tbc'
]


def generateSuits(numberOfSuits, suitLevelRange=[0, 0], suitRange=[0, 0], wantExtraShakers=False):
    suits = [sellbotSuits, cashbotSuits, lawbotSuitTypes, bossbotSuits] # Suit arrays
    wave = []
    if wantExtraShakers:
        wave = [(random.choice(suits)[random.randint(suitRange[0], suitRange[1])], 
             random.randint(suitLevelRange[0], suitLevelRange[1])) 
             for k in range(numberOfSuits)]
        wave.append(('ms', 4))
        wave.append(('ms', 4))
    else:
        wave = [(random.choice(suits)[random.randint(suitRange[0], suitRange[1])], 
             random.randint(suitLevelRange[0], suitLevelRange[1])) 
             for k in range(numberOfSuits)]
    return wave

SuitWaves = [
    # Suits in a wave can't exceed the number of spawn points.
    # While each index is actually separate wave, they will keep
    # spawning until the intermission wave, which is defined below.

    # WAVE 1:
    generateSuits(10, [3, 4], [0, 0]),
    generateSuits(13, [3, 4], [0, 0]), # Wait Wave
    generateSuits(17, [2, 3], [0, 0]), # Intermission Wave

    # WAVE 2:
    generateSuits(11, [2, 3], [0, 1]),
    generateSuits(14, [2, 2], [0, 1]), # Wait Wave
    generateSuits(17, [2, 3], [0, 1]), # Intermission Wave

    # WAVE 3:
    generateSuits(8,  [2, 3], [1, 2]),
    generateSuits(11, [2, 2], [2, 2]), # Wait Wave
    generateSuits(17, [2, 3], [2, 2]), # Intermission Wave

    # WAVE 4:
    generateSuits(8,  [2, 3], [2, 3]),
    generateSuits(11, [2, 2], [3, 3]), # Wait Wave
    generateSuits(17, [2, 3], [3, 3]), # Intermission Wave

    # WAVE 5:
    generateSuits(8,  [0, 2], [3, 4]),
    generateSuits(11, [2, 4], [4, 4]), # Wait Wave
    generateSuits(17, [2, 3], [4, 4]), # Intermission Wave

    # WAVE 6:
    generateSuits(8,  [1, 2], [4, 5]),
    generateSuits(11, [1, 4], [5, 5], True), # Wait Wave
    generateSuits(16, [2, 3], [5, 5], True), # Intermission Wave

    # WAVE 7:
    generateSuits(8,  [0, 2], [5, 6], True),
    generateSuits(11, [1, 2], [6, 6], True), # Wait Wave
    generateSuits(16, [2, 3], [6, 6], True), # Intermission Wave

    # WAVE 8:
    generateSuits(10, [1, 3], [6, 7], True),
    generateSuits(15, [1, 4], [7, 7], True), # Wait Wave
    generateSuits(16, [2, 4], [7, 7], True), # Intermission Wave

    # WAVE 9: THE FINAL WAVE
    generateSuits(10, [1, 3], [6, 7], True),
    generateSuits(15, [1, 4], [7, 7], True), # Wait Wave
    generateSuits(16, [2, 4], [7, 7], True), # Intermission Wave
]

# On these waves, no more waves will spawn until all suits are destroyed.
# Once the suits are destroyed, the next wave will spawn again instantly with no intermission.
SuitWaitWaves = [1, 4, 7, 10, 13, 16, 19, 22, 25]

# These waves have a 20 second intermission period after all suits are destroyed.
SuitIntermissionWaves = [2, 5, 8, 11, 14, 17, 20, 23, 26]

# These are the last waves that start turning cogs into Skelcogs.
SuitSkelecogWaves = [24, 25, 26]

WaveBeginningTime = 10 # This should be at least 6.5 (the suit fly-down time)
IntermissionTime = 20 # How long does the intermission last?

StandardSuitDamage = 5 # How much damage does a standard suit's attack do?
MoveShakerDamageRadius = 3 # How much damage does a Move and Shaker's attack do?
MoveShakerRadius = 20 # And it's attack radius?
MoveShakerStunTime = 5 # Once hit by a Mover and Shaker, how long do toons have before hit again?

ToonHealAmount = 1 # How much healing does a pie on a Toon do?

# Let's define some needed files
CogSkyFile = 'phase_3.5/models/props/BR_sky'
InvasionMusicEnter = 'phase_4/audio/bgm/DD_main_temp.ogg' # TODO: Break into separate parts for a better loop

# This message is displayed upon trying to leave Toontown Central
LeaveToontownCentralAlert = "There isn't anywhere to go! Shops are closed for the election today."

# A message for Anth's credit sequence. Might end up unused.
Thanks = "Thank you so much for attending the elections! We'd like to thank you all for supporting us! See you all soon!"
