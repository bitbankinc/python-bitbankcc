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
from .utils import error_parser, try_json_parse
from hashlib import sha256
from logging import getLogger
import requests, hmac, time, json, contextlib, re

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode


logger = getLogger(__name__)


def get_path_from_end_point(end_point):
    match = re.match(r'^(?:http|ws)s?://[^/]+(/.+)$', end_point)
    return '' if match == None else match[1]

def sign_request(key, query):
    h = hmac.new(bytearray(key, 'utf8'), bytearray(query, 'utf8'), sha256)
    return h.hexdigest()

def make_nonce_header(query_data, api_key, api_secret):
    nonce = str(int(time.time() * 1000))
    message = nonce + query_data
    return {
        'Content-Type': 'application/json',
        'ACCESS-KEY': api_key,
        'ACCESS-NONCE': nonce,
        'ACCESS-SIGNATURE': sign_request(api_secret, message)
    }

def make_request_time_header(query_data, api_key, api_secret, time_window):
    request_time = str(int(time.time() * 1000))
    time_window = str(time_window)
    message = "".join([request_time, time_window, query_data])
    return {
        'Content-Type': 'application/json',
        'ACCESS-KEY': api_key,
        'ACCESS-REQUEST-TIME': request_time,
        'ACCESS-TIME-WINDOW': time_window,
        'ACCESS-SIGNATURE': sign_request(api_secret, message)
    }

default_config = {
    'end_point':'https://api.bitbank.cc/v1',
    'auth_method': 'request_time',
    'time_window': 5000,
}

class bitbankcc_private(object):

    def __init__(self, api_key, api_secret, end_point='https://api.bitbank.cc/v1', config=default_config):
        self.end_point = config['end_point'] if 'end_point' in config else 'https://api.bitbank.cc/v1'
        self.path_stub = get_path_from_end_point(self.end_point)
        self.api_key = api_key
        self.api_secret = api_secret
        self.auth_method = config['auth_method'] if 'auth_method' in config else 'request_time'
        self.time_window = config['time_window'] if 'time_window' in config else 5000

    def _get_query(self, path, query):
        data = self.path_stub + path + urlencode(query)
        logger.debug('GET: ' + data)
        headers = make_request_time_header(data, self.api_key, self.api_secret, self.time_window) \
            if self.auth_method == 'request_time' \
            else make_nonce_header(data, self.api_key, self.api_secret)
        uri = self.end_point + path + urlencode(query)
        with contextlib.closing(requests.get(uri, headers=headers)) as response:
            response.raise_for_status()
            return error_parser(try_json_parse(response, logger))

    def _post_query(self, path, query):
        data = json.dumps(query)
        logger.debug('POST: ' + data)
        headers = make_request_time_header(data, self.api_key, self.api_secret, self.time_window) \
            if self.auth_method == 'request_time' \
            else make_nonce_header(data, self.api_key, self.api_secret)
        uri = self.end_point + path
        with contextlib.closing(requests.post(uri, data=data, headers=headers)) as response:
            response.raise_for_status()
            return error_parser(try_json_parse(response, logger))

    def get_asset(self):
        return self._get_query('/user/assets', {})

    def get_order(self, pair, order_id):
        return self._get_query('/user/spot/order?', {
            'pair': pair,
            'order_id': order_id
        })

    # XXX: options should be named arguments like get_trade_history?
    #      this breaks compat.
    def get_active_orders(self, pair, options=None):
        if options is None:
            options = {}
        if not 'pair' in options:
            options['pair'] = pair
        return self._get_query('/user/spot/active_orders?', options)

    def order(self, pair, price, amount, side, order_type, post_only = None, trigger_price = None, position_side = None):
        params = {
            'pair': pair,
            'amount': amount,
            'side': side,
            'type': order_type
        }
        if price != None: params['price'] = price
        if post_only != None: params['post_only'] = post_only
        if trigger_price != None: params['trigger_price'] = trigger_price
        if position_side != None: params['position_side'] = position_side
        return self._post_query('/user/spot/order', params)

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

    def get_trade_history(self, pair, order_count, order_id = None, since = None, end = None, order = None):
        params = {
            'pair': pair,
            'count': order_count
        }
        if order_id != None: params['order_id'] = order_id
        if since != None: params['since'] = since
        if end != None: params['end'] = end
        if order != None: params['order'] = order
        return self._get_query('/user/spot/trade_history?', params)

    def get_margin_positions(self):
        return self._get_query('/user/margin/positions', {})

    def get_deposit_history(self, asset, count = None, since = None, end = None, order = None):
        params = {
            'asset': asset,
        }
        if count != None: params['count'] = count
        if since != None: params['since'] = since
        if end != None: params['end'] = end
        if order != None: params['order'] = order
        return self._get_query('/user/deposit_history?', params)

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

    def get_withdraw_history(self, asset, count = None, since = None, end = None, order = None):
        params = {
            'asset': asset,
        }
        if count != None: params['count'] = count
        if since != None: params['since'] = since
        if end != None: params['end'] = end
        if order != None: params['order'] = order
        return self._get_query('/user/withdrawal_history?', params)

    def get_subscribe(self):
        return self._get_query('/user/subscribe', {})
