#!/usr/local/bin/python
#

'''
:author: pbrian


aim and fire
---
Build the rst formatted .chp files into a website, and pdfs, aiming to get to some book format eventually



The concept - look at a directory. It should be full of other directories and 
.chp files (text, called chp for chapter)

Nov 08
------
adding things like doing pdfs ...


Jan 09
------
found, from joel spolsky
http://matthewjamestaylor.com/blog/ultimate-3-column-blog-style-pixels.htm

 will steal what I can

also want to create a system that publishes some of the chapters and not others







'''



from optparse import OptionParser
import os, sys, subprocess
import pprint
from docutils.examples import html_parts
from lib import  kill_pdf_odds, create_pdf, publish_this_file, getdirpath, get_html_from_rst, write_index, deploylive, strip_html, get_tmpl_dict
#getting lazy...
from config import *




def create_html(source, destination, errors):
    """given source path and dest path, convert rst into html in dest """


    print "---> Starting %s" % source 

    #HTML
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
        if not publish_this_file(f):
            continue


        source = os.path.join(thisdir, f)
        newhtml = f.replace('.chp','.html')
        destination = os.path.join(thishtmldir, newhtml)

        
        #HTML
        page_title = create_html(source, destination, errors)
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
    (opts, args) = parser.parse_args()

    ### main loop
    main(index_list)
    deploylive()

