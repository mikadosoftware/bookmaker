#!/bin/sh

#####
# pbrian paul@mikadosoftware.com
# date: Nov 2009
#
# 
# This is designed to execute on the remote repository running on live 
# webserver, then build the pages and build my website.
# but it does not run from the bare repo, but from the clone
# clone : /home/pbrian/clone_upstream/cookbook/mk1.sh
#
#
#####



git pull
python mkbook.py 

# run this on remote machie sh update_book.sh
