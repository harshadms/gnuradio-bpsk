#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: harshad
# GNU Radio version: v3.11.0.0git-489-g76831245

# zmq_PUSH_PULL_server.py

'''
 Packet payload 
 | 2 bytes addr | 46 bytes data - append 0s otherwise |
'''

import sys
import pmt
import zmq
import time
import numpy as np
from tqdm import trange
_debug = 0          # set to zero to turn off diagnostics

# create a PUSH socket
PUSH_BPSK_ADDR = "tcp://127.0.0.1:1234"
PUSH_STATS_CMD = "tcp://127.0.0.1:1237"

push_context = zmq.Context()
push_sock = push_context.socket (zmq.PUSH)
push_sock.bind(PUSH_BPSK_ADDR)

push_cmd_sock = push_context.socket (zmq.PUSH)
push_cmd_sock.bind(PUSH_STATS_CMD)

if len(sys.argv) == 1:
    repeat = True
    limit = 1
else:
    repeat = False
    limit = int(sys.argv[1])

cnt = 0
slp = 1

#while 1:

# Change address to any 16 bit integer (2 uint8 values)
addr = divmod(1, 1<<8)

if not repeat:
    for i in trange(limit):
        if not repeat:
            ch = "Testing-123456789"
            cnt = cnt + 1
        else:
            ch = input("Enter message: ")
        
        if ch == 'q':
            break
        
        
        vec = np.array([ord(c) for c in ch], np.uint8)
        
        # Add address
        vec = np.insert(vec, 0, addr)

        # ETX character
        vec = np.insert(vec, len(vec), 35)

        # Zero padding
        vec = np.insert(vec, len(vec), np.zeros(46-len(vec)))

        print (f"Sending: {vec}")

        push_sock.send(pmt.serialize_str(pmt.cons(pmt.make_dict(), pmt.pmt_to_python.numpy_to_uvector(vec))))

        time.sleep(1.1)
        
        push_cmd_sock.send(pmt.serialize_str(pmt.to_pmt(('reset',1))))

        #time.sleep(0.5)
        
        # if not repeat and cnt >= limit:
        #     break

        #slp = slp + 1
else:
    while 1:
        ch = input("Enter message: ")

        if ch == 'q':
            break
        
        ch = "Testing-123456789"

        vec = np.array([ord(c) for c in ch], np.uint8)
        
        # Add address
        vec = np.insert(vec, 0, addr)

        # ETX character
        vec = np.insert(vec, len(vec), 35)

        # Zero padding
        vec = np.insert(vec, len(vec), np.zeros(46-len(vec)))

        print (f"Sending: {vec}")

        push_sock.send(pmt.serialize_str(pmt.cons(pmt.make_dict(), pmt.pmt_to_python.numpy_to_uvector(vec))))

        time.sleep(1.1)
        
        push_cmd_sock.send(pmt.serialize_str(pmt.to_pmt(('reset',1))))
    
push_sock.close()

# Send status report message to receiver
push_cmd_sock.send(pmt.serialize_str(pmt.cons(pmt.make_dict(), pmt.pmt_to_python.numpy_to_uvector(np.array([np.uint8(1), np.uint8(limit)])))))
