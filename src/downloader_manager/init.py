#!/usr/bin/env python

# ==================================================================================== #
#
# Copyright (c) 2017 Raffaele Bua (buele)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==================================================================================== #

import sys
import subprocess
from crontab import CronTab
print("DEBUG")
sys.path.append('/usr/downloader/')
import configparser
from src.downloader_manager.downloader_manager import DownloaderManager
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Raffaele Bua"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

dm = DownloaderManager()


# set cron tab
config = configparser.ConfigParser()
config_file_path = "/usr/downloader/src/downloader_manager/config/config.cfg"
config.read(config_file_path)
cron = CronTab(user=config['CRON']['user'])
job = cron.new(command=config['CRON']['command'])
job.setall(config['CRON']['cron'])
cron.write()







