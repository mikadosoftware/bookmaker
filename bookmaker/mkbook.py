#!/usr/local/bin/python
#

'''
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


TODO
----

* alter how I handle config - I made my perennial mistake of using a
  py file for config, which means I need to know where it is to import
  it - but the config file is supplied by the content, so to import it
  you need to know where content is, but ... open the box with the
  crowbar found inside.

* Pre processing of 

* git based approval process so others can sign off / work / see
  betas.

* go dynamic???? this does static sites.  OK, but what if we did
  dynamic sites.  how to do this??? Dynamic always makes for easier
  future proofing



- need a obj for directory as well - complex to keep passing things
- around this will solve issues with the breadcrumbs. like how to know
- what level to pass.  for now I am assuming first string passed in
- bredcrumb is at HTML_ROOT.  THis is a fine assumption.

- split the text from the generator
- make a beter HTML template, so that I can use breadcrumbs
- see about releaseing this. sort of sphinx-nose
  somewhere between sphinx and ruby jekyll



:author: pbrian

==============
ReSt bookmaker
==============

This collection of files is designed to allow you to create a simple
website and/or LaTeX based-book from just templates and docutils
markup (www.docutils.org).

Docutils is a useful (if occassionaly complex) python application that
takes simple text based markup and converts it to an intermediary
parsed tree, then out to LaTeX or HTML etc.  A simple example is

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


I have written an entire site, using this system
(www.itmanagerscookbook.com) making one text file the same as one page
in the website. However the structure of the site is formed from the
structure of the directories I store the original text files in.

So the basics of operation are 

1. Write a few text files in ReSt, with a directory structure.

2. walk through the directories, turning the files into HTML / LaTeX
but keeping the directory structure.

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

This is very similar to Sphinx (www.?) - but sphinx I could not quite
get to suit my needs (I may need to reexamine it) I certainly realised
I was stealing their include file idea after I wrote my own (however
one can either include or exclude files in this one - I found that a
bonus)

Docutils - I happily recommend this - it is fast becoming standard
documentation method for Python.


CSS
---

Jan 09
found, from joel spolsky

http://matthewjamestaylor.com/blog/ultimate-3-column-blog-style-pixels.htm

This looks a very effective solution to a problem I have long had - I
just want to write simple HTML and have CSS take care of looking good
(or in this case OK)




Usage
-----

::

  $ <edit config file>
  $ python mkbook.py --no-pdf


Default is to only look for files called .chp


>>> p = create_html('/root/thebook/thebook/SoHoFromScratch', 'DNS.chp')
>>> p.title
u'Domain name system' 

Now show the page object

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
### NB!!!!
### hacky hack
### I am doing a late import of the config file because the location
### of conf is passed to this file as an arg

from optparse import OptionParser
import os, sys, subprocess
import pprint
from docutils.examples import html_parts


def loopthrudir(full_current_root, dirs, files):
    """This does the meat of the work. 
    Go through all files in a dir, 
    pdf, or htmlise them, and return their meta data (title etc)
   

    * Note on local/full


    I am using a tree strucutre that roots from same arbitrary point
    in a real disk tree.  So the strucutre I care about starts from
    thebook but on disk that is /foo/bar/thebook.  thebook/ is my
    local root, /foo/bar/thebook is my fullroot, but if I delve
    deeper, thebook/chapter1/ is my local_current_root
    
    * Returns

 
    a list of all "pages" in this directory, as page-like objects.

    >>> 1
  

    """
    
    thisdirlist = []
    files = [f for f in files if os.path.splitext(f)[1] in config.valid_exts]


    for f in files:
        print " ", f
        applog("use: %s\n" % os.path.basename(f))
        #decide on source and destimation. src_dir is told to us and is not really "this"
        try:
            thisdirlist.append(lib.rst_to_page(os.path.join(full_current_root, f)))
            ### to make command feel responsive
            print '.',
        except Exception, e:
            raise e

    ### remove files we dont want to publish.  Done after the fact because I want to use page object
    files = [page for page in thisdirlist if lib.publish_this_file(page)]
    applog('ignore: %s\n' % ' '.join([page.src_filename for page in thisdirlist if not lib.publish_this_file(page)]))
    return files



def run_dirs():

    """ Go through the directory holding the .chp files, and run each
        file through the rst generator(s)


    I have three ways of pruning the files / directories I will index
    first two are simple remove svn / git directories from contention.
    The third is depeandt on a dir contianing a file called *no_index*

    Here this dir is then ignored and not parsed - a no index file will cut off not merely one dir but whole branch

    NB - for os.walk you must use direct operators on returned dirs listing - 
    this is an iterator and does not "do" assignment

    """

    ignore_dirs = ['.svn', '.git']
    dir_list = {}
    
    for root, dirs, files in os.walk(config.chapters_dir):         
        # three ways of pruning the 
        ### 
        print root
#        dirs = [d for d in dirs if d.find(".git") == -1]
#        dirs = [d for d in dirs if ".svn" not in d.split("/")]
#        print "-", dirs 
#        print raw_input(root)

        ## if in THIS dir, i have a file called noindex,
        ## then parse files in THIS dir but no sub dirs
        if config.NO_INDEX_SUBDIRS in files: 
            del dirs[:]
            print "not indexing below", root

        if root.find(".git") != -1: continue
        if root.find(".svn") != -1: continue

  
        # do not collect directories with nothing in them
        pages_list = loopthrudir(root, dirs, files)    
        if len(pages_list) > 0:
            dir_list[lib.dir_identity(root)] = pages_list



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
                        'breadcrumbs': lib.list_to_breadtrail(pg.breadcrumbs),
                        'css_theme': config.css_theme
                       }  
            open(dest, 'wb').write(s.encode('utf8'))
        indexhtml = prepare_index(dirlist[dir]) 
        open(os.path.join(os.path.dirname(pg.ondisk_dest), 'index.html'), 'wb').write(indexhtml)
    write_contents(dirlist)
 
def write_contents(fulldirlist):
    ''' '''
    html = ''
#    previousdir = ''
    for dir in  sorted(fulldirlist.keys()):
        singledirlist = fulldirlist[dir]
        s, dirname = get_index_body(singledirlist, toc=True)
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
                        'breadcrumbs': lib.list_to_breadtrail(['contents',]),
                        'css_theme':config.css_theme

                          }

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
   

def get_index_body(singledirlist, toc=False):
    """Given a list of page objects, build an index html page
    This page now has 3 uses

    1. as part of the main TOC
    2. as a stand alone index page for each direcotry
    3. as topic blocks for the fornt page... - ie front page will now use chunks of the toc


    NB I can return "unknown directory" because there are no files in dir.
    I think  it safer not to return anything    
    
    toc - are we calling this for the toc / front page (ie short version) or full in page version?

    """
    
    tmpl = config.maintmpl
    dirname = 'unknown directory'
    s = """<ul> """
    for pg in singledirlist:
        dirname = os.path.dirname(pg.src)
        s += build_contents_link(pg)

    s += '</ul>'


    topic_file = os.path.join(dirname, 'topic.rst')

    if not os.path.isfile(topic_file):
        #not topic file defined, so plain index file please
        return (s, dirname)

    else:
 
        topic_pg = lib.rst_to_page(topic_file)
        if toc:
            html = '<h2 class="subtitle">' + topic_pg.subtitle + "</h2>" + s
            return (html, dirname)
        else:
            html = topic_pg.teaser + s 
            return (html, dirname)    
 




def prepare_index(singledirlist):
    ''' 
    * generate the index page for a chapter directory
    
    takes list of page objects in the dir, returns complete html page to be written to disk

    What I want to do is pull in a new file topic.rst, which is a title, subtitle and body,
    that provides the overview of a topic.   I then list the articles under that topic.
    I need therefore to have a prepare_index body, which is the maintext here, ie not pluggedinto tmpl
    this index body can be reused to put on front page.


    '''
    tmpl = config.maintmpl
    s, dirname = get_index_body(singledirlist)
    html = tmpl % {'maintext':s + "</ul>", 'rhs':config.rhs_text,
                        'title':dirname, 'html_root':config.HTMLROOT,
                  'breadcrumbs': lib.list_to_breadtrail([dirname,]),
                  'css_theme': config.css_theme
                  }
    return html



def set_permissions(username, grpname):
    '''need to alter permissions on the files to be served '''
    #    sudo chown -R nobody:nobody book/
#    import pwd, grp, os
#    print "set permissions", username, grpname
#    uid = pwd.getpwnam(username).pw_uid
#    gid = grp.getgrnam(grpname).gr_gid
#    print "set permissions", username, uid, grpname, gid
#    print config.HTML_DEPLOY_DIR
#    os.chown(config.HTML_DEPLOY_DIR, uid, gid)
#nice but no recursion...
    l = ["chown", "-R", username + ":" + grpname, 
          config.HTML_DEPLOY_DIR]
    print l
    subprocess.check_call(l)

    l = ["chmod", "-R", '0775', 
          config.HTML_DEPLOY_DIR]
    print l
    subprocess.check_call(l)


def main():
    """ """


    ### main loop
    check_environment()
    dir_list = run_dirs()
    write_to_disk(dir_list)
#    TOC XXX
    lib.make_frontpage(config.frontpage_list_articles)
    deploylive()

    set_permissions("www","www")    

def check_chp_dir_arg_valid(chp_dir):
    ''' '''
    return os.path.isdir(chp_dir)


def bootstrap():
    '''There is stuff we do after import, ie import config.  I need to call this  but this whole thing needs configparser'''

    global config
    global chp_dir
    global applog
    global lib

    global  getdestpath
    global  get_html_from_rst
    global  write_index
    global  deploylive
    global  get_tmpl_dict
    global  check_environment
   
    global  dir_identity
    global  rst_to_page
    global  BookMakerError

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


    ### setup config files
    #### All content directories MUST have a folder named this:
    book_config_folder = ".bookmaker"
    #### and a config fole formatted as needed called config.py 
    sys.path.insert(0, os.path.abspath(chp_dir))
    sys.path.insert(0, os.path.abspath(os.path.join(chp_dir, book_config_folder)))
    import config    

    from lib import  publish_this_file, getdestpath, \
                     get_html_from_rst, write_index, deploylive,  \
                     get_tmpl_dict, check_environment, applog, \
                     dir_identity, rst_to_page, BookMakerError
    import lib

    if not check_chp_dir_arg_valid(chp_dir):
        raise BookMakerError("Chapter Directory (%s) is not a dir" % chp_dir)
    else:
        config.setup_chp_dir(chp_dir)

    if opts.ignore_exclude == True:    
        config.IGNORE_EXCLUDE = True



if __name__ == '__main__':





    
    bootstrap()
    main()
