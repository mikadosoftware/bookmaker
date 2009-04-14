#!/usr/local/bin/python
#! -*- coding: utf-8 -*-

"""
pbrian

Library functions to support web site from ReSt creation.


"""

import os, sys, subprocess
import pprint
from docutils.examples import html_parts
from docutils import core
import config
import ConfigParser
import shutil


#parts = /usr/local/lib/python2.5/site-packages/docutils-0.5-py2.5.egg/docutils
#>>> from docutils import core
#>>> help(core.publish_parts)

    
def write_indexpage_to_disk(contents, section_path, isMainContents=False):
    '''cleaning up write_index, use this to actually write to disk

    section_path is the bit of this folder after chapters_dir,
    so for example '/root/thebook/thebook/SoHoFromScratch/foo' > 'SoHoFromScratch/foo'
    

    isMainContents - I want to have the main content section written to a diff location
    ''' 

    ### now we have a formatted page of contents, put it in the main site tmpl
    d = get_tmpl_dict()
    d["title"] = "Index for %s" % os.path.basename(section_path)
    d["maintext"] = contents
    d["rhs"] = config.rhs_text

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
            
	    this_section_contents += '''<li> <a href="%s">%s</a>
                           <span class="subtitle">(%s)</span>
                           </li> \n''' % (dest_href, page_title, page_info["subtitle"])
             
        this_section_contents += '</ul>'
        write_indexpage_to_disk(this_section_contents, this_section_path)
        all_contents += this_section_contents

    write_indexpage_to_disk(all_contents, '', True)


def deploylive():
    """move from where html files create to the DocumentRoot """    
    import shutil, glob
 
    print "start deploy from %s to %s." % (config.HTML_BUILD_DIR, config.HTML_DEPLOY_DIR)

    #shutil.rmtree(config.HTML_DEPLOY_DIR)

    shutil.copytree(config.HTML_BUILD_DIR, config.HTML_DEPLOY_DIR)

    subprocess.check_call(['cp','-r','css', config.HTML_DEPLOY_DIR ])
    subprocess.check_call(['cp','-r','img', config.HTML_DEPLOY_DIR ])

    #shutil.copy(os.path.join(config.HTML_DEPLOY_DIR, "index.html"), 
    #            os.path.join(config.HTML_DEPLOY_DIR, "contents.html")) 


    print "deploy done"


def make_site_index():
    """I Want a different index page
   
     """
    pass



def get_html_from_rst(uStr, src=None):
    ''' THis uses ReSt to get some HTML from just text in text area. It is a bit funny - I force                            
    the title and body to be joined before it beocmes UStr, then I return title and body seperate.                          
    Seems to work as long as css is ok.

    returns
    -------
    A dict of data about the page::

      ['subtitle', 'version', 'encoding', 'html_prolog', 'header', 'meta', 'html_title', 'title', 'stylesheet', 'html_subtitle', 'html_body', 'body', 'head', 'body_suffix', 'fragment', 'docinfo', 'html_head', 'head_prefix', 'body_prefix', 'footer', 'body_pre_docinfo', 'whole']

    examples,py in docutils.core is used    


    '''


    try:
        overrides = {'input_encoding': "unicode",
                 'initial_header_level': 2}
        p = core.publish_parts(uStr, writer_name="html", settings_overrides=overrides)
        p['source']=src
        return p

    except Exception, e:
        print 'fail', e
        return 'rst2html failed: %s' % str(e)




def getdirpath(html_pdf, root):
    '''Given the root of where the walk is, 
       decide what the dest html path is 

     so if we are looking at /foo/bar as holding all the rst files
     and /foo/bar/MyImportantSection as a sub dir
     and we want to put the html stage into /wibble/wobble
     we want to see a dest of /wibble/wobble and /wibble/wobble/MyImptSubDir
     '''
    

    if html_pdf == 'html':
        
        path_from_docroot = root.replace(config.chapters_dir, '')
        if path_from_docroot.find("/") == 0:
            path_from_docroot = path_from_docroot[1:]
        dst = os.path.join(config.HTML_BUILD_DIR, path_from_docroot)
        return dst
    else:
        return os.path.join(config.latex_dir, root)


def get_tmpl_dict():
    """ returns a dictionary that holds appropriate defaults for the main.tmpl"""
    d = {"html_root":config.HTMLROOT,
         "HTML_BUILD_DIR":config.HTML_BUILD_DIR, 
         "title":"",
         "maintext":'',
         "rhs":''}

    return d



def publish_this_file(root, f):
    """given a file basename, decide if we want to publish it
    
    At the moment the only criteria is ends in .chp, but clearly can extend 
    so define which artilces to publish (or not)

    I have created a file .ppp_include 
    which looks like 

include = ['ibmadverts.chp',]
exclude = []

    if a file is listed in include we include it, if it is in exclude we do not
    if the .ppp_include file is missing include all
    XXX - todo - raise a warning if filelisted but not in dir
 
    """

    #must end .chp
    junk, ext = os.path.splitext(f)
    if ext in ('.chp',): 
        valid_flag = True
    else:
        valid_flag = False
        #break on any failure
        return valid_flag



    #test the user defined include/exclude
    include_file = os.path.join(root, config.incl_file_name) 

    #does it exist - if not we publish all files
    if not os.path.isfile(include_file):
        return True #if no include file print anyway

    ### An include file exists.

    c = ConfigParser.ConfigParser()
    c.read(include_file)

    #[('include', 'ibmadverts.chp pov.chp')] -> {include:'ibmadverts.chp, ...
    items = dict(c.items('exclude'))

    try:
        files_to_exclude = items["exclude"].split() #assumes no spaces in filename        
    except Exception, e:
       files_to_exclude = []


    #logic for publishing
    if f in files_to_exclude : 
        valid_flag = False
        print "-- %s to be excluded." % os.path.basename(f) 
        #succeed once
        return valid_flag 
    else:
        valid_flag = True
   
    # if not excluded, publish. 
    return valid_flag


def create_pdf(source, ltx_source, errors):
    """given source file create pdfs  

    2 steps - take rst and make latex, then take latex and make pdf
    """

    pdflatex_cmds = ['pdflatex', '--quiet', '--output-directory=%s' % latex_dir, '--interaction=nonstopmode']
    to_latex_cmds   = ['rst2latex.py']


    try: 
        to_latex_cmds.extend([source, ltx_source]) #src, dest  
        subprocess.check_call(to_latex_cmds)

        pdflatex_cmds.append(ltx_source)
        subprocess.check_call(pdflatex_cmds)

    except Exception, e:
        errors.append(e)

    abs_latex_dir = os.path.abspath(latex_dir)
    kill_pdf_odds(abs_latex_dir)


def kill_pdf_odds(abs_latex_dir):
    """given a file killoff any temp latex pdf files

    log, out, ltx """
    files = os.listdir(abs_latex_dir)

    for f in files:
        j, ext = os.path.splitext(f)
        if ext in (".log", ".aux", ".out"): 
            os.remove(os.path.join(abs_latex_dir, f))

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

    os.mkdir(config.HTML_BUILD_DIR)
    #kind of assumes its there ...
    shutil.rmtree(os.path.join(config.chapters_dir, "img"))
    shutil.copytree(config.IMG_DIR, os.path.join(config.chapters_dir, "img"))
    ### make destination OK
    shutil.copytree(config.IMG_DIR, os.path.join(config.HTML_BUILD_DIR, "img"))
    shutil.copytree(config.CSS_DIR, os.path.join(config.HTML_BUILD_DIR, "css"))
    

class page(object):
    """represents what we know about a (html) page

    really this is a convenient way to store metadata about a file
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)




def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
