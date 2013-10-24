model-path resources

server-version dev
# This is, oddly enough, in *reverse* order of their loading...
dc-file config/toon.dc
dc-file config/otp.dc

eventlog-host 127.0.0.1
accountdb-local-file databases/csm-cookies.db

account-server-endpoint https://www.toontownrewritten.com/api/gameserver/

default-model-extension .bam

show-total-population #t
merge-mat-tailor #t

want-pets #f
want-news-page #f
want-news-tab #f
want-housing #f
