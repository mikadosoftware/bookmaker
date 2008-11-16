#!/bin/sh
#### get ports, then rebuild world and kernel on a clean installed machine

pkg_add -r cvsup-without-gui
rehash
hash

cvsup /root/ports-supfile
cvsup /root/src-supfile

echo NO_PROFILE=true >> /etc/make.conf
cd /usr/src
make -j4 buildworld


cd /usr/src
make buildkernel KERNCONF=GENERIC
make installkernel KERNCONF=GENERIC

shutdown now

# cd /usr/src
# make installworld
#mergemaster


