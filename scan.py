

from __future__ import print_function
import browser_cookie
import requests
import urllib
import os

from checks import CheckObj, getChecks

class Scan(object):
    """Scaning reflect XSS by a static way."""

    def __init__(self, checkObjs, requestFunc = None):
        """
        #   checkObjs:      [checkObj, checkObj, ...]       ->  list
        #   requestFunc:    request function                ->  function
        #
        #   in checkObjs:
        #       checkobj:   CheckObj type's object          ->  CheckObj
        """
        assert(isinstance(checkObjs, list))
        self.checkObjs = checkObjs

        self.ANCHER = CheckObj.getANCHER()

        logFileName = '/'.join([os.getcwd(), 'log.txt'])
        print("log file at %s" % logFileName)
        self.logFile = open(logFileName, 'a+')

        if requestFunc:
            self.request = requestFunc

    @staticmethod
    def request(url):
        """input a url, return its text"""
        cj = browser_cookie.chrome()

        try:
            r = requests.get(url, cookies=cj)
        except:
            print("Error Response for URL: %s" % url)

        return r.text

    def check_log(self, url, respText, obj):
        """ check one resp by one obj
        #   check the return text by obj.callback, if true log [url, obj.logMsg]
        #
        #   parameter:  respText    -> string
        #               obj         -> CheckObj
        """
        assert(isinstance(obj, CheckObj))
        callback = obj.callback
        logMsg = obj.logMsg

        def log(msg):
            self.logFile.write(' || '.join([url, logMsg, '\n']))

        if callback(respText):
            log(logMsg)


    def url_log(self, urlObj):
        """ check url by all checkObjs
        #   request url, check the return text by all checkObjs using check_log
        #
        #   parameter:  urlObj  -> (str, params)
        #
        #   in urlObj:
        #       str:        http://xx.com/xx                ->  string
        #       params:     {p1: p1_str, p2: p2_str, ...}   ->  dict
        """
        assert(isinstance(urlObj, tuple))
        url = urlObj[0]
        params = urlObj[1]

        insertStr = self.ANCHER[0]
        for obj in self.checkObjs:
            insertStr += obj.char
        insertStr += self.ANCHER[1]

        for item in params:
            oldValue = params[item]
            params[item] += insertStr

            requestUrl = '?'.join([url, urllib.urlencode(params)])
            text = requests.get(requestUrl).text
            for obj in self.checkObjs:
                self.check_log(requestUrl, text, obj)

            params[item] = oldValue

    def close(self):
        """close logFile"""
        self.logFile.close()



if __name__ == "__main__":

    scan = Scan(getChecks())
    urlObj = ("http://urltest.sinaapp.com/uxss/c.php", {'x': 'x'})
    scan.url_log(urlObj)
    scan.close()

