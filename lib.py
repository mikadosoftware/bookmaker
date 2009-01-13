import os, sys, subprocess
import pprint
from docutils.examples import html_parts
import config
import ConfigParser
import shutil


#parts = /usr/local/lib/python2.5/site-packages/docutils-0.5-py2.5.egg/docutils
#>>> from docutils import core
#>>> help(core.publish_parts)

    
def write_index(index_list, html_dir, rhs_text):
    """ 

    receive this
    {'intro': [ [<filepath>, <filetitle>], ...], }
 

    XXX This needs rethinking.
    """   

    contents = ''' '''
   
    for i in sorted(index_list.keys()):
        if len(index_list[i]) == 0: continue #no pages in this "folder"

        contents += '</ol><h3>%s</h3><ol>' % i.replace('simpleitmanager/thebook/','')
        for (ii, page_title) in index_list[i]:
            if not page_title: 
                page_title = os.path.splitext(os.path.basename(ii))[0]

            ii = ii.replace(html_dir + '/thebook/', '')      #trying to put index.html one level down from mkbook.py 
	    contents += '<li> <a href="%s">%s</a></li> \n' % (ii, page_title)

    contents += '</ol>'

    ### now we have a formatted page of contents, put it in the main site tmpl
    d = get_tmpl_dict()
    d["title"] = page_title
    d["maintext"] = contents
    d["rhs"] = rhs_text
    

    tmpl_txt = open("main.tmpl").read()

    ### write put page    
    fo = open(os.path.join(html_dir,'index.html'),'wb')
    fo.write(tmpl_txt % d)
    fo.close()

def deploylive():
    """move from where html files create to the DocumentRoot """    
    import shutil, glob
 
    print "start deploy from %s to %s." % (config.HTML_DIR, config.HTML_DEPLOY_DIR)

    shutil.rmtree(config.HTML_DEPLOY_DIR)
    shutil.copytree(os.path.join(config.HTML_DIR, config.chapters_dir), config.HTML_DEPLOY_DIR)
    for file in glob.glob(config.HTML_DIR + "/*.html"):
         shutil.copy(file, config.HTML_DEPLOY_DIR)
         print os.path.basename(file),   


    subprocess.check_call(['cp','-r','css', config.HTML_DEPLOY_DIR ])
    subprocess.check_call(['cp','-r','img', config.HTML_DEPLOY_DIR ])
    print "deploy done"

def get_html_from_rst(uStr):
    ''' THis uses ReSt to get some HTML from just text in text area. It is a bit funny - I force                            
    the title and body to be joined before it beocmes UStr, then I return title and body seperate.                          
    Seems to work as long as css is ok.
    '''

    try:
        p = html_parts(uStr.decode('latin1'), initial_header_level=2)
        return (p['html_title'], p['body'], p['subtitle'])

    except Exception, e:
        return 'rst2html failed: %s' % str(e)



def strip_html(htmlstr):
    """ given string remove any html tags, leaving plain text
    
    >>> strip_html("<li>hello</li>")
    'hello'
 
    """
    import re
    r = re.compile("\<.*?\>") #non greedy match between <>
    matches = r.findall(htmlstr)
    #print "given: %s" % htmlstr,

    for i in matches:
        htmlstr = htmlstr.replace(i, '')
    #print " %s" % htmlstr
    return htmlstr


def getdirpath(html_pdf, root, html_dir, latex_dir):
    '''given the root of where the walk is, decide what the html path is '''
    if html_pdf == 'html':
        return os.path.join(html_dir, root)
    else:
        return os.path.join(latex_dir, root)


def get_tmpl_dict():
    """ returns a dictionary that holds appropriate defaults for the main.tmpl"""
    d = {"html_root":config.HTMLROOT,
         "HTML_DIR":config.HTML_DIR, 
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
    """THe variaous file locations should still exits """
    shutil.rmtree(config.HTML_DIR)
    if not os.path.isdir(config.HTML_DIR):
        os.mkdir(config.HTML_DIR)
    


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
