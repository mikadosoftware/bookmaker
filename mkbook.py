#!/usr/local/bin/python
#

'''
:author: pbrian

==============
ReSt bookmaker
==============

This collection of files is designed to allow you to create a simple website and/or LaTeX based-book from
just templates and docutils markup (www.docutils.org).

Docutils is a useful (if occassionaly complex) python application that takes simple text based markup and converts it to
an intermediary parsed tree, then out to LaTeX or HTML etc.  A simple example is

::
   
   my heading
   ==========
   this is why ReSt is useful
   
   - it 
   - has 
   - bulletpoints


which will become


my heading
==========
this is why ReSt is useful

- it 
- has 
- bulletpoints


I have written an entire site, using this system (www.itmanagerscookbook.com) making one text file the same as one page in the website. However the structure of the site is formed from the structure of the directories I store the original text files in.

So the basics of operation are 

1. Write a few text files in ReSt, with a directory structure.
2. walk through the directories, turning the files into HTML / LaTeX but keeping the directory structure.
3. Use templates, CSS and images as needed to help things along.  
4. Have some control structure 

Process
-------

main() -- runs an os.walk over chapters_dir, passing the details of
each dir to loopthrudir(), and holds the site_dict

site_dict -- keyed to hold a rst2htmlpage obj for each chp in a dir,
within a dir dict
::

    site_obj =    metadata ....
                  contents = {'path/from/root/foodir': 
                               {'mychp': <pageobj>, ...

loopthrudir() -- for each file in src_dir 
  checks if it should be published,  asks create_html() to rst->html
  and stores in site_obj,   
  
write_index -- given site_obj, create a TOC page and a subTOC for each
dir.



Antecedants
-----------
This is very similar to Sphinx (www.?) - but sphinx I could not quite get to suit my needs (I may need to reexamine it)
I certainly realised I was stealing their include file idea after I wrote my own (however one can either include or exclude files in this one - I found that a bonus)

Docutils - I happily recommend this - it is fast becoming standard documentation method for Python.



CSS
---
Jan 09
found, from joel spolsky

http://matthewjamestaylor.com/blog/ultimate-3-column-blog-style-pixels.htm

This looks a very effective solution to a problem I have long had - I just want to write simple HTML and have CSS take care of looking good (or in this case OK)




Usage
-----

::

  $ <edit config file>
  $ python mkbook.py --no-pdf


Default is to only look for files called .chp


testings

    >>> p = create_html('/root/thebook/thebook/SoHoFromScratch', 'DNS.chp')
    >>> p.title
    u'Domain name system' 



'''



from optparse import OptionParser
import os, sys, subprocess
import pprint
from docutils.examples import html_parts
from lib import  publish_this_file,\
getdestpath, get_html_from_rst, write_index, deploylive, \
get_tmpl_dict, check_environment, applog, dir_identity
import lib


import config



def loopthrudir(full_current_root, dirs, files):
    """This does the meat of the work. 
    Go through all files in a dir, 
    pdf, or htmlise them, and return their meta data (title etc)
   

    Note on local/full
    ------------------
    I am using a tree strucutre that roots from same arbitrary point
    in a real disk tree.  So the strucutre I care about starts from
    thebook but on disk that is /foo/bar/thebook.  thebook/ is my
    local root, /foo/bar/thebook is my fullroot, but if I delve
    deeper, thebook/chapter1/ is my local_current_root
    
    Returns
    -------
    a list of all "pages" in this directory, as page-like objects.

    >>> 1
  

    """
    
    thisdirlist = []

    ### remove files we dont want to publish
    files = [f for f in files if publish_this_file(full_current_root, f)]

    for f in files:
        applog("-- %s" % os.path.basename(f))
        #decide on source and destimation. src_dir is told to us and is not really "this"
        thisdirlist.append(lib.create_html(full_current_root, f))

    return thisdirlist



def run_dirs():

    """ Go through the directory holding the .chp files, and run each
        file through the rst generator(s)"""

    ignore_dirs = ('.svn', '.git')
    dir_list = {}
    
    for root, dirs, files in os.walk(config.chapters_dir):         
        dirs = [d for d in dirs if d not in ignore_dirs]
        dir_list[dir_identity(root)] = loopthrudir(root, dirs, files)    
         
    return dir_list


def write_to_disk(dirlist):
    '''given a list of dir containing page classes write to disk'''
    for dir in dirlist:
        for pg in dirlist[dir]:
            dest = pg.get_dest_to_write_to()
            dest_dir = os.path.split(dest)[0]

            if not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)

            open(dest, 'wb').write(pg.whole)



def prepare_index(dir_list):
    """
    given a dict keyed on local_root, holding list of 
   
    dir_list = {
    """
    pass




def main():
    """ """


    ### main loop
    check_environment()
    dir_list = run_dirs()
    write_to_disk(dir_list)
#    TOC XXX
#    make_frontpage(["Introduction/WhatsGoingOnHere.chp",
#    "Attitude/ibmadverts.chp", "SoHoFromScratch/time.chp",
#    "Attitude/business_case.chp"])
    deploylive()
    



if __name__ == '__main__':


    ### parse options
    parser = OptionParser()
    parser.add_option("--no-pdf", dest="no_pdf", action="store_true",
                      default=False, help="do not generate pdfs")
    parser.add_option("--ignore-exclude", 
                      dest="ignore_exclude", action="store_true",
                      default=False, help="if set, ignore exclude files and publish everything")

    (opts, args) = parser.parse_args()
    
    if opts.ignore_exclude == True:    
        print '>>>', opts.ignore_exclude
        config.IGNORE_EXCLUDE = True


    main()
