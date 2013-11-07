CFNoQuitButton=256
CFPageButton=16
CFQuicktalker=4
CFQuitButton=32
CFReversed=64
CFSndOpenchat=128
CFSpeech=1
CFThought=2
CFTimeout=8

CCNormal = 0
CCNoChat = 1
CCNonPlayer = 2
CCSuit = 3
CCToonBuilding = 4
CCSuitBuilding = 5
CCHouseBuilding = 6
CCSpeedChat = 7
CCFreeChat = 8

NAMETAG_COLORS = {
    CCNormal: (
        # Normal  FG                    BG
        ((0.3, 0.3, 0.7, 1.0), (0.8, 0.8, 0.8, 0.5),  # Name
         (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Click   FG                    BG
        ((0.2, 0.2, 0.5, 1.0), (0.2, 0.2, 0.2, 0.6),  # Name
         (1.0, 0.5, 0.5, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Hover   FG                    BG
        ((0.5, 0.5, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0),  # Name
         (0.0, 0.6, 0.6, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Disable FG                    BG
        ((0.3, 0.3, 0.7, 1.0), (0.8, 0.8, 0.8, 0.5),  # Name
         (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
    ),
    CCNoChat: (
        # Normal  FG                    BG
        ((0.8, 0.4, 0.0, 1.0), (1.0, 1.0, 1.0, 0.5),  # Name
         (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Click   FG                    BG
        ((1.0, 0.5, 0.5, 1.0), (0.2, 0.2, 0.2, 0.6),  # Name
         (1.0, 0.5, 0.5, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Hover   FG                    BG
        ((1.0, 0.5, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0),  # Name
         (0.0, 0.6, 0.6, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Disable FG                    BG
        ((0.6, 0.4, 0.2, 1.0), (0.8, 0.8, 0.8, 0.5),  # Name
         (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
    ),
    CCNonPlayer: (
        # Normal  FG                    BG
        ((0.8, 0.4, 0.0, 1.0), (1.0, 1.0, 1.0, 0.5),  # Name
         (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Click   FG                    BG
        ((1.0, 0.5, 0.5, 1.0), (0.2, 0.2, 0.2, 0.6),  # Name
         (1.0, 0.5, 0.5, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Hover   FG                    BG
        ((1.0, 0.5, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0),  # Name
         (0.0, 0.6, 0.6, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Disable FG                    BG
        ((0.6, 0.4, 0.2, 1.0), (0.8, 0.8, 0.8, 0.5),  # Name
         (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
    ),
    # TODO: CCSuit
    # TODO: CCToonBuilding
    # TODO: CCSuitBuilding
    # TODO: CCHouseBuilding
    # TODO: CCSpeedChat
    CCFreeChat: (
        # Normal  FG                    BG
        ((0.3, 0.3, 0.7, 1.0), (0.8, 0.8, 0.8, 0.5),  # Name
         (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Click   FG                    BG
        ((0.2, 0.2, 0.5, 1.0), (0.2, 0.2, 0.2, 0.6),  # Name
         (1.0, 0.5, 0.5, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Hover   FG                    BG
        ((0.5, 0.5, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0),  # Name
         (0.0, 0.6, 0.6, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
        # Disable FG                    BG
        ((0.3, 0.3, 0.7, 1.0), (0.8, 0.8, 0.8, 0.5),  # Name
         (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)), # Chat
    ),
}
