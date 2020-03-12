
#---standard library---
import re
import datetime
import sys,os
import json
from time import sleep
from datetime import datetime, time,timedelta
from datetime import date, timedelta
import random
sys.path.append('/usr/local/lib/python3.5/dist-packages')
sys.path.append(os.path.abspath(os.path.join('./scripts')))

#---Third party library---
import pandas as pd
import pymysql.cursors
from termcolor import colored
import requests
from configparser import ConfigParser

#---Local library---
from logger_config import *
import logger_config
from constants import *

#---Configuring log filename---
log_file=os.path.splitext(os.path.basename(__file__))[0]+".log"
log = logger_config.configure_logger('default', ""+DIR+""+LOG_DIR+"/"+log_file+"")

#---Reads configuration file---
def read_config_file():
    try:
        parser = ConfigParser()
        parser.read(CONFIG_FILENAME)
        return parser
    except Exception as e:
        log.error(colored(str(e),"red"))
