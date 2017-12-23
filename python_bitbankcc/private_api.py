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
from hashlib import sha256
from logging import getLogger
import requests, hmac, time, json

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode


logger = getLogger(__name__)


def sign_request(key, query):
    h = hmac.new(bytearray(key, 'utf8'), bytearray(query, 'utf8'), sha256)
    return h.hexdigest()

def make_header(query_data, api_key, api_secret):
    nonce = str(int(time.time() * 1000))
    message = nonce + query_data
    return {
        'Content-Type': 'application/json',
        'ACCESS-KEY': api_key,
        'ACCESS-NONCE': nonce,
        'ACCESS-SIGNATURE': sign_request(api_secret, message)
    }

class bitbankcc_private(object):
    
    def __init__(self, api_key, api_secret):
        self.end_point = 'https://api.bitbank.cc/v1'
        self.api_key = api_key
        self.api_secret = api_secret
    
    def _get_query(self, path, query):
        data = '/v1' + path + urlencode(query)
        logger.debug('GET: ' + data)
        headers = make_header(data, self.api_key, self.api_secret)
        uri = self.end_point + path + urlencode(query)
        response = requests.get(uri, headers=headers)
        return error_parser(response.json())
    
    def _post_query(self, path, query):
        data = json.dumps(query)
        logger.debug('POST: ' + data)
        headers = make_header(data, self.api_key, self.api_secret)
        uri = self.end_point + path
        response = requests.post(uri, data=data, headers=headers)
        return error_parser(response.json())
    
    def get_asset(self):
        return self._get_query('/user/assets', {})
    
    def get_order(self, pair, order_id):
        return self._get_query('/user/spot/order?', {
            'pair': pair,
            'order_id': order_id
        })
    
    def get_active_orders(self, pair, options=None):
        if options is None:
            options = {}
        if not 'pair' in options:
            options['pair'] = pair
        return self._get_query('/user/spot/active_orders?', options)

    def order(self, pair, price, amount, side, order_type):
        return self._post_query('/user/spot/order', {
            'pair': pair,
            'price': price,
            'amount': amount,
            'side': side,
            'type': order_type
        })
    
    def cancel_order(self, pair, order_id):
        return self._post_query('/user/spot/cancel_order', {
            'pair': pair,
            'order_id': order_id
        })

    def cancel_orders(self, pair, order_ids):
        return self._post_query('/user/spot/cancel_orders', {
            'pair': pair,
            'order_ids': order_ids
        })

    def get_orders_info(self, pair, order_ids):
        return self._post_query('/user/spot/orders_info', {
            'pair': pair,
            'order_ids': order_ids
        })

    def get_trade_history(self, pair, order_count):
        return self._get_query('/user/spot/trade_history?', {
            'pair': pair,
            'count': order_count
        })

    def get_withdraw_account(self, asset):
        return self._get_query('/user/withdrawal_account?', {
            'asset': asset
        })

    def request_withdraw(self, asset, uuid, amount, token):
        q = {
            'asset': asset,
            'uuid': uuid,
            'amount': amount
        }
        q.update(token)
        return self._post_query('/user/request_withdrawal', q)
