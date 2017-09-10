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
import enum
from sqlalchemy import *
from sqlalchemy.orm import *
from src.data.database.base import Base

__author__ = "Raffaele Bua (buele)"
__copyright__ = "Copyright 2017, Raffaele Bua"
__credits__ = ["Raffaele Bua"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raffaele Bua"
__contact__ = "info@raffaelebua.eu"
__status__ = "Development"


class ProductStatus(enum.Enum):
    """ Possible product statuses in the database.
    """
    pending = "pending"
    downloading = "downloading"
    downloaded = "downloaded"


class Product(Base):
    """ SqlAlchemy product entity.
    """
    __tablename__ = 'products'
    id = Column(Integer, Sequence('products_id_seq'), primary_key=True)
    name = Column(String(50))
    status = Column(Enum(ProductStatus))
    last_modify = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "{\"name\":\"%s\", \"status\":\"%s\", \"last_modify\":\"%s\"}" % (
            self.name, str(self.status), str(self.last_modify))