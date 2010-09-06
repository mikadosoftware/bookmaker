#!/usr/local/bin/python

"""
silly to have as spare script but 
just write up 
"""

import os

working_dir = os.path.join(os.getcwd(), 'thebook')
dirs = os.listdir(working_dir)


dirs = [dir for dir in dirs if os.path.isdir(os.path.join(working_dir, dir))]
dirs.remove('img')

print dirs


for dir in dirs:
    dir = os.path.join(working_dir, dir)

    fo = open(os.path.join(dir, '.ppp_include'), 'w')
    s = "include: "
    for file in os.listdir(dir):
        if os.path.splitext(file)[1] == ".chp" :
            s += " " + file
    fo.write("[include]\n")
    fo.write(s)
    fo.close()
