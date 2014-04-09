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

SuitWaves = [
    # Suits in a wave can't exceed the number of spawn points.
    # While each index is actually separate wave, they will keep
    # spawning until the intermission wave, which is defined below.

    # WAVE 1:
    [('f', 0), ('bf', 1), ('f', 0), ('f', 0), ('cc', 0), ('sc', 0), ('sc', 1), ('bf', 0), ('cc', 1)],
    [('sc', 1), ('cc', 1), ('bf', 0), ('sc', 0), ('f', 1), ('bf', 1)], # Wait Wave
    [('f', 1), ('bf', 0), ('sc', 0), ('cc', 0), ('f', 0), ('bf', 1), ('sc', 0), ('cc', 1), ('sc', 0), ('f', 0), ('bf', 1), ('bf', 0), ('f', 1), ('bf', 0)], # Intermission Wave

    # WAVE 2:
    [('pp', 0), ('dt', 0), ('cc', 1), ('tm', 0), ('bf', 2), ('b', 0), ('p', 1)],
    [('p', 1), ('b', 0), ('b', 0), ('tm', 1), ('tm', 0), ('cc', 0), ('sc', 2), ('nd', 0), ('bf', 1), ('bf', 1), ('p', 0)], # Wait Wave
    [('p', 1), ('b', 0), ('b', 1), ('tm', 1), ('tm', 1), ('cc', 0), ('sc', 2), ('nd', 0), ('bf', 2), ('bf', 2), ('p', 1), ('b', 0), ('b', 0), ('tm', 1), ('tm', 1), ('cc', 0), ('sc', 3)], # Intermission Wave

    # WAVE 3:
    [('ym', 0), ('dt', 0), ('tw', 0), ('nd', 0), ('ym', 1), ('dt', 1), ('tw', 1), ('nd', 1)],
    [('ym', 1), ('dt', 1), ('tw', 1), ('nd', 1), ('ym', 1), ('ym', 1), ('dt', 1), ('tw', 1), ('nd', 1), ('ym', 1), ('dt', 1)], # Wait Wave
    [('ym', 2), ('dt', 2), ('tw', 2), ('nd', 2), ('ym', 2), ('dt', 2), ('tw', 2), ('nd', 2), ('ym', 3), ('dt', 3), ('tw', 3), ('nd', 3), ('ym', 3), ('dt', 3), ('tw', 3), ('nd', 3), ('ym', 3)], # Intermission Wave

    # WAVE 4:
    [('mm', 0), ('ac', 0), ('bc', 0), ('gh', 0), ('mm', 0), ('ac', 0), ('bc', 0), ('gh', 0)],
    [('mm', 1), ('ac', 1), ('bc', 1), ('gh', 1), ('mm', 1)], # Wait Wave
    [('mm', 1), ('ac', 1), ('bc', 1), ('gh', 1), ('mm', 1), ('ac', 1), ('bc', 1), ('gh', 1), ('mm', 2), ('ac', 2), ('bc', 2), ('gh', 2), ('mm', 2), ('ac', 2), ('bc', 2), ('gh', 2), ('mm', 2)], # Intermission Wave

    # WAVE 5:
    [('ds', 0), ('bs', 0), ('nc', 0), ('ms', 0), ('ds', 1), ('bs', 1), ('nc', 1), ('ms', 1)],
    [('ds', 1), ('bs', 1), ('nc', 1), ('ms', 1), ('ds', 2)], # Wait Wave
    [('ds', 1), ('bs', 1), ('nc', 1), ('ms', 1), ('ds', 1), ('bs', 1), ('nc', 1), ('ms', 1), ('ds', 2), ('bs', 2), ('nc', 2), ('ms', 2), ('ds', 2), ('bs', 2), ('nc', 2), ('ms', 2), ('ds', 2)], # Intermission Wave

    # WAVE 6:
    [('hh', 0), ('sd', 0), ('mb', 0), ('tf', 0), ('hh', 1), ('sd', 1), ('mb', 1), ('tf', 1)],
    [('hh', 1), ('sd', 1), ('mb', 1), ('tf', 1), ('hh', 2)], # Wait Wave
    [('hh', 1), ('sd', 1), ('mb', 1), ('tf', 1), ('hh', 1), ('sd', 1), ('mb', 1), ('tf', 1), ('hh', 2), ('sd', 2), ('mb', 2), ('tf', 2), ('hh', 2), ('sd', 2), ('mb', 2), ('tf', 2), ('hh', 2)], # Intermission Wave

    # WAVE 7:
    [('cr', 0), ('le', 0), ('ls', 0), ('m', 0), ('cr', 1), ('le', 1), ('ls', 1), ('m', 1)],
    [('cr', 1), ('le', 1), ('ls', 1), ('m', 1), ('cr', 2)], # Wait Wave
    [('cr', 1), ('le', 1), ('ls', 1), ('m', 1), ('cr', 1), ('le', 1), ('ls', 1), ('m', 1), ('cr', 2), ('le', 2), ('ls', 2), ('m', 2), ('cr', 2), ('le', 2), ('ls', 2), ('m', 2), ('cr', 2)], # Intermission Wave

    # WAVE 8:
    [('tbc', 0), ('bw', 0), ('rb', 0), ('mh', 0), ('tbc', 1), ('bw', 1), ('rb', 1), ('mh', 1)],
    [('tbc', 1), ('bw', 1), ('rb', 1), ('mh', 1), ('tbc', 2)], # Wait Wave
    [('tbc', 2), ('bw', 2), ('rb', 2), ('mh', 2), ('tbc', 2), ('bw', 2), ('rb', 2), ('mh', 2), ('tbc', 3), ('bw', 3), ('rb', 3), ('mh', 3), ('tbc', 4), ('bw', 4), ('rb', 4), ('mh', 4), ('tbc', 4)], # Intermission Wave

    # WAVE 9: THE FINAL WAVE
    [('tbc', 2), ('bw', 1), ('rb', 3), ('mh', 3), ('tbc', 1), ('bw', 1), ('rb', 2), ('mh', 4)],
    [('tbc', 4), ('bw', 1), ('rb', 4), ('mh', 1), ('tbc', 3)], # Wait Wave
    [('tbc', 4), ('bw', 2), ('rb', 2), ('mh', 2), ('tbc', 3), ('bw', 3), ('rb', 4), ('mh', 4), ('tbc', 3), ('bw', 3), ('rb', 3), ('mh', 3), ('tbc', 4), ('bw', 4), ('rb', 4), ('mh', 4), ('tbc', 4)], # Intermission Wave
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
MoveShakerStunTime = 5.0 # Once hit by a Mover and Shaker, how long do toons have before hit again?

ToonHealAmount = 1 # How much healing does a pie on a Toon do?

# Let's define some needed files
CogSkyFile = 'phase_3.5/models/props/BR_sky'
InvasionMusicEnter = 'phase_4/audio/bgm/DD_main_temp.ogg' # TODO: Break into separate parts for a better loop

# This message is displayed upon trying to leave Toontown Central
LeaveToontownCentralAlert = "There isn't anywhere to go! Shops are closed for the election today."

# A message for Anth's credit sequence. Might end up unused.
Thanks = "Thank you so much for attending the elections! We'd like to thank you all for supporting us! See you all soon!"
