# 2013.08.22 22:22:54 Pacific Daylight Time
# Embedded file name: toontown.minigame.PairingGameGlobals
import PlayingCardDeck
EasiestGameDuration = 120
HardestGameDuration = 90
EndlessGame = config.GetBool('endless-pairing-game', 0)
MaxRankIndexUsed = [7,
 7,
 7,
 8,
 9]

def createDeck(deckSeed, numPlayers):
    deck = PlayingCardDeck.PlayingCardDeck()
    deck.shuffleWithSeed(deckSeed)
    deck.removeRanksAbove(MaxRankIndexUsed[numPlayers])
    return deck


def calcGameDuration(difficulty):
    difference = EasiestGameDuration - HardestGameDuration
    adjust = difference * difficulty
    retval = EasiestGameDuration - adjust
    return retval


def calcLowFlipModifier(matches, flips):
    idealFlips = round(matches * 2 * 1.6)
    if idealFlips < 2:
        idealFlips = 2
    maxFlipsForBonus = idealFlips * 2
    retval = 0
    if flips < idealFlips:
        retval = 1
    elif maxFlipsForBonus < flips:
        retval = 0
    else:
        divisor = maxFlipsForBonus - idealFlips
        difference = maxFlipsForBonus - flips
        retval = float(difference) / divisor
    return retval
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\PairingGameGlobals.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:22:54 Pacific Daylight Time
