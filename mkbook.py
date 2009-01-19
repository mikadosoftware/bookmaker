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

main() runs an os.walk over chapters_dir, passing the details of each dir to loopthrudir()
loopthrudir() defines the dest directories, and for each file in src_dir 
  checks if it should be published, creates dest paths, asks create_html() to rst-html and write to disk,
  stores a dict of data about that page in index_list (dict by section)

create_html() calls rst to get the html of the page, then grabs the main.tmpl and passes in html and other data 
writes that file to the dest location.





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
from lib import  kill_pdf_odds, create_pdf, publish_this_file, getdirpath, get_html_from_rst, write_index, deploylive, get_tmpl_dict, check_environment
#getting lazy...
from config import *




def create_html(source, destination, dry_run=False):
    """
    given source path and dest path, convert rst into html in dest 

    returns
    -------
    a dictionary representing the returns from rst conversion and 
    src, dest, errors in conversion

    """
    #dry run test
    if dry_run == True: return ""
    errors_converting_page = []
    
    print "---> convert %s to %s" % (source, destination) 
    try:
        rst_txt = unicode(open(source).read(),'utf8') #i should save all my files as utf8 anyway
        page_info = get_html_from_rst(rst_txt) #now have html plus meta data

    #problems getting rst to html - if it is severe, well do not publish it!!   
    except Exception, e:
        raise e  



    #write out tmpl to destination
    tmpl_txt = open("main.tmpl").read()                

    d = get_tmpl_dict()
    d["title"] = page_info['title']
    d["maintext"] =  page_info['html_body']
    d["rhs"] = rhs_text
    d['subtitle'] = page_info['subtitle']

    outstr = tmpl_txt % d
    fo = open(destination, 'w')
    fo.write(outstr)
    fo.close()

    page_info["src"] = source
    page_info["dest"] = destination
    page_info["errors"] = errors_converting_page

    return page_info


 
     
   
def loopthrudir(root, dirs, files):
    """This does the meat of the work. 
    Go through all files in a dir, 
    pdf, or htmlise them, and return their meta data (title etc)
   
    Returns
    -------
    a list of all "pages" in this directory, as page-like objects.
   
    """

    thisdirlist = []
    # '''given the root of where the walk is, decide what the html path is bit 
    #we do this cos the html destimation is emtpy and we need to mirror it
    src_dir     = root
    dest_htmldir = getdirpath("html", src_dir) 
    dest_pdfdir  = getdirpath("pdf", src_dir) 


    #### bit weak
    try:
        os.mkdir(dest_htmldir)
        os.mkdir(dest_pdfdir)
    except:
        pass


    for f in files:
        print "-- %s" % os.path.basename(f)
        #check if want to publish
        if not publish_this_file(root, f):
            continue


        #decide on source and destimation. src_dir is told to us and is not really "this"
        source = os.path.join(src_dir, f)
        newhtml = f.replace('.chp','.html')
        destination = os.path.join(dest_htmldir, newhtml)

        
        #create HTML, return a dict that understand what the page is, holds titles etc
        page_info = create_html(source, destination, opts.dry_run)
        thisdirlist.append(page_info)


        if opts.no_pdf == False:          
            #LaTeX
            ltx_file = f.replace('.chp','.ltx') 
            ltx_source = os.path.join(latex_dir, ltx_file)
            create_pdf(source, ltx_source, errors)

    return thisdirlist


###main loop
def main(index_list):
    """ Go through the directory holding the .chp files, and run each file through 
        the rst generator(s)"""

    ignore_dirs = ('.svn', '.git')
    

    for root, dirs, files in os.walk(chapters_dir):
        for d in ignore_dirs:
            if root.find(d) != -1: 
                continue
            else:
                index_list[root] = loopthrudir(root, dirs, files)    

    ### write a contents file
    write_index(index_list,  rhs_text)






if __name__ == '__main__':


    ### parse options
    parser = OptionParser()
    parser.add_option("--no-pdf", dest="no_pdf", action="store_true",
                      default=False, help="do not generate pdfs")
    parser.add_option("--dry-run", dest="dry_run", action="store_true",
                      default=False, help="do not generate HTML")

    (opts, args) = parser.parse_args()

    index_list = {} 

    ### main loop
    check_environment()
    main(index_list)
    deploylive()

