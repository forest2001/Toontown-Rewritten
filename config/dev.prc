# This is the PRC configuration file for developer servers and clients. 
# If making a change here, please remember to add it to public_client.prc
# as well as deployment/server.prc if necessary.

# Client settings
window-title Toontown Rewritten [DEV BUILD]
server-version dev
sync-video #f
want-dev #f


# Resource settings
vfs-mount resources /
model-path /
default-model-extension .bam

# Server settings
eventlog-host 127.0.0.1
accountdb-local-file databases/csm-cookies.db
account-server-endpoint https://www.toontownrewritten.com/api/gameserver/


# DC Files
# This is, oddly enough, in *reverse* order of their loading...
dc-file config/toon.dc
dc-file config/otp.dc


# Beta Modifications
# Temporary modifications for unimplemented features go here.
want-pets #f
want-news-tab #f
want-news-page #f
want-old-fireworks #t
# This is a temporary 'fix' for DistributedSmoothNodes... probably not the permanent solution to our problem, but it works for now.
smooth-lag 0.4


# Developer Modifications
# A few fun things for our developer build. These shouldn't go in public_client.
estate-day-night #t
want-instant-parties #t
show-total-population #f
want-whitelist #f


# Holidays and Events
force-holiday-decorations 6
