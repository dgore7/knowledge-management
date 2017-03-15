__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

#TODO: ALLOW  USERS TO STAY LOGGED IN

import http.cookies


class Session:

    def __init__(self, username, password):
        self._conns = {}
        self.cookies = http.cookies.SimpleCookie()
        self.cookies[""]

    def __del__(self):
        self.close()

    def close(self):
        for key, data in self._conns.items():
            for transport, proto in data:
                transport.close()

        self._conns.clear()

    def update_cookies(self, cookies):
        if isinstance(cookies, dict):
            cookies = cookies.items()

        for name, value in cookies:
            if isinstance(value, http.cookies.Morsel):
                dict.__setitem__(self.cookies, name, value)
            else:
                self.cookies[name] = value