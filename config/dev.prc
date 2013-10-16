model-path resources

server-version dev
# This is, oddly enough, in *reverse* order of their loading...
dc-file config/toon.dc
dc-file config/otp.dc

accountdb-local-file databases/csm-cookies.db

account-server-endpoint https://www.toontownrewritten.com/api/gameserver/

default-model-extension .bam

want-pets #f
want-news-page #f
want-news-tab #f
