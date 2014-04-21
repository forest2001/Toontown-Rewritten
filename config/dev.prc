# This is the PRC configuration file for developer servers and clients. 
# If making a change here, please remember to add it to public_client.prc
# as well if the changes should be visible when pushed to the public.

# Client settings
window-title Toontown Rewritten [DEV BUILD]
server-version dev # Mirai fills this in
sync-video #f


# Resource settings
model-path resources
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


# Developer Modifications
# A few fun things for our developer build. These shouldn't go in public_client.
estate-day-night #t
want-instant-parties #t
show-total-population #f


# Holidays and Events
force-holiday-decorations 6