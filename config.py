import os.path


### CONSTANTS 
HTMLROOT = ""
working_dir = os.path.dirname(os.path.abspath(__file__))
FULLROOTPATH = working_dir

BINARYPATH = os.path.abspath('./')

HTML_DIR = '/tmp/bookbuild'
HTML_DEPLOY_DIR = "/usr/local/www/apache22/data/book"


### valid exts for files that are raw test
valid_exts = ['.chp',]


## new config

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
rst2html_overrides = { 'input_encoding': "unicode",
                       'initial_header_level': 2,
                       'styleheet-path':'css/thebook.css',
                       'link-stylesheet':True
                      }

errors = []


pdflatex_cmds = ['pdflatex', '--output-directory=%s' % latex_dir, '--interaction=nonstopmode']
to_latex_cmds   = ['rst2latex.py']

maintmpl = open('main.tmpl').read()
rhs_text = open('rhs.tmpl').read() % {'HTML_ROOT': HTMLROOT}

chapters_dir = None; SOURCE_RST_ROOT = None; IMG_DIR = None; CSS_DIR = None
def setup_chp_dir(chp_dir):
    #This will get replaced by an arg passed to mkbook os.path.join(working_dir, 'thebook') #'/home/pbrian/clone_upstream/thebook/thebook'
    global chapters_dir
    global SOURCE_RST_ROOT
    global IMG_DIR
    global CSS_DIR
    chapters_dir = chp_dir
    SOURCE_RST_ROOT = chapters_dir
    IMG_DIR = os.path.join(chapters_dir, "img")
    CSS_DIR = os.path.join(chapters_dir, "css")
