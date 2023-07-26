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

import pmt
import zmq
import struct
import numpy as np

_debug = 0          # set to zero to turn off diagnostics

# create a PUSH socket
PROTOCOL = "tcp://"
SERVER = "127.0.0.1"          # localhost
PUSH_PORT = ":1234"
PUSH_ADDR = PROTOCOL + SERVER + PUSH_PORT

push_context = zmq.Context()
push_sock = push_context.socket (zmq.PUSH)
push_sock.bind(PUSH_ADDR)

while 1:
    ch = input("Enter message: ")

    if ch == 'q':
        break

    push_sock.send(pmt.serialize_str(pmt.cons(pmt.make_dict(), pmt.pmt_to_python.numpy_to_uvector(np.array([ord(c) for c in ch], np.uint8)))))
#push_sock.send(pmt.serialize_str(pmt.to_pmt(tab)))
