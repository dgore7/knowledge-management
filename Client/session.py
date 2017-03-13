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