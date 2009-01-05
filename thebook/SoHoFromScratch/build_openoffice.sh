#!/bin/sh

#list1="www/firefox graphics/gimp print/acroread7 mail/thunderbird"
#list2="java/jdk14 editors/openoffice.org-2 databases/mysql-query-browser"
#list="editors/openoffice.org-2"
#list="editors/vim6 shells/bash devel/subversion net/vnc"
list="net/rdesktop"
for x in $list
do

cd /usr/ports/$x
make config-recursive

done

for x in $list
do

echo "start $(date +'%F-%T') $x" >> /root/build.log
cd /usr/ports/$x
make install package clean
echo "end $(date +'%F-%T') $x" >> /root/build.log

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
