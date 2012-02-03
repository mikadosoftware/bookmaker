=========
BookMaker
=========

Overview
--------

Bookmaker is a fairly short Content Management System.  I did not
really intend to build one, but it looks like I have.  Originally I
wanted a way to convert ReSt based files into a website, and the then
new Sphinx project from Python looked a good idea.  But it was a bit
too complex for me, I did not spend enough time getting my head around
its config stuiff (I now know why it is complex, there is no easy
solution) and so I built my own.  It grew a bit.

So, we have a script that will take a directory, assume that directory
holds

* hierachy of folders and ReSt based text files that represent the
  content to be managed.

* meta folder that holds templates and config infomration

* css - seems simple enough.  might need to enforce docutils css
  globally

* imgs (well, media) for the whole hierarchy.  Yes that could be
  better.  Well I think that hardly matters - each page refs its own
  imgs so they can be put anywhere as long as the pages keep the right
  refs.


Desired Features
----------------

allowing collaboration with git - so for example having someone push comments and spelling changes.

