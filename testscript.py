
import sys, os

chp_dir = '/home/pbrian/com.mikadosoftware/cookbook'
sys.path.insert(0, os.path.join(os.path.abspath(chp_dir), '.bookmaker'))
import config

import lib
import mkbook



config.setup_chp_dir(chp_dir)
p = lib.rst_to_page(os.path.join(chp_dir, 'SoHoFromScratch/DNS.chp'))

dirlist = mkbook.run_dirs()

