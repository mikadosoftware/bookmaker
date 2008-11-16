#!/bin/sh
###
# THis is to make a jail *after* the first jail
# with buildworld has been done (in fact I think it
# can run after host buildworld...?)
#
# basically, after we have got the binaries built
# all we need do is installworld...
#
###

HOSTNAME=$1
D=/usr/jail/$HOSTNAME
cd /usr/src
mkdir -p $D
make installworld DESTDIR=$D
make distribution DESTDIR=$D
#mount -t devfs devfs $D/dev

