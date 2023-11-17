import json
import networkx as nx
from config import ONOS_IP, ONOS_PORT, VERBOSE
from utils import json_get_req, json_post_req, json_delete_req, bps_to_human_string
from pprint import pprint
from events.EventProcessor import EventProcessor
import logging
import io
import sys
import tensorflow as tf
import numpy as np
from flexnet_observation import Observation
import os, contextlib
import random


class IMRManager(object):
    def __init__(self, verbose=VERBOSE):
        self.intentKey_to_inOutElements = {}
        self.verbose = verbose
        self.retrieve_monitored_intents_from_ONOS()

        self.max_requested_band = {}
        self.intents_paths = {}
        self.current_paths = {}
        self.zero_count = {}

        self.new_model = tf.saved_model.load('/home/mich/Downloads/emu-230417/onos-opa-example-bez-loss/tf_model') #bylo po prostu 'tf_model'
        self.model = self.new_model.signatures["serving_default"]
        self.observer = Observation()

    def retrieve_monitored_intents_from_ONOS(self):
        logging.info("Retrieving Monitored Intents...")
        reply = json_get_req('http://%s:%d/onos/v1/imr/imr/monitoredIntents' % (ONOS_IP, ONOS_PORT))
        if 'response' not in reply:
            return
        for apps in reply['response']:
            for intent in apps['intents']:
#                if self.verbose:
                print("intent")
                print(intent)
                flow_id = (intent['key'], apps['id'], apps['name'])
                #if len(intent['inElements']) == 1 and len(intent['outElements']) == 1:
                index = intent['key'].find('None') + 4
                self.intentKey_to_inOutElements[flow_id] = (intent['key'][:index], intent['key'][index:])
                print(self.intentKey_to_inOutElements[flow_id])
                #else:
                #    print('Intent with multiple inElements/outElements are not currently supported :(')

    def get_monitored_intents(self):
        return set(self.intentKey_to_inOutElements.keys())

    def used_links(self,path,topo): #zwraca numery uzywanych linkow w danym pathie
        res = []
        index = 0
        for link in topo.edges(data=True):
            for i in range(1,len(path)-2):
                if link[0] == path[i] and link[1] == path[i+1]:
                    res.append(index)
            index += 1
        return res

    def get_mutual(self,path1,path2,topo):
        res = []
        index = 0
        for link in topo.edges(data=True):
            for i in range(len(path1)-1):
                for j in range(len(path2)-1):
                    if link[0] == path1[i] and link[1] == path1[i+1] and path1[i] == path2[j] and path1[i+1] == path2[j+1]:
                        res.append(index)
            index += 1
        return res

    def get_avg_flow(self, tm):
        avg_flow = 0
        avg_count = 0
        for flow_id, amount in tm.items():
            avg_flow += amount/1000
            avg_count += 1
        if avg_count > 0:
            avg_flow /= avg_count
        return max(100,avg_flow)

# MZ added
    def get_bandwidth_from_intent(self,intent_id):
        print(ONOS_IP)
        print(ONOS_PORT)
        print(intent_id[2])
        print(intent_id[0])
        reply = json_get_req('http://%s:%d/onos/v1/intents/%s/%s' % (ONOS_IP, ONOS_PORT, intent_id[2], intent_id[0]))
        print(reply)
        try:
            return reply['constraints'][0]['bandwidth']
        except:
            return None

    def reroute_monitored_intents(self, tm, topoManager):
        reroute_msg = {'routingList': []}

        topo = topoManager.G.copy()
        print(topo)
        print("to byla topo")
        for flow_id, amount in tm.items():
            if amount == 0.0 or random.random() < 0.5:
                continue
#            bw = self.get_bandwidth_from_intent(flow_id)
            amount /= 1000
            if flow_id not in self.max_requested_band:
                self.max_requested_band[flow_id] = amount
            
            self.max_requested_band[flow_id] = max(amount,self.max_requested_band[flow_id])
#            self.max_requested_band[flow_id] = bw
            assigned_bandwidth = self.max_requested_band[flow_id]/1000
            
            print("Amount: "+str(amount))
            print("Assigned: "+str(assigned_bandwidth))

            intent_key, app_id, app_name = flow_id
           
            in_elem, out_elem = self.intentKey_to_inOutElements[flow_id]
            #if self.verbose:
            print('\nFinding paths for demand %s -> %s' % (in_elem, out_elem))

            if self.verbose:
                for link in topo.edges(data=True):
                    print(link)           

            print("wew");
            print(self.intents_paths)
            if flow_id not in self.intents_paths:
                print("TU???")
                #with open(os.devnull, 'w') as devnull:
                #    with contextlib.redirect_stdout(devnull):
                while True:
                    try:
                        self.intents_paths[flow_id] = EventProcessor.process(topo, in_elem, out_elem, assigned_bandwidth)
                        break
                    except Exception as exp:
                        print("ggg")

                if self.verbose:
                    print('Found paths %s' % self.intents_paths[flow_id])
            #print(self.intents_paths)
            new_path = -1
            if flow_id not in self.current_paths:
                self.current_paths[flow_id] = 0
                new_path = 0

            if flow_id in self.intents_paths:
               current_path = self.current_paths[flow_id]
               
            tx_bandwidth = []
            links_capacity = []
            for link in topo.edges(data=True):
                tx_bandwidth.append(link[2]['used_bandwidth'])
                links_capacity.append(link[2]['bandwidth'])
            #print("info o flow")
            #print(flow_id)
            #print("part2")
            #print(self.intents_paths[flow_id])
            #print("koniec info o flow")
            #print(self.current_paths)
            #print("koniec info o current paths")
            #print(self.used_links())
            #print("koniec used links")
            ports_first = self.used_links(self.intents_paths[flow_id][self.current_paths[flow_id]],topo)
            ports_second = self.used_links(self.intents_paths[flow_id][(self.current_paths[flow_id]+1)%2],topo)
            order_bandwidth = assigned_bandwidth
            mutual = self.get_mutual(self.intents_paths[flow_id][0],self.intents_paths[flow_id][1],topo)

            max_bps = 0
            for port in ports_first:
                max_bps = max(max_bps,links_capacity[port])
            for port in ports_second:
                max_bps = max(max_bps,links_capacity[port])


            tx_bandwidth.append(amount)
            links_capacity.append(max_bps)
            end_port = len(tx_bandwidth) - 1
            #print(ports_first)
            #print("przerwa miedzy portami")
            #print(ports_second)

            obs = self.observer.get_all(np.array(tx_bandwidth)/max_bps, np.array(ports_first), np.array(ports_second), order_bandwidth, np.array(links_capacity), end_port, np.array(mutual), max_bps)
            q_values = self.model(observations = tf.constant([obs],dtype = tf.float32), is_training = tf.constant(False), timestep = tf.constant(0,dtype = tf.int64), prev_reward = tf.constant(1.), prev_action = tf.constant(0,dtype=tf.int64))['q_values']
            action = np.argmax(q_values)
             
            if action == 1:
               new_path = (self.current_paths[flow_id] + 1) % 2
               self.current_paths[flow_id] = new_path
#               print("new path: "+str(flow_id)+" "+str(new_path)+" "+str(amount))
               reroute_msg['routingList'].append({'key': intent_key, 'appId': {'id': app_id, 'name': app_name},'paths': [{'path': self.intents_paths[flow_id][new_path], 'weight': 1.0}]})

        #if self.verbose:
        logging.info('reroute_msg config:')
        pprint(reroute_msg)
        json_post_req(('http://%s:%d/onos/v1/imr/imr/reRouteIntents' % (ONOS_IP, ONOS_PORT)), json.dumps(reroute_msg))


def reduced_capacity_on_path(topo, amount, path):
    reduced_topo = topo.copy()
    for link in zip(path, path[1:]):
        if reduced_topo[link[0]][link[1]]['bandwidth'] - amount <= 0:
            reduced_topo.remove_edge(link[0], link[1])
        else:
            reduced_topo[link[0]][link[1]]['bandwidth'] -= amount
    return reduced_topo


# MZ modified
def reduced_capacity_topo(topo, amount):
    reduced_topo = topo.copy()
    to_delete = []
    for link in reduced_topo.edges(data=True):
        if link[2]['bandwidth'] - amount < 0:
            to_delete.append(link)
        else:
            link[2]['bandwidth'] -= amount
    for link in to_delete:
        reduced_topo.remove_edge(link[0],link[1])
    return reduced_topo
