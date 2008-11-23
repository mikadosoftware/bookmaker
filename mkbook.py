#!/usr/local/bin/python
#

'''
:author: pbrian
aim
---
To build the book into a nice format - initially just use 
rst2html but can get more complex
check_call(["ls", "-l"])

The concept - look at a directory. It should be full of other directories and 
.chp files (text, called chp for chapter)

'''

import os, sys, subprocess
import pprint


### CONSTANTS 
chapters_dir = 'thebook'
html_dir = 'simpleitmanager'

cmdpath = '/usr/home/pbrian/downloads/docutils-0.5/tools/rst2html.py'
cmdpath = 'rst2html.py'
options = ['--stylesheet-path=css/thebook.css',
          '--link-stylesheet']
errors = []

index_list ={} 


###main loop
def main():

    for root, dirs, files in os.walk(chapters_dir):
        if root.find('.svn') != -1: 
            continue
        else:
            print root, dirs, files
            loopthrudir(root, dirs, files )    
    write_index()

def gethtmldirpath(root):
    '''given the root of where the walk is, decide what the html path is '''
    return os.path.join(html_dir, root)


def loopthrudir(root, dirs, files):
    
    thisdirlist = []
    thishtmldir = gethtmldirpath(root) 
    thisdir     = root

    try:
        os.mkdir(thishtmldir)
    except:
        pass

    for f in files:
        #must end .chp
        junk,ext = os.path.splitext(f)
        if ext not in ('.chp',): continue

        source = os.path.join(thisdir, f)
        newhtml = f.replace('.chp','.html')
        destination = os.path.join(thishtmldir, newhtml)
        thisdirlist.append(destination)


        #build subprocess command
        cmds = [cmdpath]
        cmds.extend(options)
        cmds.extend([source, destination])


        try:
            subprocess.check_call(cmds)
        except Exception, e:
            errors.append(e)

    index_list[thishtmldir] = thisdirlist
   
def write_index():
   
    fo = open(os.path.join(html_dir,'index.html'),'wb')
    fo.write('<html><body><ol>')


       
    for i in sorted(index_list.keys()):
        fo.write('</ol><h3>%s</h3><ol>' % i.replace('simpleitmanager/thebook/',''))
        for ii in index_list[i]:
            ii = ii.replace(html_dir + '/', '')      #trying to put index.html one level down from mkbook.py 
	    fo.write('<li> <a href="%s">%s</a></li> \n' % (ii,
                                                 os.path.basename(ii).replace('.html','')))
    fo.write('</ol></body></html>')
    fo.close()

    print 'Total errors: %s' % len(errors)
    pprint.pprint(errors)

def deploylive():
    print '== starting deploy'
    subprocess.check_call(['cp','-r',html_dir, '/usr/local/www/data/'])
    subprocess.check_call(['cp','-r','css','/usr/local/www/data/'])

if __name__ == '__main__':
    main()
    deploylive()

