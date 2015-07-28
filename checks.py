

import re


class CheckObj(object):
    """check object for a type of XSS vul char"""
    def __init__(self, char, callback, logMsg):
        self.char = char
        self.callback = callback
        self.logMsg = logMsg

    @staticmethod
    def getANCHER():
        return ('wlstrt', 'wke')


def gen_easy_find(char, text):
    r = "(.*?)".join(CheckObj.getANCHER())
    result = re.findall(r, text, re.S)
    for item in result:
        if item and item.find(char) > -1:
            return True
    return False

def check3c(text):
    return gen_easy_find('<', text)

def check22(text):
    return gen_easy_find('"', text)

def check27(text):
    return gen_easy_find('\'', text)

def check0a(text):
    return gen_easy_find(chr(0x0a), text)

def getChecks():
    """get all checkObjs"""
    objs = []
    objs.append(CheckObj('<', check3c, "check <"))
    objs.append(CheckObj('"', check22, "check \""))
    objs.append(CheckObj('\'', check27, "check '"))
    objs.append(CheckObj('%0a', check0a, "check \n"))

    return objs




