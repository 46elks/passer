from urllib.error import HTTPError
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from base64 import b64encode
import os
import json

class Elks:
    client_key = None
    client_secret = None
    baseurl = "https://api.46elks.com/a1/"

    def __init__(self):
        if 'PASSER_ELKS_KEY' in os.environ:
            self.client_key = os.environ['PASSER_ELKS_KEY']
        if 'PASSER_ELKS_SECRET' in os.environ:
            self.client_secret = os.environ['PASSER_ELKS_SECRET']

    def query_api(self, endpoint, data=None):
        b = lambda x: bytes(x, 'utf-8')
        keysecret = '%s:%s' % (self.client_key, self.client_secret)
        auth = b('BASIC %s' % (b64encode(keysecret)))

        if data:
            conn = Request(call_url, b(urlencode(data)))
        else:
            conn = Request(call_url)

        conn.add_header('Authorization', auth)

        try:
            response = urlopen(conn)
        except HTTPError as err:
            return False
        return response.read()

    def get_text_by_id(self, id_):
        elks_data = query_api('/SMS/%s' % id_) 
        if not elks_data:
            return False
        data = json.loads(elks_data)
        return data

