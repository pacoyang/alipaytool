# 介绍
alipaytool是基于tornado异步机制写的支付宝服务端异步回调代码，暂时只有移动支付(即时到账)的回调程序。

# 使用方法
```python
import tornado.web
from tornado.ioloop import IOLoop
from alipaytool.handler import MobilePayHandler

# alipay notify_id verify url
HTTPS_VERIFY_URL = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'
# your alipay partner
ALI_PARTNER = 'XXX'
# you alipay public key just like '-----BEGIN PUBLIC KEY-----\nXXXX\n-----END PUBLIC KEY-----'
ALI_PUBLIC_KEY = 'XXX'


class TestAlipayNotifyHandler(MobilePayHandler):
    def do_business_logic(self, params):
        out_trade_no = params['out_trade_no']
        trade_no = params['trade_no']
        trade_status = params['trade_status']
        total_fee = params['total_fee']
        buyer_email = params['buyer_email']
        print out_trade_no, trade_no, trade_status, total_fee, buyer_email
        return


application = tornado.web.Application(
    [(r'^/notify$', TestAlipayNotifyHandler)],
    **{'HTTPS_VERIFY_URL': HTTPS_VERIFY_URL, 'ALI_PARTNER': ALI_PARTNER, 'ALI_PUBLIC_KEY': ALI_PUBLIC_KEY}
)


if __name__ == '__main__':
    application.listen(8088)
    IOLoop.instance().start()

```
您可以在do_business_logic中重写你的业务代码
