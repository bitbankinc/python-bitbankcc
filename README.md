# python_bitbankcc

このライブラリは https://bitbank.cc/ の Public & Private API をパイソンで扱うためのものです。

## インストール

```
# `@<commit_hash>` で現在のmasterに固定し、インストールすることをオススメします
sudo pip install git+https://github.com/bitbankinc/python-bitbankcc.git@<commit_hash>
```

## パラメーターの詳細

APIドキュメントをご覧いただき、各パラメータについてお読みになって下さい。

https://docs.bitbank.cc/

## 使い方

インポートする
(インストールと違ってモジュール名は `-` ではなく `_` になります)

```python
import python_bitbankcc
```

### パブリックAPI

```python
import json

# public API classのオブジェクトを取得
pub = python_bitbankcc.public()

# PUBLIC TEST

value = pub.get_ticker(
    'btc_jpy' # ペア
)
print(json.dumps(value))

value = pub.get_depth(
    'btc_jpy' # ペア
)
print(json.dumps(value))

value = pub.get_transactions(
    'btc_jpy' # ペア
)
print(json.dumps(value))

# 同じメソッドを日にち指定で
value = pub.get_transactions(
    'btc_jpy', # ペア
    '20170313' # YYYYMMDD 型の日付
)
print(json.dumps(value))

value = pub.get_candlestick(
    'btc_jpy', # ペア
    '1hour', # タイプ
    '20170313' # YYYYMMDD 型の日付
)
print(json.dumps(value))
```

### プライベートAPI

```python
import os, json

API_KEY = os.environ['BITBANK_API_KEY']
API_SECRET = os.environ['BITBANK_API_SECRET']

prv = python_bitbankcc.private(API_KEY, API_SECRET)

# PRIVATE TEST

value = prv.get_asset()
print(json.dumps(value))

value = prv.get_order(
    'btc_jpy', # ペア
    '71084903' # 注文ID
)
print(json.dumps(value))

value = prv.get_active_orders(
    'btc_jpy' # ペア
)
print(json.dumps(value))

value = prv.order(
    'btc_jpy', # ペア
    '131594', # 価格
    '0.0001', # 注文枚数
    'buy', # 注文サイド
    'market' # 注文タイプ
)
print(json.dumps(value))

value = prv.cancel_order(
    'btc_jpy', # ペア
    '133493980' # 注文ID
)
print(json.dumps(value))

value = prv.cancel_orders(
    'btc_jpy', # ペア
    ['133503762', '133503949'] # 注文IDのリスト
)
print(json.dumps(value))

value = prv.get_orders_info(
    'btc_jpy', # ペア
    ['133511828', '133511986'] # 注文IDのリスト
)
print(json.dumps(value))

value = prv.get_trade_history(
    'btc_jpy', # ペア
    '10' # 取得する約定数
)

value = prv.get_withdraw_account(
    'btc' # アセットタイプ
)
print(json.dumps(value))

value = prv.request_withdraw(
    'btc', # アセットタイプ
    'e9fb5d9f-0509-4cb5-8325-ec13ade4354c', # 引き出し先UUID
    '10.123', # 引き出し数
    { # 有効になっていた場合に必須
        'otp_token': '387427',
        'sms_token': '836827'
    }
)
print(json.dumps(value))
```
