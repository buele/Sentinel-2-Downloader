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

import os
import urllib.request
from src.data.database.services.products_service import ProductsService
from src.data.database.entities.product import *
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Raffaele Bua"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class ProductDownloader:
    """ This class is the interface with the internet to retrieve data from remote datasource.
    """
    def __init__(self, inbox_path, files_to_download, domain):
        logger.debug("(ProductDownloader __init__) ")
        self.inbox_path = inbox_path
        self.files_to_download = files_to_download
        self.domain = domain
        return

    def download_product(self, product_name):
        """ This method launches the http request to download the product via product name.

            :param product_name: The name of product to download
            :type product_name: String

            :returns: None
            :rtype: None

        """
        logger.debug("(ProductDownloader download_product) ")
        logger.debug("(ProductDownloader download_product) product.name: " + product_name)
        new_product_path = self.inbox_path + product_name.replace("/", "-")[:-1]
        if not os.path.exists(new_product_path):
            os.makedirs(new_product_path)
        files_to_download = self.files_to_download #.split(',')
        for file_name in files_to_download:
            url = self.domain + product_name + file_name
            new_file_path = new_product_path + '/' + file_name
            urllib.request.urlretrieve(url, new_file_path)
