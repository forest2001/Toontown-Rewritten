model-path resources

window-title Toontown Rewritten [DEV BUILD]

# Should these be stored in the root or a phase file?
# For now, store them in phase_3/etc/
cursor-filename phase_3/etc/toonmono.cur
icon-filename phase_3/etc/icon.ico

server-version dev
# This is, oddly enough, in *reverse* order of their loading...
dc-file config/toon.dc
dc-file config/otp.dc

eventlog-host 127.0.0.1
accountdb-local-file databases/csm-cookies.db

account-server-endpoint https://www.toontownrewritten.com/api/gameserver/

default-model-extension .bam

cog-thief-ortho 0

show-total-population #t
want-mat-all-tailors #t

want-karts #t
want-pets #f
want-news-page #f
want-news-tab #f
want-housing #f

force-holiday 1
