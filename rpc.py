import requests, json, os
import os, sys, errno

class BitcoinRPC:
    def __init__(self, user, passwd, host="127.0.0.1", port=8332, protocol="http", wallet_name="", timeout=30, **kwargs):
        self.user = user
        self.passwd = passwd
        self.port = port
        self.protocol = protocol
        self.host = host
        self.wallet_name = wallet_name
        self.timeout = timeout
        self.r = None

    def wallet(self, wallet_name=""):
        return BitcoinRPC(user=self.user,
                      passwd=self.passwd,
                      port=self.port,
                      protocol=self.protocol,
                      host=self.host,
                      wallet_name=wallet_name,
                      timeout=self.timeout)

    @property
    def url(self):
        return "{s.protocol}://{s.user}:{s.passwd}@{s.host}:{s.port}/wallet/{s.wallet_name}".format(s=self)

    def __getattr__(self, method):
        headers = {'content-type': 'application/json'}

        # TODO: async
        def fn(*args, **kwargs):
            payload = {
                "method": method,
                "params": args,
                "jsonrpc": "2.0",
                "id": 0,
            }
            timeout = self.timeout
            if "timeout" in kwargs:
                timeout = kwargs["timeout"]
            url = self.url
            if "wallet" in kwargs:
                url = url+"/wallet/{}".format(kwargs["wallet"])
            # TODO: await
            r = requests.post(
                url, data=json.dumps(payload), headers=headers, timeout=timeout)
            self.r = r
            if r.status_code != 200:
                raise Exception("Server responded with error code %d: %s" % (r.status_code, r.text))
            r = r.json()
            if r["error"] is not None:
                raise Exception(r["error"])
            return r["result"]
        return fn
