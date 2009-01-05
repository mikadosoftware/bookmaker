#!/bin/sh

#list="www/firefox graphics/gimp print/acroread7 mail/thunderbird"
list="lang/python x11-fonts/ttmkfdir x11/xorg x11-wm/xfce4"
for x in $list
do

cd /usr/ports/$x
make config-recursive

done

for x in $list
do

cd /usr/ports/$x
make install clean 2>&1 /usr/ports/$x/buildlog.log

done



#GETTING openoffice
#OOo_2.2.0_FreeBSD62Intel_install_en-GB.tbz
#ftp -a ftp://ooopackages.good-day.net/pub/OpenOffice.org/FreeBSD/2.2/i386
#/usr/ports/java/jdk14
#editors/openoffice.org-2
#make install clean

#databases/mysql-query-browser
#bash
#
