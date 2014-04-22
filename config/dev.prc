model-path resources

window-title Toontown Rewritten [DEV BUILD]

server-version dev
# This is, oddly enough, in *reverse* order of their loading...
dc-file config/toon.dc
dc-file config/otp.dc

eventlog-host 127.0.0.1
accountdb-local-file databases/csm-cookies.db

account-server-endpoint https://www.toontownrewritten.com/api/gameserver/

default-model-extension .bam

cog-thief-ortho 0

show-total-population #f
want-mat-all-tailors #t
want-tailor-jellybeans #t

# For alpha, we have to disable a few features for now.
want-pets #f
want-karts #t
want-housing #t
want-news-tab #f
want-news-page #f

# A few fun things for our developer build.
estate-day-night #t
want-instant-parties #t

# Here are some events to enable.
force-holiday-decorations 6
want-doomsday #f
# TODO: Fix new fireworks
want-old-fireworks #t

#goodbye vsync
sync-video #f