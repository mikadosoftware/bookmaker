
import sys, os
import mkbook
mkbook.bootstrap()

chp_dir = '/home/pbrian/com.mikadosoftware/cookbook'

import config

import lib




config.setup_chp_dir(chp_dir)
p = lib.rst_to_page(os.path.join(chp_dir, 'SoHoFromScratch/DNS.chp'))

dirlist = mkbook.run_dirs()

singledirlist = dirlist['Attitude']

html = mkbook.prepare_index(singledirlist)

