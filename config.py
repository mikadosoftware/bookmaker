import os.path

HTMLROOT = "/book"


### CONSTANTS 
chapters_dir = '/root/thebook/thebook'
HTML_DIR = '/tmp/bookbuild'
HTML_BUILD_DIR = HTML_DIR
HTML_DEPLOY_DIR = "/usr/local/www/data/book"
IMG_DIR = os.path.join("/root/thebook", "img")
CSS_DIR = os.path.join("/root/thebook", "css")

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

