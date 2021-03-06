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

from src.core.AmazonBucketManager import AmazonBucketManager
from src.core.ProductDownloader import ProductDownloader
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017 Raffaele Bua"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class Datasource:
    """ This class is the datasource of all data used by the *Downloader*.
    """
    def __init__(self, configurations):
        logger.debug("(Datasource __init__)")
        self.configurations = configurations
        self.abm = AmazonBucketManager(configurations)
        self.productDownloader = ProductDownloader(configurations.inbox_path,
                                                   configurations.files,
                                                   configurations.aws_domain)
        return

    def get_products_list(self, search_filter):
        """ This method generates the product list from query filters defined in the config file
            by the user.

            :param searchFilter: Search parameters to filter the available files in the bucket
            :type searchFilter: SearchFilter

            :returns: The list of available products.
            :rtype: List

        """
        logger.debug("(Datasource get_products_list)")
        products_list = self.abm.get_products_list(search_filter)
        logger.debug("(Datasrouce get_products_list) list of products:")
        for product_name in products_list:
            logger.debug("(Datasource get_products_list) product_name: " + product_name)
        return products_list

    def download_product(self, product):
        """ This method donwloads  the product passed as method paramenter.

            :param product: The product to download
            :type product: Product

            :returns: None
            :rtype: None

        """
        self.productDownloader.download_product(product)
