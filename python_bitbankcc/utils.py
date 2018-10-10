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

def error_parser(json_dict):
    if json_dict['success'] == 1:
        return json_dict['data']
    else:
        code = str(json_dict['data']['code'])
        contents = ERROR_CODES[code] if code in ERROR_CODES else '不明なエラーです。サポートにお問い合わせ下さい'
        message = 'エラーコード: ' + code + ' 内容: ' + contents
        raise Exception(message)

ERROR_CODES = {
    '10000': 'URLが存在しません',
    '10001': 'システムエラーが発生しました。サポートにお問い合わせ下さい',
    '10002': '不正なJSON形式です。送信内容をご確認下さい',
    '10003': 'システムエラーが発生しました。サポートにお問い合わせ下さい',
    '10005': 'タイムアウトエラーが発生しました。しばらく間をおいて再度実行して下さい',
    '20001': 'API認証に失敗しました',
    '20002': 'APIキーが不正です',
    '20003': 'APIキーが存在しません',
    '20004': 'API Nonceが存在しません',
    '20005': 'APIシグネチャが存在しません',
    '20011': '２段階認証に失敗しました',
    '20014': 'SMS認証に失敗しました',
    '30001': '注文数量を指定して下さい',
    '30006': '注文IDを指定して下さい',
    '30007': '注文ID配列を指定して下さい',
    '30009': '銘柄を指定して下さい',
    '30012': '注文価格を指定して下さい',
    '30013': '売買どちらかを指定して下さい',
    '30015': '注文タイプを指定して下さい',
    '30016': 'アセット名を指定して下さい',
    '30019': 'uuidを指定して下さい',
    '30039': '出金額を指定して下さい',
    '40001': '注文数量が不正です',
    '40006': 'count値が不正です',
    '40007': '終了時期が不正です',
    '40008': 'end_id値が不正です',
    '40009': 'from_id値が不正です',
    '40013': '注文IDが不正です',
    '40014': '注文ID配列が不正です',
    '40015': '指定された注文が多すぎます',
    '40017': '銘柄名が不正です',
    '40020': '注文価格が不正です',
    '40021': '売買区分が不正です',
    '40022': '開始時期が不正です',
    '40024': '注文タイプが不正です',
    '40025': 'アセット名が不正です',
    '40028': 'uuidが不正です',
    '40048': '出金額が不正です',
    '50003': '現在、このアカウントはご指定の操作を実行できない状態となっております。サポートにお問い合わせ下さい',
    '50004': '現在、このアカウントは仮登録の状態となっております。アカウント登録完了後、再度お試し下さい',
    '50005': '現在、このアカウントはロックされております。サポートにお問い合わせ下さい',
    '50006': '現在、このアカウントはロックされております。サポートにお問い合わせ下さい',
    '50008': 'ユーザの本人確認が完了していません',
    '50009': 'ご指定の注文は存在しません',
    '50010': 'ご指定の注文はキャンセルできません',
    '50011': 'APIが見つかりません',
    '60001': '保有数量が不足しています',
    '60002': '成行買い注文の数量上限を上回っています',
    '60003': '指定した数量が制限を超えています',
    '60004': '指定した数量がしきい値を下回っています',
    '60005': '指定した価格が上限を上回っています',
    '60006': '指定した価格が下限を下回っています',
    '70001': 'システムエラーが発生しました。サポートにお問い合わせ下さい',
    '70002': 'システムエラーが発生しました。サポートにお問い合わせ下さい',
    '70003': 'システムエラーが発生しました。サポートにお問い合わせ下さい',
    '70004': '現在取引停止中のため、注文を承ることができません',
    '70005': '現在買注文停止中のため、注文を承ることができません',
    '70006': '現在売注文停止中のため、注文を承ることができません',
    '70009': 'ただいま成行注文を一時的に制限しています。指値注文をご利用ください。',
    '70010': 'ただいまシステム負荷が高まっているため、最小注文数量を一時的に引き上げています。'
}
