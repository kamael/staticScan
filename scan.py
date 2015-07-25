

from __future__ import print_function
import _mysql
import browser_cookie
import requests
import json
import urllib

from pool import ThreadPool

def get_urls():

    db=_mysql.connect("10.125.8.217","1688sec","1688sec", "1688sec")
    db.query("""SELECT uri, parameter FROM url_process_record""")
    r = db.store_result()

    urls = []
    while True:
        item = r.fetch_row()
        if not item:
            break

        uri = item[0][0]
        try:
            params = json.loads(item[0][1])
        except:
            continue

        urls.append((uri, params))

    return urls

def for_url(urls, callback):

    for item in urls:
        uri = item[0]
        parameters = item[1]

        callback(uri, parameters)

f = open("a.txt", "a+")
def request_log(item):

    url = item[0]
    case = item[1]

    #print(url)
    cj = browser_cookie.chrome()
    try:
        r = requests.get(url, cookies=cj)
    except:
        #print("error:" + url)
        return

    try:
        if r.text and r.text.index(case) > -1:
            print("get:" + url)
            f.write(url + '\n')
        else:
            print("None")
    except:
        print(r.text)

check_list = ["<abbbbc"]
urls = []
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

