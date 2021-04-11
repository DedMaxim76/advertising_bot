import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

import pyqiwi  # Библиотека называется qiwipy, но модуль pyqiwi!
import requests

from data import config
from data.config import QIWI_TOKEN, WALLET_QIWI

wallet = pyqiwi.Wallet(token=QIWI_TOKEN, number=WALLET_QIWI)


class NoPaymentFound(Exception):
    pass


class NotEnoughMoney(Exception):
    pass


@dataclass
class Payment:
    amount: int
    id: str = None

    def create(self):
        self.id = str(uuid.uuid4())

    def check_payment(self):
        for tx in wallet.history(rows=50, start_date=datetime.now() - timedelta(days=2))["transactions"]:
            if tx.comment:
                if str(self.id) in tx.comment:
                    if float(tx.total.amount) >= float(self.amount):
                        return True
                    else:

                        raise NotEnoughMoney

        else:
            raise NoPaymentFound

    @property
    def invoice(self):
        link = "https://oplata.qiwi.com/create?publicKey={pubkey}&amount={amount}&comment={comment}"
        return link.format(pubkey=config.QIWI_PUBKEY, amount=self.amount, comment=self.id)

    @staticmethod
    def send_to_card(payment_data):
        # payment_data - dictionary with all payment data
        s = requests.Session()
        s.headers['Accept'] = 'application/json'
        s.headers['Content-Type'] = 'application/json'
        s.headers['authorization'] = 'Bearer ' + wallet.token
        postjson = {"id": "", "sum": {"amount": "", "currency": "643"},
                    "paymentMethod": {"type": "Account", "accountId": "643"}, "fields": {"account": ""}}
        postjson['id'] = str(int(time.time() * 1000))
        postjson['sum']['amount'] = payment_data.get('sum')
        postjson['fields']['account'] = payment_data.get('to_card')
        prv_id = payment_data.get('prv_id')

        res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/' + prv_id + '/payments', json=postjson)
        return res.json()

    @staticmethod
    def send_to_qiwi(to_qw, amount):
        s = requests.Session()
        s.headers = {'content-type': 'application/json',
                     'authorization': 'Bearer ' + wallet.token,
                     'User-Agent': 'Android v3.2.0 MKT',
                     'Accept': 'application/json'}
        postjson = {"sum": {"amount": "", "currency": ""},
                    "paymentMethod": {"type": "Account", "accountId": "643"}, "comment": "'+comment+'",
                    "fields": {"account": ""}, 'id': str(int(time.time() * 1000))}
        postjson['sum']['amount'] = amount
        postjson['sum']['currency'] = '643'
        postjson['fields']['account'] = to_qw
        res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=postjson)
        return res.json()

    @staticmethod
    def get_card_system(card_number):
        s = requests.Session()
        res = s.post('https://qiwi.com/card/detect.action', data={'cardNumber': card_number})
        return res.json()['message']
