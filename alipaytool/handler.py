# coding: utf-8
import base64

import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class MobilePayHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        params = self._params_format()
        http_client = AsyncHTTPClient()
        verify_url = '%spartner=%s&notify_id=%s' % (
            self.application.settings.get('HTTPS_VERIFY_URL'),
            self.application.settings.get('ALI_PARTNER'),
            params.get('notify_id')
        )
        try:
            response = yield tornado.gen.Task(http_client.fetch, verify_url)
            resp_text = response.body
        except:
            resp_text = ''
        if resp_text != 'true':
            print 'notify_id error'
            self.write('fail')
            self.finish()
            return
        is_sign = self._sign_verify(params)
        if not is_sign:
            print 'sign error'
            self.write('fail')
            self.finish()
            return
        self.do_business_logic(params)
        self.write('success')
        self.finish()
        return

    def _params_format(self):
        params = {}
        for key in self.request.body_arguments.keys():
            values = ''
            for index, value in enumerate(self.request.body_arguments[key]):
                values += value if index == len(self.request.body_arguments[key]) - 1 \
                    else value + ','
            params[key] = values
        return params

    def _sign_verify(self, params):
        sign_str = self._create_sign_string(params)
        is_sign = self._verify_sign(
            self.application.settings.get('ALI_PUBLIC_KEY'),
            sign_str,
            params.get('sign', '')
        )
        return is_sign

    def _create_sign_string(self, params):
        result = ''
        for index, key in enumerate(sorted(params)):
            value = params.get(key)
            if value == '' or key == 'sign' or key == 'sign_type':
                continue
            result += key + '=' + value if index == len(params.keys()) - 1\
                else key + '=' + value + '&'
        return result

    def _verify_sign(self, public_key, sign_str, sign):
        rsa_key = RSA.importKey(public_key)
        signer = PKCS1_v1_5.new(rsa_key)
        digest = SHA.new(sign_str)
        if signer.verify(digest, base64.decodestring(sign)):
            return True
        return False

    def do_business_logic(self, params):
        pass
