#!/usr/bin/env python
# -*- coding: utf8 -*-
import re
import urllib
import urllib2
import cookielib
import cStringIO
import gzip
import sys
import pdb
import json


class PinterestPinata(object):

    def __init__(self, email=None, password=None, username=None):
        if not email or not password:
            raise PinterestPinataException('Illegal arguments email={email}, password={password}, username={username}'.format(
                email=email, password=password, username=username))

        self.email = email
        self.password = password
        self.username = username
        self.logged_in = False
        self.csrf_token = None
        self.cookie_jar = cookielib.CookieJar()
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookie_jar)
        urllib2.HTTPRedirectHandler.max_redirections = 2

    def login(self):
        login_url = 'https://pinterest.com/login/'
        self._request(login_url)

        data = urllib.urlencode({
            'source_url': '/login/',
            'data': json.dumps({'options': {'username_or_email': self.email,
                                            'password': self.password}}),
            'module_path': 'App()>LoginPage()>Login()>Button(class_name=primary, text=Log in, type=submit, size=large)'
        })

        res, headers, cookies = self._request('http://www.pinterest.com/resource/UserSessionResource/create/',
                                              data=data,
                                              referrer=login_url,
                                              ajax=True)

        if self.email in res:
            self.logged_in = True

    def boards(self, username):
        res = self._request('http://www.pinterest.com/' + username + '/')

        boards = []
        for x in re.findall(r'<a.*class="boardLinkWrapper".*', res[0]):
            boards.append('http://www.pinterest.com' + re.findall(r'"/.*/"', x)[0].replace('"', ''))

        return boards

    def pin(self, board_id=None, description=None, image_url=None, link=None):
        if not board_id or not description or not image_url or not link:
            raise PinterestPinataException('Illegal link board_id={board_id}, description={description}, image_url={image_url}, '
                                           'link={description}'.format(
                board_id=board_id, description=description, image_url=image_url, link=link))

        if not self.logged_in:
            self.login()

        url = 'http://pinterest.com/pin/create/bookmarklet/'

        data = urllib.urlencode({
            'source_url': url,
            'data': json.dumps({'options': {'board_id': board_id,
                                            'description': description,
                                            'link': link,
                                            'image_url': image_url}}),
            'module_path': 'App()>PinBookmarklet()>PinCreate()>PinForm()>'
                           'Button(class_name=repinSmall pinIt, text=Pin it, disabled=false, has_icon=true, show_text=false, type=submit, color=primary)'
        })

        res, header, query = self._request('http://www.pinterest.com/resource/PinResource/create/',
                                           data,
                                           referrer=url,
                                           ajax=True)

        if 'PinResource' in res:
            json_res = json.loads(res)
            return json_res['resource_response']['data']['id']

        return -1

    def repin(self, board_id=None, pin_id=None, link=None, description=None):
        if not board_id or not pin_id or not link or not description:
            raise PinterestPinataException('Illegal arguments board_id={board_id}, pin_id={pin_id}, link={link}, '
                                           'description={description}'.format(
                board_id=board_id, pin_id=pin_id, link=link, description=description))

        if not self.logged_in:
            self.login()

        url = 'http://pinterest.com/pin/' + pin_id

        data = urllib.urlencode({
            'source_url': url,
            'data': json.dumps({'options': {'board_id': board_id,
                                            'pin_id': pin_id,
                                            'link': link,
                                            'description': description,
                                            }
            }),
            'module_path': 'App()>Closeup(resource=PinResource(fetch_visual_search_objects=true, id={pin_id}))>'
                           'PinActionBar(resource=PinResource(id={pin_id}))>ShowModalButton(module=PinCreate)'
                           '#Modal(module=PinCreate(resource=PinResource(id={pin_id})))'.format(pin_id=pin_id)
        })

        res, header, query = self._request('http://www.pinterest.com/resource/RepinResource/create/',
                                           data=data,
                                           referrer=url,
                                           ajax=True)

        if 'RepinResource' in res:
            json_res = json.loads(res)
            return json_res['resource_response']['data']['id']

        return -1

    def _add_headers(self, opener, referrer='http://google.com/', ajax=False):
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
            ('X-NEW-APP', 1)
        ]
        opener.addheaders.append(('Referer', referrer))
        if ajax:
            opener.addheaders.append(('X-Requested-With', 'XMLHttpRequest'))
        if self.csrf_token:
            opener.addheaders.append(('X-CSRFToken', self.csrf_token))

    def _request(self, url, data=None, referrer='http://google.com/', ajax=False):
        handlers = [self.cookie_handler]
        opener = urllib2.build_opener(*handlers)
        self._add_headers(opener, referrer, ajax)

        html = ''
        try:
            req = urllib2.Request(url, data)
            res = opener.open(req, timeout=10)
            html = res.read()
        except Exception as e:
            sys.exc_clear()
            print "Something went terribly wrong {e}".format(e=e)
            return False, {}, {}

        headers = res.info()
        if ('Content-Encoding' in headers.keys() and headers['Content-Encoding'] == 'gzip') or \
                ('content-encoding' in headers.keys() and headers['content-encoding'] == 'gzip'):
            data = cStringIO.StringIO(html)
            gzipper = gzip.GzipFile(fileobj=data)
            try:
                html_unzipped = gzipper.read()
            except Exception:
                sys.exc_clear()
            else:
                html = html_unzipped

        cookies = {cookie.name: cookie.value for cookie in self.cookie_jar}
        self.csrf_token = cookies['csrftoken']

        return html, headers, cookies


class PinterestPinataException(Exception):
    pass


if __name__ == "__main__":
    import traceback
    try:
        pinata = PinterestPinata(email=sys.argv[1], password=sys.argv[2], username=sys.argv[3])
        print pinata.boards(sys.argv[3])
    except PinterestPinataException:
        print traceback.format_exc()
