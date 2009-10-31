#!/usr/local/bin/python
#! -*- coding: utf-8 -*-

"""
pbrian

Library functions to support web site from ReSt creation.

General Description 
------------------- 

I want to write a whole site
using ReSt, making my life easier.  The structure of the site will
remain the same, with just the .rst files being replaced by .html, the
creation of appropriate index.html files.  Images will be held in img/
dir in each directory

I have no idea how to link inbetween in rst...


How it works
------------

config file is set up - firstly it contains the 

SOURCE_RST_ROOT = root folder where rst files can be found
HTML_BUILD_DIR = temp folder to build HTML files
PATH_FROM_DOCROOT = working ala apache, what is path from the server 
 documentroot to the final deployed HTML files.  Expected to be / 
DEPLOY_HTML_ROOT = the docroot
IMG_DIR = location of source IMG files
CSS_DIR = location of source CSS files


What I want it to do:

- loop thru the all directories, building a site structure, keyed on
dirpathfromroot, keeping html as objects converted from rst
(keep in memory??)

- store that strucutre, write out the index pages and them template
  everything

BUILD_PAGES
BUILD_INDEXES
WRITE_TO_DISK


TODO:
- really passing around this dict then playing with it is poor - use an object.
- some tests!!!


NOTES
#parts = /usr/local/lib/python2.5/site-packages/docutils-0.5-py2.5.egg/docutils
#>>> from docutils import core
#>>> help(core.publish_parts)


>>> ux = u"Hello\\n-----\\n there sailor"
>>> p = get_html_from_rst(ux)
>>> pp = page(**p)
>>> print pp.title 
Hello





"""

import os, sys, subprocess
import pprint
from docutils.examples import html_parts
from docutils import core
import config
import ConfigParser
import shutil


########### BUILD PAGES FUNCTIONS
def first_sentences(txt, ct=5):
    """
    Given some text return first 5 sentences 
    This is a problem.  If there is a call out in the first sentences, 
    I get ugly warning signs...
    However, cutting off HTML is worse and less predictatble

    .. returns: string representing rst for first few sentences of a chapter

    >>> first_sentences("hello.  there. Sailor. How. Are. You. Big. Spender.")
    'hello.  there. Sailor. How. Are. '
    

    """
    split_on = ". "
    sentences = txt.split(split_on)
    
    final_txt = ". ".join(sentences[:ct])
    ### If I get a call out I just disgard it. Not too safe.
    delete_me = ['[#]_', '[*]_']
    for d in delete_me:
        final_txt = final_txt.replace(d, "")  
    return  final_txt + split_on



def make_frontpage(chosen_articles):
    """ Put on the front page 3 articles that reflect the latest on the site """

    pages = []
    for article in chosen_articles:
        try:
            articlepath = os.path.join(config.chapters_dir, article)
            page = rst_to_page(articlepath)
            pages.append(page) 
        except Exception, e:
            raise e 

    destination = os.path.join(config.HTML_BUILD_DIR, "index.html")

    fullstr = ''
    for p in pages:
        fullstr += p.teaser
        fullstr += '<a href="%s">more...</a>' % os.path.join(p.dest_url) 
        fullstr += '<hr/>'

    #write out tmpl to destination - could seperate out here. 
    tmpl_txt = open("main.tmpl").read()                
    
    d = get_tmpl_dict()
    d["title"] = 'Frontpage'
    d["maintext"] =  fullstr
    d["rhs"] = config.rhs_text
    d['subtitle'] = 'Frontpage subtitle'
    d['breadcrumbs'] = 'frontispiece'

    outstr = tmpl_txt % d
    fo = open(destination, 'w')
    fo.write(outstr)
    fo.close()



def rst_to_page(articlepath):
    """Convert rst file to page object

    returns
    -------
    an obj  representing the returns from rst conversion and 
    src, dest, errors in conversion

    teasr = first few sentences converted to HTML

    >>> p = rst_to_page(os.path.join('/root/thebook/thebook/SoHoFromScratch', 'DNS.chp'))
    >>> p.title
    u'Domain name system'

    """
    source_path = articlepath #os.path.join(full_current_root, file)
    try:
        #i should save all my files as utf8 anyway
        rst_txt = unicode(open(source_path).read(),'utf8')
        ## Grab the first few sentences, and make a taster 
        rst_first_sentences = first_sentences(rst_txt) 
        first_sentences_info = get_html_from_rst(rst_first_sentences)
        page_info = get_html_from_rst(rst_txt) 
 
    #problems getting rst to html - if it is severe, well do not publish it!!   
    except Exception, e:
        raise e

        #error converting page - get out. let others handle that

    page_info["src"] = source_path
    page_info['teaser'] = first_sentences_info['html_body']
    #convert to an object 
    return page(**page_info)



def get_html_from_rst(uStr):
    """ 

    returns
    -------
    A dict of data about the page::

      ['subtitle', 'version', 'encoding', 'html_prolog', 'header', 'meta', 'html_title', 'title', 'stylesheet', 'html_subtitle', 'html_body', 'body', 'head', 'body_suffix', 'fragment', 'docinfo', 'html_head', 'head_prefix', 'body_prefix', 'footer', 'body_pre_docinfo', 'whole']

    examples,py in docutils.core is used    


    I think a decent object might be better here - a rst2htmlpage object
    
    """
    try:
        overrides = {'input_encoding': "unicode",
                 'initial_header_level': 2}
        p = core.publish_parts(uStr, writer_name="html", 
                               settings_overrides=overrides)
        return p

    except Exception, e:
        applog("FAILED RST CONVERSION: %s" % str(e))
        raise e


def publish_this_file(page):
    """given a file object, decide if we want to publish it
    
    All files to publish must end .chp

    I have created a file .ppp_include 
    which looks like 

exclude = ['ibmadverts.chp',]


    if a file is listed in exclude we do not publish
    if the .ppp_include file is missing include all
    XXX - todo - raise a warning if filelisted but not in dir
 
    """

    #must end .chp
    junk, ext = os.path.splitext(page.src)
    if ext in config.valid_exts: 
        valid_flag = True
    else:
        valid_flag = False
        #break on any failure
        return valid_flag


    root, file = os.path.split(page.src)
    #test the user defined include/exclude
    include_file = os.path.join(page.src_dir, config.incl_file_name) 

    #does it exist - if not we publish all files
    if not os.path.isfile(include_file):
        return True #if no include file print anyway

    ### An include file exists.

    ### DO we want to ignore exclude files (ie draft)
    if config.IGNORE_EXCLUDE == True:
        print '---->>>', page.src, config.IGNORE_EXCLUDE
        return True


    c = ConfigParser.ConfigParser()
    c.read(include_file)

    #[('include', 'ibmadverts.chp pov.chp')] -> {include:'ibmadverts.chp, ...
    items = dict(c.items('include'))

    try:
        files_to_include = items["include"].split() #assumes no spaces in filename        
    except Exception, e:
       files_to_include = []

    #logic for publishing
    if os.path.basename(page.src) in files_to_include : 
        #this file is in include, so return True, we want to publish
        return True
    else:
        valid_flag = False
   
    # if not include, no publish. 
    return valid_flag


def getdestpath(html_pdf, local_full, src_full_path):
    """Given the root of where the walk is, 
       decide what the dest html path is 

     so if we are looking at /foo/bar as holding all the rst files
     and /foo/bar/MyImportantSection as a sub dir
     and we want to put the html stage into /wibble/wobble
     we want to see a dest of /wibble/wobble and /wibble/wobble/MyImptSubDir
    
     >>> x = config.HTML_BUILD_DIR
     >>> getdestpath('html', 'full', '/foo/bar/subdir')
     '/tmp/bookbuild/html/foo/bar/subdir'
     >>> getdestpath('html', 'local', '/root/thebook/foo/bar/subdir')
     'foo/bar/subdir'
     >>> x
     '/tmp/bookbuild/html'

    """

    local_src_path = dir_identity(src_full_path)

    if local_full == 'full':
        dst = os.path.join(config.HTML_BUILD_DIR, local_src_path)
    else:
        dst = local_src_path
    return dst


def get_tmpl_dict():
    """ returns a dictionary that holds appropriate defaults for the
    main.tmpl
    """

    d = {"html_root":config.HTMLROOT,
         "HTML_BUILD_DIR":config.HTML_BUILD_DIR, 
         "title":"",
         "maintext":'',
         "rhs":''}

    return d

    

########### BUILD INDEXES
def make_site_index():
    """
    I Want a different index page
   
    """
    pass

####
def list_to_breadtrail(breadlist):
    '''convert a list of strings into a formatted breadcrumb trail.

    Assumes that a list passed in starts from HTMLROOT'''
    url = '''<a href="%s/%s" class="breadcrumb_url">%s</a>'''
    s = ' / '
    for crumb in breadlist:
        idx = breadlist.index(crumb)
        path = '/'.join(breadlist[:idx+1])
        s += url % (config.HTMLROOT, path, crumb)

    return ''

########### WRITE TO DISK FUNCTIONS

def write_html_to_dest():
    """ """

    #write out tmpl to destination
    tmpl_txt = open("main.tmpl").read()                

    d = get_tmpl_dict()
    d["title"] = page_info['title']
    d["maintext"] =  page_info['html_body']
    d["rhs"] = config.rhs_text
    d['subtitle'] = page_info['subtitle']

    outstr = tmpl_txt % d
    fo = open(destination, 'w')
    fo.write(outstr)
    fo.close()


def write_indexpage_to_disk(contents, section_path, isMainContents=False):
    """
    cleaning up write_index, use this to actually write to disk

    section_path is the bit of this folder after chapters_dir,
    so for example /root/thebook/thebook/SoHoFromScratch/foo > SoHoFromScratch/foo
    

    isMainContents - I want to have the main content section written
    to a diff location

    """


    ### now we have a formatted page of contents, put it in the main site tmpl
    d = get_tmpl_dict()
    d["title"] = "Index for %s" % os.path.basename(section_path)
    d["maintext"] = contents
    d["rhs"] = config.rhs_text
    d['breadcrumbs'] = list_to_breadtrail(['contents',])
    tmpl_txt = open("main.tmpl").read()



    ### write put page    
    
    dest = os.path.join(os.path.join(config.HTML_BUILD_DIR, section_path), 'contents.html')
#    if isMainContents:
#        dest = os.path.join(os.path.join(config.HTML_BUILD_DIR, section_path), 'contents.html')

    print "===*** writing %s to %s\n" % (section_path, dest)
    fo = open(dest,'wb')
    fo.write(tmpl_txt % d)
    fo.close()
    


def write_index(index_list):
    """ 

    receive this
    {'intro': [ {...dict holding details on a page...}

    I want an index.html in *each* directory, and maybe a big one in root dir. Not sure.
    I think better to keep whats going on as the intro for now, maybe later do a 
    *new* page. 

    keys() looks like 
['/root/thebook/thebook/Attitude',
 '/root/thebook/thebook/SoHoFromScratch',
 '/root/thebook/thebook/Introduction',
 '/root/thebook/thebook',
 '/root/thebook/thebook/OSS',
 '/root/thebook/thebook/OtherPoV']

nb config.chapters_dir = '/root/thebook/thebook'

    
    """   

    all_contents = ''' '''              #the whole site index
    this_section_contents = ''' '''     #index for just one section/directory

    ### go thru the dict of sections, where each section is a list of dict of page data
    ### {'introduction section':[{<pageinfo>},...
 
    for section in sorted(index_list.keys()):
        this_section_contents = ''' '''
        this_section_path = section.replace(config.chapters_dir, '') 
        if  this_section_path.find("/") == 0: 
            this_section_path = this_section_path[1:]


        if len(index_list[section]) == 0: continue #no pages in this "folder"

        this_section_contents += '<h3>%s</h3><ul>' % os.path.basename(section)

        for page_info in index_list[section]:
            if page_info["title"] == "": 
                page_title = os.path.splitext(os.path.basename(page_info['src']))[0]
            else:
                page_title = page_info["title"] 

            ###  this is a bit confusing - I am planning to write an index page in each dir so only need basename?
            dest_href = page_info['dest'].replace(config.HTML_BUILD_DIR, config.HTMLROOT)


            print "*** writing this src, %s to this html page %s then indexing as %s\n\n" % (page_info['src'],  page_info['dest'], dest_href)
            
            if page_info["subtitle"] == '':
                subtitle = ''
            else:
                subtitle = "(" + page_info["subtitle"] + ")"
	    this_section_contents += '''<li>
                                        <a href="%s">%s</a>
                                        <span class="content_subtitle">%s</span>
                                      </li> \n''' % (dest_href, page_title, subtitle)
             
        this_section_contents += '</ul>'
        write_indexpage_to_disk(this_section_contents, this_section_path)
        all_contents += this_section_contents

    write_indexpage_to_disk(all_contents, '', True)


def deploylive():
    """move from where html files create to the DocumentRoot """    

    import shutil, glob
 
    print "start deploy from %s to %s." % (config.HTML_BUILD_DIR, config.HTML_DEPLOY_DIR)

    shutil.rmtree(config.HTML_DEPLOY_DIR)

    shutil.copytree(config.HTML_BUILD_DIR, config.HTML_DEPLOY_DIR)

    subprocess.check_call(['cp','-r','css', config.HTML_DEPLOY_DIR ])
    subprocess.check_call(['cp','-r','img', config.HTML_DEPLOY_DIR ])

    #shutil.copy(os.path.join(config.HTML_DEPLOY_DIR, "index.html"), 
    #            os.path.join(config.HTML_DEPLOY_DIR, "contents.html")) 

    print "deploy done"

def check_environment():
    """Clean the file system so html etc can be produced.

    We remove the staging html dir, and the final deploy dir.
    We then repopulate the media (css, imgs) into the staging dir,
    ready for the html to be made

    XXX - it might be simpler to have img dir in each level of chapter dir, 
    """

    for expendable_dir in (config.HTML_BUILD_DIR, config.HTML_DEPLOY_DIR): 

        if os.path.isdir(expendable_dir):
            shutil.rmtree(expendable_dir)
        #os.mkdir(expendable_dir)


    for dir in (config.HTML_DIR, config.HTML_DEPLOY_DIR):
        if not os.path.isdir(dir):
             os.makedirs(dir)

    #kind of assumes its there ...
    shutil.rmtree(os.path.join(config.chapters_dir, "img"))
    shutil.copytree(config.IMG_DIR, os.path.join(config.chapters_dir, "img"))
    ### make destination OK
    shutil.copytree(config.IMG_DIR, os.path.join(config.HTML_BUILD_DIR, "img"))
    shutil.copytree(config.CSS_DIR, os.path.join(config.HTML_BUILD_DIR, "css"))
    

####### Misc
def dir_identity(fullpath):
    """
    We have a directory structure, from ROOT onwards.  I do not care
    where on the disk root starts, so this removes the root prefix to
    give me a cleaner directory identity

    LOCALROOTPATH = from the structure root
    FULLROOTPATH = from the real root

    BINARYROOT = location of binaries

    returns: path as string
      
    # doctest
    # I think that I want to have my paths rooted such that the top level dirs (soho etc) are at the top
    # so I use chapters_dir as the mask

    """
    #eg I have /root/thebook/thebook/SoHo/dns.chp, I get back thebook/SoHo/dns.chp
    local_src_path = fullpath.replace(config.chapters_dir, '')
    if local_src_path.find("/") == 0:
        local_src_path = local_src_path[1:]

    return local_src_path

def applog(msg):
    """
    really dumb standing for proper logging 
    .. returns:: Nothing

    Nothing to test really.

    """

    logfileo = open(config.logfilepath, "ab")
    logfileo.write(msg)
    logfileo.close()

class page(object):
    """represents what we know about a (html) page

    really this is a convenient way to store metadata about a file
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def get_dest_to_write_to(self):
        """given self knowledge return the location to write out to

           local_current_root = dir_identity(full_current_root)
           local_source = os.path.join(local_current_root, file)

        

        """
        destfile = dir_identity(self.src).replace(".chp", ".html")
        return os.path.join(config.HTML_BUILD_DIR, destfile)


    def __repr__(self):
        return "rst_page: %s" % self.title

    @property
    def breadcrumbs(self):
        """return a list of stages from local root to local current root """
        local_path = dir_identity(self.src)
        breadcrumbs = os.path.split(local_path)[0].split("/")
        breadcrumbs = [b for b in breadcrumbs if b != '']
        #replace the last breadcrumb with page title
        breadcrumbs.append(self.title) 

        return breadcrumbs

    @property
    def dest_url(self):
        '''Return relative url that is this page '''
        return self.ondisk_dest.replace(config.HTML_BUILD_DIR, config.HTMLROOT)
        
    @property
    def ondisk_dest(self):
        return self.get_dest_to_write_to()
     
    @property
    def src_filename(self):
        return os.path.basename(self.src)

    @property
    def src_dir(self):
        '''Directory that contains the source file for this page'''
        return os.path.dirname(self.src)


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
