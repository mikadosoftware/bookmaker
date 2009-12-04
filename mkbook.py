#!/usr/local/bin/python
#

'''
TODO:
- need a obj for directory as well - complex to keep passing things around
- this will solve issues with the breadcrumbs. like how to know what level to pass.
  for now I am assuming first string passed in bredcrumb is at HTML_ROOT.  THis is a fine assumption.

- split the text from the generator
- make a beter HTML template, so that I can use breadcrumbs
- see about releaseing this. sort of sphinx-nose
  somewhere between sphinx and ruby jekyll



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


page object 
-----------
Is created from publish_parts in docutils, which gives back a variety of html
when processed.
attributes of page object:
['body',
 'body_pre_docinfo',
 'body_prefix',
 'body_suffix',
 'breadcrumbs',
 'docinfo',
 'encoding',
 'footer',
 'fragment',
 'get_dest_to_write_to',
 'head',
 'head_prefix',
 'header',
 'html_body',
 'html_head',
 'html_prolog',
 'html_subtitle',
 'html_title',
 'meta',
 'src',
 'stylesheet',
 'subtitle',
 'title',
 'version',
 'whole']


'''



from optparse import OptionParser
import os, sys, subprocess
import pprint
from docutils.examples import html_parts
from lib import  publish_this_file,\
getdestpath, get_html_from_rst, write_index, deploylive, \
get_tmpl_dict, check_environment, applog, dir_identity, rst_to_page
import lib
import config

from lib import BookMakerError


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
    files = [f for f in files if os.path.splitext(f)[1] in config.valid_exts]


    for f in files:
        applog("use: %s\n" % os.path.basename(f))
        #decide on source and destimation. src_dir is told to us and is not really "this"
        try:
            thisdirlist.append(lib.rst_to_page(os.path.join(full_current_root, f)))
            ### to make command feel responsive
            print '.',
        except Exception, e:
            pass # this is v bad. dont do it kids.

    ### remove files we dont want to publish.  Done after the fact because I want to use page object
    files = [page for page in thisdirlist if publish_this_file(page)]
    applog('ignore: %s\n' % ' '.join([page.src_filename for page in thisdirlist if not publish_this_file(page)]))
    return files



def run_dirs():

    """ Go through the directory holding the .chp files, and run each
        file through the rst generator(s)"""

    ignore_dirs = ('.svn', '.git')
    dir_list = {}
    
    for root, dirs, files in os.walk(config.chapters_dir):         
#        dirs = [d for d in dirs if d not in ignore_dirs]
#       for some reason the above does not work .... dirs still holds .git
        if '.git' in dirs: dirs.remove('.git')
        dir_list[dir_identity(root)] = loopthrudir(root, dirs, files)    
         
    return dir_list


def write_to_disk(dirlist):
    '''given a list of dir containing page classes write to disk

    - test if it is to be published
    - put it in the tmpl form
    '''
    tmpl = config.maintmpl
    for dir in dirlist:
        if len(dirlist[dir]) == 0: continue
        for pg in dirlist[dir]:
            dest = pg.get_dest_to_write_to()
            dest_dir = os.path.split(dest)[0]
            #
            if not lib.publish_this_file(pg): continue
          
            if not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)
            s = tmpl % {'maintext':pg.html_body, 'rhs':config.rhs_text,
                        'title':pg.title, 'html_root':config.HTMLROOT, 
                        'breadcrumbs': lib.list_to_breadtrail(pg.breadcrumbs)}  
            open(dest, 'wb').write(s)
        indexhtml = prepare_index(dirlist[dir]) 
        open(os.path.join(os.path.dirname(pg.ondisk_dest), 'index.html'), 'wb').write(indexhtml)
    write_contents(dirlist)
 
def write_contents(fulldirlist):
    ''' '''
    html = ''
#    previousdir = ''
    for dir in  sorted(fulldirlist.keys()):
        singledirlist = fulldirlist[dir]
        s, dirname = get_index_body(singledirlist)
        #is this dir a subdir of previous?
#        commonpre = os.path.commonprefix([dirname, previousdir]).replace(config.chapters_dir, '')
#        print previousdir, dirname, commonpre
#        if len(commonpre) < 2: html+='</ul>\n'
        html += '</ul>\n\n<h3>%s</h3>\n' % dirname.replace(config.chapters_dir, '')
        html += s
#        previousdir = dirname
    
    maintmpl = config.maintmpl
    fullhtml = maintmpl % {'maintext':html, 'rhs':config.rhs_text,
                        'title': 'Contents', 'html_root':config.HTMLROOT,
                        'breadcrumbs': lib.list_to_breadtrail(['contents',])}

    open(os.path.join(config.HTML_BUILD_DIR, 'contents.html'), 'wb').write(fullhtml)

def build_contents_link(page):
    '''given a page return a html fragment that is li for content page '''
    if page.title == '':
        title = os.path.split(page.dest_url)[1].replace('.html','')
    else:
        title = page.title
   
    if page.subtitle =='':
        subtitle = ''
    else:
        subtitle =  page.subtitle 


    s = '''<li>
           <a class="contentTitle" href="%s">%s</a>
           <span class="contentSubtitle">%s</span>
           </li>''' % (
                       page.dest_url, title, subtitle)
    return s
   

def get_index_body(singledirlist):
    """Given a list of page objects, build an index html page
   
    """
    tmpl = config.maintmpl
    dirname = 'unknown directory'
    s = """<ul> """
    for pg in singledirlist:
        dirname = os.path.dirname(pg.src)
        s += build_contents_link(pg)
    return (s, dirname)

def prepare_index(singledirlist):
    tmpl = config.maintmpl
    s, dirname = get_index_body(singledirlist)
    html = tmpl % {'maintext':s + "</ul>", 'rhs':config.rhs_text,
                        'title':dirname, 'html_root':config.HTMLROOT,
                  'breadcrumbs': lib.list_to_breadtrail([dirname,])}
    return html



def main():
    """ """


    ### main loop
    check_environment()
    dir_list = run_dirs()
    write_to_disk(dir_list)
#    TOC XXX
    lib.make_frontpage(["Introduction/WhatsGoingOnHere.chp",
    "Attitude/ibmadverts.chp", "SoHoFromScratch/time.chp",
    "Attitude/business_case.chp"])
    deploylive()
    

def check_chp_dir_arg_valid(chp_dir):
    ''' '''
    return os.path.isdir(chp_dir)


if __name__ == '__main__':


    ### parse options
    usage="""usage: %prog [options] location_of_chp_dir """
    parser = OptionParser(usage=usage)

    parser.add_option("--no-pdf", dest="no_pdf", action="store_true",
                      default=False, help="do not generate pdfs")

    parser.add_option("--ignore-exclude", 
                      dest="ignore_exclude", action="store_true",
                      default=False, help="if set, ignore exclude files and publish everything")

    (opts, args) = parser.parse_args()

    #check if args is a viable location for a chp_dir
    if len(args) == 1:
        chp_dir = os.path.abspath(args[0])
    else:
        raise BookMakerError("Supply only one argument - Chapter Directory Path")

    if not check_chp_dir_arg_valid(chp_dir):
        raise BookMakerError("Chapter Directory (%s) is not a dir" % chp_dir)
    else:
        config.setup_chp_dir(chp_dir)

    if opts.ignore_exclude == True:    
        config.IGNORE_EXCLUDE = True


    main()
