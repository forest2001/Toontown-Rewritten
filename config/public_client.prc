# This is the PRC configuration file for a published TTR client. Note that only
# this file and Panda3D's Confauto.prc are included. Any relevant directives in
# Config.prc should be reproduced here.
# Comments and empty lines are stripped by Mirai's builder.

# The server version is actually a placeholder; Mirai's builder fills it in.
server-version SERVER_VERSION_HERE
# DC files are NOT configured. They're wrapped up into the code automatically.

default-model-extension .bam

show-total-population #t

# For alpha, we have to disable a few features for now.
want-pets #f
want-news-page #f
want-news-tab #f
want-housing #f

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
