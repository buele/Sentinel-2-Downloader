#!/usr/bin/env python

# ==================================================================================== #
#
# Copyright (c) 2017 Sardegna Clima - Raffaele Bua (buele)
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

from src.core.Configuration import Configuration
import re
import datetime
import configparser
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Raffaele Bua"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class ConfigurationManager:
    def __init__(self):
        """ This class manages configurations, it extracts the configurations strings from the
        config file and put the values in the *Configuration*  class.
        """
        logger.debug("(ConfigurationManager __init__)")
        self.config = configparser.ConfigParser()
        self.config.read("/usr/downloader/src/core/config/config.cfg")
        self.configuration = Configuration()
        self.load_configuration()

    def get_configuration(self):
        return self.configuration

    def datetime_from_string(self, date_string):
        date_regex = "([0-9]*)/([0-9]*)/([0-9]*)"
        date_match = re.search(date_regex, date_string)
        return datetime.date(int(date_match.group(1)),
                             int(date_match.group(2)),
                             int(date_match.group(3)))
    def load_end_date(self ):
        end_date = self.config['FILTER']['end_date']
        if end_date != 'NOW':
            return self.datetime_from_string(end_date)
        else:
            return datetime.datetime.now().date()

    def load_start_date(self):
        start_date = self.config['FILTER']['start_date']
        return self.datetime_from_string(start_date)

    def load_tiles(self):
        return self.config['FILTER']['tiles'].split(',')

    def load_files_to_download(self):
        return self.config['FILTER']['files_to_download'].split(',')

    def load_aws_xmlns(self):
        return self.config['AWS']['xmlns']

    def load_aws_products_regex(self):
        return self.config['AWS']['products_regex']

    def load_aws_domain(self):
        return self.config['AWS']['domain']

    def load_inbox_path(self):
        return self.config['DOWNLOADER']['inbox_path']

    def load_parallel_downloads(self):
        return self.config['DOWNLOADER']['parallel_downloads']

    def load_configuration(self):
        logger.debug("(ConfigurationManager load_configuration)")
        self.configuration.start_date = self.load_start_date()
        self.configuration.end_date = self.load_end_date()
        self.configuration.tiles = self.load_tiles()
        self.configuration.files = self.load_files_to_download()
        self.configuration.aws_xmlns = self.load_aws_xmlns()
        self.configuration.aws_products_regex = self.load_aws_products_regex()
        self.configuration.aws_domain = self.load_aws_domain()
        self.configuration.inbox_path = self.load_inbox_path()
        self.configuration.parallel_downloads = self.load_parallel_downloads()
        logger.debug("(ConfigurationManager load_configuration) finished")











