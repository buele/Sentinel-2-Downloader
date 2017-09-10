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


import datetime
import re
from collections import OrderedDict
import urllib.request
import xml.etree.ElementTree as ET
from src.data.logger.logger import logger

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Raffaele Bua"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class AmazonBucketManager:
    """ This class is an Adapter of Amazon AWS services.
        Main goal of this class is **Retrieve the list of products from aws via tile list, and time interval**
    """
    def __init__(self, configurations):

        self.config = configurations
        self.product_list = []
        self.last_item = None
        return

    def generate_url(self, tile, year):
        """ This method generates the aws url from the tile name string and the start year of filter interval.
            AWS service has the *prefix* parameter, to filter the list of available files in the bucket.
            This method generates the proper *prefix* parameter value, to give the list of files
            available in the year of *year* argument passed in the method.

            The generated parameter is like:

            .. code-block:: bash

                prefix=tiles/{tile}/{year}/

            :param tile: The tile name string with a pattern like

            .. code-block:: bash

                32/T/MK

            :param year: The year
            :returns: request url
            :rtype: String
        """
        url_template = 'http://sentinel-s2-l1c.s3.amazonaws.com/?list-type=2&prefix=tiles/{tile}/{year}/'
        url = url_template.format(tile=tile, year=year)
        return url

    def extract_date(self, item):
        """ This method extracts the date from the tile name string (complete with the date).

            :param item: The tile name complete string. e.g.

            .. code-block:: bash

                tiles/32/T/MK/YYYY/MM/DD/

            where
                * **YYYY** is the year
                * **MM** is the month
                * **DD** is the day

            :returns: The extracted date form the tile name string
            :rtype: Datetime
            The method apply the regex:

            .. code-block:: bash

                tiles/[0-9]2/[A-Z]/[A-Z]{2}/([0-9]{4})/([0-9]*)/([0-9]*)/

            to the *item* parameter
        """
        regex = 'tiles/[0-9]2/[A-Z]/[A-Z]{2}/([0-9]{4})/([0-9]*)/([0-9]*)/'
        match = re.search(regex, item)
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return datetime.date(int(year), int(month), int(day))

    def load_products(self, tile, year, paginated=False):
        """ *load_products* load list products form the Amazon *AWS* Bucket of Sinergise *Sentinel-2 on AWS*.
            This method contains the *AWS* APIs semantic it is the core of Adapter.
            It manages also pagination.

            :param tile: Tile name
            :type tile: String
            :param year: Year of interest, the method extract the whole list of products for this year
            :type year: String
            :param paginated: if this parameter is *True* that means that the list provided from AWS is
                              paginated and the next page starts after the *last_item*
            :type year: Boolean
            :returns: None
            :rtype: None

            This method stores the list of products in the classes property *product_list*.
        """
        logger.debug("(AmazonBucketManager load_products)")
        # Generate url for year
        url = self.generate_url(tile, year)
        # Append to url start_from attribute if the request is paginated
        if paginated:
            url = url + "&start-after=" + self.last_item
        # Http request
        response = urllib.request.urlopen(url)
        root = ET.fromstring(response.read().decode('utf-8'))
        # Extract data from xml
        contents = root.findall('{'+self.config.aws_xmlns+'}Contents')
        for item in contents:
            key = item.find('{' + self.config.aws_xmlns + '}Key').text
            product_path = ''
            try:
                product_path = re.search(self.config.aws_products_regex, key)
            except ValueError:
                logger.warn("Product not found for key: " + key)
            self.product_list.append(product_path.group(0))
        # Check if the page is truncated (paginated case)
        if root.find('{' + self.config.aws_xmlns + '}IsTruncated').text == 'true':
            self.last_item = contents[-1].find('{' + self.config.aws_xmlns + '}Key').text
            return True
        else:
            return False

    def get_products_list(self, searchFilter):
        """ This method manages the retrieval of aws products.
            This method contains the *AWS* APIs semantic it is the core of Adapter.
            It manages also pagination.

            :param searchFilter: Search parameters to filter the available files in the bucket
            :type searchFilter: SearchFilter

            :returns: The pending products available in the Amazon bucket.
            :rtype: None

            .. todo:: Optimize list retrieval using set end date year instead *NOW* year.
        """
        logger.debug("(AmazonBucketManager get_products_list)")
        tile = searchFilter.tile
        self.product_list = []
        self.last_item = None
        year = int(searchFilter.start_date.year)
        current_year = datetime.datetime.now().year
        pending_products = []
        # Extract whole list of products via amazon, from start year to now
        # TODO: OPTMIZE IT USING THE END DATE FROM CONFIGURATION AND NOT *NOW*
        while year <= current_year:
            is_truncated = self.load_products(tile, year, False)
            while is_truncated:
                is_truncated = self.load_products(tile, year, True)
            year += 1
        # Clean list of products
        self.product_list = set(self.product_list)
        # Generate dictionary
        dict = {}
        for product in self.product_list:
            date = self.extract_date(str(product))
            product_string = str(product)
            dict[date] = product_string
        # Sort dictionary
        dict = OrderedDict(sorted(dict.items()))
        # Filter products via date interval
        for product_date in dict:
            if product_date >= searchFilter.start_date and product_date <= searchFilter.end_date:
                pending_products.append(dict[product_date])
        return pending_products

