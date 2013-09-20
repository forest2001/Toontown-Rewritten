# 2013.08.22 22:22:58 Pacific Daylight Time
# Embedded file name: toontown.minigame.RingTrackGroup


class RingTrackGroup():
    __module__ = __name__

    def __init__(self, tracks, period, trackTOffsets = None, reverseFlag = 0, tOffset = 0.0):
        if trackTOffsets == None:
            trackTOffsets = [0] * len(tracks)
        self.tracks = tracks
        self.period = period
        self.trackTOffsets = trackTOffsets
        self.reverseFlag = reverseFlag
        self.tOffset = tOffset
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\RingTrackGroup.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:22:58 Pacific Daylight Time
