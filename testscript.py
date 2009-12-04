

import lib
import mkbook
import config
chp_dir = '/home/pbrian/downloads/thebook/'
config.setup_chp_dir(chp_dir)
p = lib.rst_to_page('/home/pbrian/downloads/thebook/SoHoFromScratch/DNS.chp')

dirlist = mkbook.run_dirs()

