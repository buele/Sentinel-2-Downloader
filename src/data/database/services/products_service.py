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
from sqlalchemy import *
from sqlalchemy.orm import *
import configparser
from src.data.database.entities.product import Product
from src.data.database.entities.product import ProductStatus

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Raffaele Bua"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"

class ProductsService():
    """ This class is the service to manage products inside the database. It is a wrapper to manage products,
        exploiting SqlAlchemy ORM.
    """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("src/data/database/config/db.cfg")
        self.engine = create_engine(config['database']['connection_string'],  pool_recycle=3600)

    def add_new_product(self, product):
        """ Add a new product in the database

            :param product: Product entity to add in the database
            :type product: Product
        """
        result = False
        Session = sessionmaker(bind=self.engine)
        session = Session()
        already_present_product = session.query(Product). \
            filter(Product.name == product.name).all()
        try:
            if len(already_present_product) == 0:
                session.add(product)
                session.commit()
                result = True
            session.close()
        except Exception as err:
            pass

        return result

    def get_products_to_process(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.downloaded).all()
        session.close()
        return result

    def update_product_status(self, product_name, status):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        product = session.query(Product). \
            filter(Product.name == product_name).first()
        if product != None:
            product.status = status
            product.last_modify = datetime.datetime.utcnow()
            session.commit()
        session.close()

    def get_pending_products(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product).\
            filter(Product.status == ProductStatus.pending).all()
        session.close()
        return result

    def get_downloading_products(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.downloading).all()
        session.close()
        return result

    def get_a_downloaded_product(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.downloaded).first()
        session.close()
        return result

    def get_downloaded_products(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Product). \
            filter(Product.status == ProductStatus.downloaded).all()
        session.close()
        return result


