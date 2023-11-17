import logReader
from time import sleep
import json
import logging
import urllib3

ONOS_USER = 'onos'
ONOS_PASS = 'rocks'


def json_get_req(url):
    try:
        http = urllib3.PoolManager()
        headers = urllib3.make_headers(basic_auth=ONOS_USER + ':' + ONOS_PASS)
        request = http.request('GET', url, headers=headers)
        return json.loads(request.data)
    except IOError as e:
        logging.error(e)
        return ''


def host_to_switch_translator():
    # print("Retrieving hosts...")
    host_switch_dict = {}
    hosts_reply = json_get_req('http://127.0.0.1:8181/onos/v1/hosts')
    for host in hosts_reply['hosts']:
        factors = host['ipAddresses'][0].split('.')
        host_name = "h" + factors[3]
        try:
            switch_name_tmp = int(host['locations'][0]['elementId'][3:])
            switch_name = "sw" + str(switch_name_tmp)
        except:
            switch_name = "sw0"

        # switche straca dodatkowe hosty, ale jeden host wystarczy do uzyskania delaya, wydajniej szukać po switchach
        host_switch_dict[switch_name] = host_name

    switches_list = []      # lista list, pod każdym indeksem jest lista portów jednego switcha
    swithes_reply = json_get_req('http://127.0.0.1:8181/onos/v1/devices')
    for switch in swithes_reply['devices']:
        switch_id = switch['id']
        # src_node = link['src']['device']

        switch_ports = json_get_req('http://127.0.0.1:8181/onos/v1/devices/%s/ports' % switch_id)
        switch_ports_list = []
        for port in switch_ports['ports']:
            switch_ports_list.append(port['annotations']['portName'])   # dodajemy porty pojedynczego switcha
        switches_list.append(switch_ports_list)

    # zwracamy pary host-switch oraz liste list z portami wszystkich switchy
    return host_switch_dict, switches_list


def links_finder():
    links_dict = {}
    reply = json_get_req('http://127.0.0.1:8181/onos/v1/links')
    src_losses = {}
    dst_losses = {}
    for link in reply['links']:
        src_node = link['src']['device']
        dst_node = link['dst']['device']
        src_port_number = link['src']['port']
        dst_port_number = link['dst']['port']

        src_switch_name = ''
        dst_switch_name = ''
        src_port = json_get_req('http://127.0.0.1:8181/onos/v1/devices/%s/ports' % src_node)
        for port in src_port['ports']:
            if port['port'] == src_port_number:
                src_switch_name = port['annotations']['portName']
        dst_port = json_get_req('http://127.0.0.1:8181/onos/v1/devices/%s/ports' % dst_node)
        for port in dst_port['ports']:
            if port['port'] == dst_port_number:
                dst_switch_name = port['annotations']['portName']

        links_dict[src_switch_name] = dst_switch_name   # wypełniamy słownik linków, każdy jest parą src_switch - dst_switch

    return links_dict


if __name__ == '__main__':
    host_switch_dict, switches_list = host_to_switch_translator()
    links_dict = links_finder()
    logReader.read_log_file("/home/mich/skrypty/pingLogs.txt", 100, host_switch_dict, switches_list, links_dict)
    # logReader.read_whole_log_file("/home/mich/skrypty/pingLogs.txt", host_switch_dict, switches_list, links_dict)
