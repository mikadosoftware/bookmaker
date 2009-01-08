import os, sys, subprocess
import pprint
from docutils.examples import html_parts
import config


    
def write_index(index_list, html_dir, rhs_text):
    """ 

    receive this
    {'intro': [ [<filepath>, <filetitle>], ...], }
 

    XXX This needs rethinking.
    """   
    print "+++++++++++++++++++++"
    pprint.pprint(index_list)
    print "+++++++++++++++++++++"

    contents = ''' '''
   
    for i in sorted(index_list.keys()):
        contents += '</ol><h3>%s</h3><ol>' % i.replace('simpleitmanager/thebook/','')
        for (ii, page_title) in index_list[i]:
            if not page_title: page_title = 'xxx'
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
    fo = open(os.path.join(html_dir,'contents.html'),'wb')
    fo.write(tmpl_txt % d)
    fo.close()

def deploylive():
    print '== starting deploy'
    
    import shutil, glob
    shutil.rmtree(config.HTML_DEPLOY_DIR)
    shutil.copytree(os.path.join(config.HTML_DIR, config.chapters_dir), config.HTML_DEPLOY_DIR)
    for file in glob.glob(config.HTML_DIR + "/*.html"):
        print file
        shutil.copy(file, config.HTML_DEPLOY_DIR)


    subprocess.check_call(['cp','-r','css', config.HTML_DEPLOY_DIR ])
    subprocess.check_call(['cp','-r','img', config.HTML_DEPLOY_DIR ])


def get_html_from_rst(uStr):
    ''' THis uses ReSt to get some HTML from just text in text area. It is a bit funny - I force                            
    the title and body to be joined before it beocmes UStr, then I return title and body seperate.                          
    Seems to work as long as css is ok.'''
    try:
        p = html_parts(uStr.decode('latin1'), initial_header_level=2)
        return (p['html_title'], p['body'])

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



def publish_this_file(f):
    """given a file basename, decide if we want to publish it
    
    At the moment the only criteria is ends in .chp, but clearly can extend 
    so define which artilces to publish (or not)"""
    #must end .chp
    junk, ext = os.path.splitext(f)
    if ext in ('.chp',): 
        return True
    else:
        return False



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

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
