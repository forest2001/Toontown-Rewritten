# This is the PRC configuration file for a published TTR client. Note that only
# this file and Panda3D's Confauto.prc are included. Any relevant directives in
# Config.prc should be reproduced here.

# Client settings
window-title Toontown Rewritten [BETA]
server-version SERVER_VERSION_HERE
audio-library-name p3openal_audio
sync-video #f
want-dev #f
preload-avatars #t
texture-anisotropic-degree 16
language LANGUAGE_HERE

# Resources settings
model-path /
model-cache-models #f
model-cache-textures #f
vfs-mount phase_3.mf /
vfs-mount phase_3.5.mf /
vfs-mount phase_4.mf /
vfs-mount phase_5.mf /
vfs-mount phase_5.5.mf /
vfs-mount phase_6.mf /
vfs-mount phase_7.mf /
vfs-mount phase_8.mf /
vfs-mount phase_9.mf /
vfs-mount phase_10.mf /
vfs-mount phase_11.mf /
vfs-mount phase_12.mf /
vfs-mount phase_13.mf /
default-model-extension .bam

# Now that we've loaded the phase files, tell panda to trust the TTRCA
ssl-certificates phase_3/etc/TTRCA.crt
#<dev>
ssl-certificates phase_3/etc/TTRDev.crt
#</dev>

# This is the shared secret for CSMUD login
# ##### NB! Update deployment/server.prc too! #####
csmud-secret Yv1JrpTUdkX6M86h44Z9q4AUaQYdFnectDgl2I5HOQf8CBh7LUZWpzKB9FBD

# DC files are NOT configured.
# They're wrapped up into the code automatically.


# Beta Modifications
# Temporary modifications for unimplemented features go here.
want-pets #f
want-news-tab #f
want-news-page #f
want-old-fireworks #f
# This is a temporary 'fix' for DistributedSmoothNodes... probably not the permanent solution to our problem, but it works for now.
smooth-lag 0.4


# Holidays and Events
force-holiday-decorations 6


# Chat
force-avatar-understandable #t
force-player-understandable #t
