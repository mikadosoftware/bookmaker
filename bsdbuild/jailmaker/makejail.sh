#!/bin/sh
HOSTNAME=$1
D=/usr/jail/$HOSTNAME
cd /usr/src
mkdir -p $D
make -j6 world DESTDIR=$D
make distribution DESTDIR=$D
#mount_devfs devfs $D/dev
#cd /usr/src
#make clean
