#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
# 
# Copyright (c) 2017 bitbank, inc. (ビットバンク株式会社)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
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

from __future__ import absolute_import, division, print_function, unicode_literals
from .utils import error_parser
from logging import getLogger
import requests


logger = getLogger(__name__)


class bitbankcc_public(object):
    
    def __init__(self):
        self.end_point = 'https://public.bitbank.cc'
    
    def _query(self, query_url):
        response = requests.get(query_url)
        return error_parser(response.json())
    
    def get_ticker(self, pair):
        path = '/' + pair + '/ticker'
        return self._query(self.end_point + path)
    
    def get_depth(self, pair):
        path = '/' + pair + '/depth'
        return self._query(self.end_point + path)
    
    def get_transactions(self, pair, yyyymmdd=None):
        path = '/' + pair + '/transactions'
        if yyyymmdd: path += '/' + yyyymmdd
        return self._query(self.end_point + path)
    
    def get_candlestick(self, pair, candle_type, yyyymmdd):
        path = '/' + pair + '/candlestick/' + candle_type + '/' + yyyymmdd
        return self._query(self.end_point + path)
    
