'''
Created on 17/12/2013

@author: tmardesic
'''

import os
import subprocess
from subprocess import (PIPE, Popen)
import time
import traceback
import threading
from threading import Lock
import textwrap
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from multiprocessing import Queue


class Log():
    
    def __init__(self):
        """ Constructor """
        pass
 
    # --- Para estas funciones LOG ---
    def _log(self,level,transaction,msg):
        """ Inserta log a fifo
        level : VACIO , E, W
        transaction: --- , <-- , --> .....
        """
        msg = msg if isinstance(msg, str)  else str(msg)
        stamp = str(datetime.now()).split(".")[0]
        print(stamp+" ["+level+"] ["+transaction+"] : "+msg)
        
    def I(self, transaction, msg):
        self._log(" ",transaction,msg)        

    def W(self, transaction, msg):
        self._log("W",transaction,msg)

    def E(self, transaction, msg):
        self._log("E",transaction,msg)


   