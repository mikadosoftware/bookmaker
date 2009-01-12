import lib
import os

print lib.publish_this_file("thebook/Attitude", "someother.chp")
x = os.listdir("thebook/Attitude")
for f in x: print f + " ",
