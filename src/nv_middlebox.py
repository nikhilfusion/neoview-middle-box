#! /usr/bin/python3
# -*- coding: utf8 -*-
# The middlebox software for remote camera management and relay streaming.
#
__author__ = "Sugesh Chandran"
__copyright__ = "Copyright (C) The neoview team."
__license__ = "GNU Lesser General Public License"
__version__ = "1.0"

import platform
import sys
import os

curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(curr_dir, os.pardir)))

from src.nv_logger import nv_logger,default_nv_log_handler
from src.nvdb.nvdb_manager import db_mgr_obj
from src.nv_midbox_websock.nv_midbox_ws import nv_midbox_ws
# Import all the configuration values
from src.nv_midbox_conf import nv_midbox_conf

class nv_middlebox():
    def __init__(self):
        self.nv_log_handler = nv_logger(self.__class__.__name__).get_logger()
        self.nv_cli_mgr = None # Cli thread to read user inputs.

    def init_db(self):
        self.nv_log_handler.info("Initilizing the middlebox DB")
        db_mgr_obj.setup_session()
        db_mgr_obj.create_system_record()

    def run(self):
        try:
            sys.tracebacklimit=0
            self.nv_log_handler.info("starting the middlebox")
            self.init_db()
            self.nv_websock = nv_midbox_ws()
            self.nv_websock.start()
            self.nv_conf = nv_midbox_conf()
            self.nv_conf.do_midbox_conf()
        except KeyboardInterrupt:
            if self.nv_conf:
                self.nv_conf.exit_all_threads()

if __name__ == "__main__":
    # if platform.system() != 'Linux':
    #     default_nv_log_handler.error("Neoview Middlebox works only on Linux " +
    #                                  "platform")
    #     exit(1)
    nv_mid_obj = nv_middlebox()
    try:
        nv_mid_obj.run()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        default_nv_log_handler.error("Exiting with exception %s" %str(e))
