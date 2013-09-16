# 2013.08.22 22:13:58 Pacific Daylight Time
# Embedded file name: direct.directutil.LargeBlobSenderConsts
USE_DISK = 1
ChunkSize = 100
FilePattern = 'largeBlob.%s'

def getLargeBlobPath():
    return config.GetString('large-blob-path', 'i:\\toontown_in_game_editor_temp')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directutil\LargeBlobSenderConsts.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:58 Pacific Daylight Time
