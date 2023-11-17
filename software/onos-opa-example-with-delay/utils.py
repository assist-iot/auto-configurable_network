import base64
import json
import logging
import urllib3
from config import *

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
http = urllib3.PoolManager()


def authenticated_http_req(url, user, pwd, getPost):

    http = urllib3.PoolManager()
    headers = urllib3.make_headers(basic_auth=user+':'+pwd, accept_encoding='application/json')
    r = http.request(getPost, url, headers=headers)
    return r

  #  request = http.request('GET',url)
   # base64string = base64.encodestring('%s:%s' % (user, pwd)).replace('\n', '')
    #request.add_header('Authorization', 'Basic %s' % base64string)
    #return request


def json_get_req(url):
    try:
        http = urllib3.PoolManager()
        headers = urllib3.make_headers(basic_auth=ONOS_USER+':'+ONOS_PASS)
        request = http.request('GET', url, headers=headers)
        return json.loads(request.data)
    except IOError as e:
        logging.error(e)
        return ''

def json_delete_req(url):
    try:
        http = urllib3.PoolManager()
        headers = urllib3.make_headers(basic_auth=ONOS_USER+':'+ONOS_PASS)
        request = http.request('DELETE', url, headers=headers)
        return json.loads(request.data)
    except IOError as e:
        logging.error(e)
        return ''

def json_post_req(url, json_data):
    try:
        http = urllib3.PoolManager()
        headers = urllib3.make_headers(basic_auth=ONOS_USER+':'+ONOS_PASS)
        request = http.request('POST', url, headers=headers, body=json_data)
        
      #  request.add_header('Content-Type', 'application/json')
       # response = urllib3.urlopen(request, data=json_data)
        return json.loads(request.data)
    except IOError as e:
        logging.error(e)
        return ''


def bps_to_human_string(value, to_byte_per_second=False):
    if to_byte_per_second:
        value = value/8.0
        suffix = 'B/s'
    else:
        suffix = 'bps'

    for unit in ['', 'K', 'M', 'G']:
        if abs(value) < 1000.0:
            return '%3.1f %s%s' % (value, unit, suffix)
        value /= 1000.0
    return '%.1f %s%s' % (value, 'T', suffix)
