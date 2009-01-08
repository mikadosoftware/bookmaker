
HTMLROOT = "/root/foo"


### CONSTANTS 
chapters_dir = 'thebook'
HTML_DIR = 'simpleitmanager'
HTML_DEPLOY_DIR = "/root/foo/"
IMG_DIR = "img"




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

index_list ={} 
rhs_text = open('rhs.tmpl').read()
