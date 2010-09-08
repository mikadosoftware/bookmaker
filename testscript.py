
import sys, os
content_meta_dir = sys.argv[1:][0]

sys.path.insert(0, os.path.abspath(content_meta_dir))


import lib
import mkbook
import config
chp_dir = '/home/pbrian/mikadosoftware.com/projects/cookbook'
config.setup_chp_dir(chp_dir)
p = lib.rst_to_page(os.path.join(chp_dir, 'SoHoFromScratch/DNS.chp'))

dirlist = mkbook.run_dirs()

