import os.path


### CONSTANTS 
HTMLROOT = "/book"
chapters_dir = '/root/thebook/thebook'
FULLROOTPATH = '/root/thebook'

BINARYPATH = os.path.abspath('./')

HTML_DIR = '/tmp/bookbuild'
HTML_DEPLOY_DIR = "/usr/local/www/data/book"
IMG_DIR = os.path.join(FULLROOTPATH, "img")
CSS_DIR = os.path.join(FULLROOTPATH, "css")




## new config
SOURCE_RST_ROOT = chapters_dir
HTML_BUILD_DIR = os.path.join(HTML_DIR, 'html')
PATH_FROM_DOCROOT = HTMLROOT
DEPLOY_HTML_ROOT = HTML_DEPLOY_DIR


logfilepath = os.path.join(FULLROOTPATH, 'log.log')

###
incl_file_name = '.ppp_include'
IGNORE_EXCLUDE = False         # if true put every file into site.  This is set with argument flag to make simple for me to review site.

latex_dir  = 'simpleITmanager_latex'

####### No longer used - using html_parts
#cmdpath = '/usr/home/pbrian/downloads/docutils-0.5/tools/rst2html.py'
#cmdpath = 'rst2html.py'
#
#rst_options = ['--stylesheet-path=css/thebook.css', 
#               '--initial-header-level=3',
#               '--link-stylesheet']


errors = []


pdflatex_cmds = ['pdflatex', '--output-directory=%s' % latex_dir, '--interaction=nonstopmode']
to_latex_cmds   = ['rst2latex.py']


rhs_text = open('rhs.tmpl').read() % {'HTML_ROOT': HTMLROOT}

