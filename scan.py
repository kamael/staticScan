

from __future__ import print_function
import _mysql
import browser_cookie
import requests
import json
import urllib
import os

from pool import ThreadPool

class CheckObj(object):
    """check object for a type of XSS vul char"""
    def __init__(self, char, callback, logMsg):
        self.char = char
        self.callback = callback
        self.logMsg = logMsg


class Scan(object):
    """Scaning reflect XSS by a static way."""

    def __init__(self, urls, checkObjs, requestFunc = None):
        """
        #   urls:           [(str, params), ...]            ->  list
        #   checkobj:       CheckObj type's object          ->  CheckObj
        #   requestFunc:    request function                ->function
        #
        #   in url:
        #       str:        http://xx.com/xx                ->  string
        #       params:     {p1: p1_str, p2: p2_str, ...}   ->  dict
        """
        assert(isinstance(urls, list))
        assert(isinstance(checkObjs, list))
        self.urls = urls
        self.checkObj = checkObj


        self.logFileiName = '/'.join([os.getcwd(), 'log.txt'])
        self.logFile = open(self.logFileName, 'a+')

        if requestFunc:
            self.request = requestFunc

    def close(self):
        """close logFile"""
        self.logFile.close()

    def check_log(self, respText, obj):
        """ check one resp by one obj
        #   request url, check the return text by obj.callback, if true log [obj.url, obj.logMsg]
        #
        #   parameter:  respText  -> string
        #               obj -> CheckObj
        """
        assert(isinstance(obj, CheckObj))
        callback = obj.callback
        logMsg = obj.logMsg

        def log(msg):
            self.logFile.write(' || '.join([url, logMsg, '\n']))

        if callback(r.text):
            log(logMsg)

    #TODO: check all urls by all CheckObj


    @staticmethod
    def request(url):
        """input a url, return its text"""
        cj = browser_cookie.chrome()

        try:
            r = requests.get(url, cookies=cj)
        except:
            print("Error Response for URL: %s" % url)

        return r.text




def for_url(urls, callback):

    for item in urls:
        uri = item[0]
        parameters = item[1]

        callback(uri, parameters)


def gen_urls(uri, params):

        if not params:
            return

        for key in params:
            params[key] = params[key][0]

        for key in params:
            oldValue = params[key]

            for case in check_list:
                params[key] = oldValue + case
                url = '?'.join([uri, urllib.urlencode(params)])
                url = "http://" + url
                params[key] = oldValue

                urls.append((url, case))
                #request_log(url, case)


if __name__ == "__main__":

    for_url(get_urls(), gen_urls)
    p = ThreadPool(request_log, urls, 30)
    p.start()

