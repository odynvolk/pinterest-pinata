#!/usr/bin/env python
# -*- coding: utf8 -*-
import urllib
import urllib2
import cookielib
import cStringIO
import gzip
import sys
import json
import pdb
import json


class PinterestPinata(object):

    def __init__(self, email=None, password=None):
        if not email or not password:
            raise PinterestPinataException('Illegal arguments email={email}, password={password}'.format(
                email=email, password=password))

        self.email = email
        self.password = password
        self.logged_in = False
        self.csrf_token = None
        self.cookie_jar = None

    def login(self):
        login_url = 'https://pinterest.com/login/'
        self._request(login_url)

        data = urllib.urlencode({
            'source_url': '/login/',
            'data': json.dumps({"options": {"username_or_email": self.email,
                                            "password": self.password}
            }),
            'module_path': 'App()>LoginPage()>Login()>Button(class_name=primary, text=Log in, type=submit, size=large)'
        })

        res, headers, cookies = self._request('http://www.pinterest.com/resource/UserSessionResource/create/',
                                              data=data,
                                              referrer=login_url,
                                              ajax=True)

        if self.email in res:
            self.logged_in = True

    def repin(self, board_id=None, pin_id=None):
        if not board_id or not pin_id:
            raise PinterestPinataException('Illegal arguments board_id={board_id}, pin_id={pin_id}'.format(
                board_id=board_id, pin_id=pin_id))

        if not self.logged_in:
            self.login()

        url = 'http://pinterest.com/pin/' + pin_id

        data = urllib.urlencode({
            'source_url': url,
            'data': '{"options":{"board_id":"391179986322646823","description":"Doldisarna som kan ta sig till Bryssel - DN.SE","link":"http://www.dn.se/valet-2014/doldisarna-som-kan-ta-sig-till-bryssel/","is_video":false,"pin_id":"512566001313223479"},"context":{}}',
            'module_path': 'App()>Closeup(resource=PinResource(fetch_visual_search_objects=true, id=512566001313223479))>PinActionBar(resource=PinResource(id=512566001313223479))>ShowModalButton(module=PinCreate)#Modal(module=PinCreate(resource=PinResource(id=512566001313223479)))'
        })

        res, header, query = self._request('http://www.pinterest.com/resource/RepinResource/create/',
                                           data=data,
                                           referrer=url,
                                           ajax=True)

    def _request(self, url, data=None, referrer='http://google.com/', ajax=False):
        handlers = []

        urllib2.HTTPRedirectHandler.max_redirections = 2

        if not self.cookie_jar:
            self.cookie_jar = cookielib.CookieJar()

        cookie_handler = urllib2.HTTPCookieProcessor(self.cookie_jar)
        handlers.append(cookie_handler)

        opener = urllib2.build_opener(*handlers)

        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.1 \
                      (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'),
            ('Accept', 'image/png,image/*;q=0.8,*/*;q=0.5'),
            ('Accept-Language', 'en-us,en;q=0.5'),
            ('Accept-Encoding', 'gzip,deflate'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
            ('Keep-Alive', '3600'),
            ('Host', 'www.pinterest.com'),
            ('Origin', 'http://www.pinterest.com'),
            ('Connection', 'keep-alive'),
            ('Referer', referrer),
            ('X-NEW-APP', 1)
        ]
        if ajax:
            opener.addheaders.append(('X-Requested-With', 'XMLHttpRequest'))
        if self.csrf_token:
            opener.addheaders.append(('X-CSRFToken', self.csrf_token))
        error_happen = False
        html = ''
        try:
            req = urllib2.Request(url, data)
            r = opener.open(req, timeout=10)
            html = r.read()
        except Exception, e:
            sys.exc_clear()
            error_happen = e

        if error_happen:
            return error_happen, {}, {}

        headers = r.info()
        # If we get gzipped data the unzip it
        if ('Content-Encoding' in headers.keys() and headers['Content-Encoding']=='gzip') or \
                ('content-encoding' in headers.keys() and headers['content-encoding']=='gzip'):
            data = cStringIO.StringIO(html)
            gzipper = gzip.GzipFile(fileobj=data)
            # Some servers may return gzip header, but not zip data.
            try:
                html_unzipped = gzipper.read()
            except:
                sys.exc_clear()
            else:
                html = html_unzipped

        cookies = {cookie.name:cookie.value for cookie in self.cookie_jar}
        self.csrf_token = cookies['csrftoken']

        return html, headers, cookies


class PinterestPinataException(Exception):
    pass


if __name__ == "__main__":
    import traceback
    try:
        pinata = PinterestPinata(email=sys.argv[1], password=sys.argv[2])
        pinata.repin(board_id='391179986322646823', pin_id='512566001313223479')
    except PinterestPinataException:
        print traceback.format_exc()
    finally:
        pass