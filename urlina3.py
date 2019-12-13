#!/usr/bin/env python3

#--------------------------------------------------------------------------------
def main():
    read_param()
    reqs = test_params()
    test_url(reqs)
    exit(0)
#--------------------------------------------------------------------------------
def usage():
    print("""Usage:
	%s -h|--help	Get help.

	%s <file> [-s] [-c] [-r] [-d] [-txx]
        <file>      YAML file with a list of testing URLs
        -s          Skip not matching a status codes
        -c          Check SSL validation
        -r          Add "Rederer" header as testing URL
        -d          Debug mode.
        -txx        Timeout of requests. Default: 10 (sec), min: 1 (sec), max: 3600 (sec)

Format of a YAML file:
---
urls:
  - url: <Full URL address. Example: https://yandex.ru/search?text=123456780&clid=2186621>
    code: <A comparing status code. Default: 200>
    method: <A requiest method. Default: GET>
""" % (argv[0], argv[0]))
    exit(0)
#--------------------------------------------------------------------------------
def read_param():
    global data
    global debug
    global verify
    global ignore
    global timeout
    global referer
    debug = True if '-d' in argv else False
    ignore = True if '-s' in argv else False
    verify = True if '-c' in argv else False
    referer = True if '-r' in argv else False
    if debug:
        print("Incoming params:")
        for arg in argv: print("\t%s" % arg)
        print("----------------\n")
    if len(argv) < 2:
        print("Error: Incomming parameters.\nTry %s -h.\n" % argv[0])
        exit(1)
    if argv[1] in ['-h','--help']:
        usage()
    file = argv[1]
    if not isfile(file):
        print("Error: File '%s' not found.\nTry %s -h.\n" % (file, argv[0]))
        exit(1)
    timeout = 10
    for arg in argv:
        if arg == argv[0]: continue
        if arg.startswith('-t'):
            timeout = arg.replace('-t', '')
    try:
        timeout = int(timeout)
    except Exception as exc:
        print("Error: Wrong parameter '-t' ('%s')\nTry %s -h.\n" % (str(timeout), argv[0]))
        if debug: print("[%s: %s]" % (type(exc).__name__, str(exc)))
        exit(1)
    if timeout > 3600 or timeout < 1:
        print("Error: Wrong parameter '-t' ('%s')\nTry %s -h.\n" % (str(timeout), argv[0]))
        exit(1)
    try:
        data = load(open(file).read(), Loader=BaseLoader)
    except Exception as exc:
        print("Error: File '%s' not exist or invalid.\nTry %s -h.\n" % (file, argv[0]))
        if debug: print("[%s: %s]" % (type(exc).__name__, str(exc)))
        exit(1)
    if debug:
        print("Readed:")
        print("  - http timeout:         %i" % timeout)
        print("  - cert check:           %s" % str(verify))
        print("  - ignore code mismatch: %s" % str(ignore))
        print("  - add referer:          %s" % str(referer))
        print("  - file:                 %s" % file)
        print("data:\n%s\n" % str(data))
        print("---------")
    return
#--------------------------------------------------------------------------------
def test_params():
    if not 'urls' in data.keys() or type(data['urls']).__name__ != 'list':
        print("Error: Wrong data format.\nTry %s -h.\n" % argv[0])
        exit(1)
    reqs = []
    for chk in data['urls']:
        if not 'code' in chk.keys(): chk['code'] = '200'
        else: chk['code'] = str(chk['code'])
        if not 'method' in chk.keys(): chk['method'] = 'GET'
        else: chk['method'] = str(chk['method'])
        if not 'url' in chk.keys():
            print("Error: Address is required.\nTry %s -h.\n" % argv[0])
            exit(1)
        else: chk['url'] = str(chk['url'])
        if not chk['url'].lower().startswith('http://') and not chk['url'].lower().startswith('https://'):
            print("Error: Address need to start with 'http://' or 'https://'\nTry %s -h.\n" % argv[0])
            exit(1)
        reqs.append(chk)
    return reqs
#--------------------------------------------------------------------------------
def test_url(reqs):
    print("Checking...")
    print("Status\tMethod\tCode\tComparing code\tAddress")
    for req in reqs:
        if debug:
            print("Processing: %s" % str(req))
        if referer:
            headers['Referer'] = req['url']
        try:
            response = requests.request(req['method'], req['url'], headers=headers, verify=verify, timeout=timeout)
        except Exceptions as exc:
            if not ignore:
                print("Error of execution of request. Exiting...")
                if debug: print("[%s: %s]" % (type(exc).__name__, str(exc)))
                exit(1)
            else:
                print("ERROR\tError of execution of request for '%s'." % req['url'])
                if debug: print("[%s: %s]" % (type(exc).__name__, str(exc)))
        if str(response.status_code) != str(req['code']):
            if not ignore:
                print("Error: real and expected status code do not match (%s != %s) for %s::%s\nTry %s -h?\n" % (req['code'], str(response.status_code), req['method'], req['url']))
                exit(1)
            print("FAIL\t%s\t%s\t%s\t\t%s" % (req['method'], response.status_code, req['code'], req['url'])) # error
        else:
            print("OK\t%s\t%s\t%s\t\t%s" % (req['method'], response.status_code, req['code'], req['url'])) # ok
        if debug:
            print("\nRequest Headers:")
            for key in headers.keys(): print("\t%s:\t%s" % (key, headers[key]))
            print("\nAnswer Headers:")
            for key in response.headers.keys(): print("\t%s:\t%s" % (key, response.headers[key]))
    print("Done.")
    return
#--------------------------------------------------------------------------------
from os.path import isfile
from sys import argv, exit
from yaml import load, BaseLoader
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#--------------------------------------------------------------------------------
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}
if __name__ == "__main__":
    main()
