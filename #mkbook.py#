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


Antecedants
-----------
This is very similar to Sphinx (www.?) - but sphinx I could not quite get to suit my needs (I may need to reexamine it)
I certainly realised I was stealing their include file idea after I wrote my own (however one can either include or exclude files in this one - I found that a bonus)

Docutils - I happily recommend this - it is fast becoming standard documentation method for Python.



Usage
-----

::

  $ <edit config file>
  $ python mkbook.py --no-pdf


Default is to only look for files called .chp

CSS
---
Jan 09
found, from joel spolsky

http://matthewjamestaylor.com/blog/ultimate-3-column-blog-style-pixels.htm

This looks a very effective solution to a problem I have long had - I just want to write simple HTML and have CSS take care of looking good (or in this case OK)

'''



from optparse import OptionParser
import os, sys, subprocess
import pprint
from docutils.examples import html_parts
from lib import  kill_pdf_odds, create_pdf, publish_this_file, getdirpath, get_html_from_rst, write_index, deploylive, strip_html, get_tmpl_dict, check_environment
#getting lazy...
from config import *




def create_html(source, destination, errors, dry_run=False):
    """given source path and dest path, convert rst into html in dest """

    #HTML
    if dry_run == True: return ""

    print "---> Starting %s to %s" % (source, destination) 
    try:
        rst_txt = open(source).read()
        (html_title, html_body) = get_html_from_rst(rst_txt)
        plain_title = strip_html(html_title)
 
        tmpl_txt = open("main.tmpl").read()                

        d = get_tmpl_dict()
        d["title"] = plain_title
        d["maintext"] =  html_title + html_body
        d["rhs"] = rhs_text


        outstr = tmpl_txt % d
        fo = open(destination, 'w')
        fo.write(outstr)
        fo.close()

        return plain_title

    except Exception, e:
        errors.append(e)

 
     
   
def loopthrudir(root, dirs, files, index_list):
    """from walk, run cmds on all files in this dir """

    thisdirlist = []
    thishtmldir = getdirpath("html", root, HTML_DIR, latex_dir) 
    thispdfdir  = getdirpath("pdf", root, HTML_DIR, latex_dir) 
    thisdir     = root

    #### bit weak
    try:
        os.mkdir(thishtmldir)
        os.mkdir(thispdfdir)
    except:
        pass


    for f in files:
        #check if want to publish
        if not publish_this_file(root, f):
            continue


        source = os.path.join(thisdir, f)
        newhtml = f.replace('.chp','.html')
        destination = os.path.join(thishtmldir, newhtml)

        
        #HTML
        page_title = create_html(source, destination, errors, opts.dry_run)
        thisdirlist.append([destination, page_title])

        if opts.no_pdf == False:          
            #LaTeX
            ltx_file = f.replace('.chp','.ltx') 
            ltx_source = os.path.join(latex_dir, ltx_file)
            create_pdf(source, ltx_source, errors)

    
    index_list[thishtmldir] = thisdirlist


###main loop
def main(index_list):
    """ Go through the directory holding the .chp files, and run each file through 
        the rst generator(s)"""

    for root, dirs, files in os.walk(chapters_dir):
        if root.find('.svn') != -1: 
            continue
        else:
            loopthrudir(root, dirs, files, index_list)    
    ### write a contents file
    write_index(index_list, HTML_DIR, rhs_text)





if __name__ == '__main__':


    ### parse options
    parser = OptionParser()
    parser.add_option("--no-pdf", dest="no_pdf", action="store_true",
                      default=False, help="do not generate pdfs")
    parser.add_option("--dry-run", dest="dry_run", action="store_true",
                      default=False, help="do not generate HTML")

    (opts, args) = parser.parse_args()

    ### main loop
    check_environment()
    main(index_list)
    deploylive()

