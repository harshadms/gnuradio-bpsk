#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Uhd Packet Tx
# GNU Radio version: v3.11.0.0git-489-g76831245

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq
from packet_tx import packet_tx  # grc-generated hier_block




class uhd_packet_tx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Uhd Packet Tx", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.samp_rate = samp_rate = 1e6
        self.rep = rep = 3
        self.rate = rate = 2
        self.polys = polys = [109, 79]
        self.nfilts = nfilts = 32
        self.k = k = 7
        self.eb = eb = 0.6
        self.Const_PLD = Const_PLD = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.Const_PLD.gen_soft_dec_lut(8)
        self.tx_rrc_taps = tx_rrc_taps = firdes.root_raised_cosine(nfilts, nfilts,1.0, eb, (11*sps*nfilts))
        self.tx_gain = tx_gain = 68
        self.taps = taps = firdes.root_raised_cosine(1.0,samp_rate,samp_rate/sps,eb,11*sps)
        self.pad_start = pad_start = 100
        self.pad_end = pad_end = 100
        self.hdr_format = hdr_format = digital.header_format_counter(digital.packet_utils.default_access_code, 3, Const_PLD.bits_per_symbol())
        self.freq = freq = 915
        self.enc_hdr = enc_hdr = fec.repetition_encoder_make(8000, rep)
        self.enc = enc = fec.cc_encoder_make(8000,k, rate, polys, 0, fec.CC_TERMINATED, False)
        self.amp = amp = 21.5
        self.Const_HDR = Const_HDR = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.Const_HDR.gen_soft_dec_lut(8)

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://127.0.0.1:1234', 100, False)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "serial=31BADAB")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            'packet_len',
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(freq * 1e6, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.packet_tx_0 = packet_tx(
            hdr_const=Const_HDR,
            hdr_enc=enc_hdr,
            hdr_format=hdr_format,
            pad_end=pad_end,
            pad_start=pad_start,
            pld_const=Const_PLD,
            pld_enc=enc,
            psf_taps=tx_rrc_taps,
            sps=sps,
        )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.6)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.packet_tx_0, 'in'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.packet_tx_0, 0), (self.blocks_multiply_const_vxx_0, 0))


    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_taps(firdes.root_raised_cosine(1.0,self.samp_rate,self.samp_rate/self.sps,self.eb,11*self.sps))
        self.set_tx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, (11*self.sps*self.nfilts)))
        self.packet_tx_0.set_sps(self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_taps(firdes.root_raised_cosine(1.0,self.samp_rate,self.samp_rate/self.sps,self.eb,11*self.sps))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_rep(self):
        return self.rep

    def set_rep(self, rep):
        self.rep = rep

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_tx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, (11*self.sps*self.nfilts)))

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_taps(firdes.root_raised_cosine(1.0,self.samp_rate,self.samp_rate/self.sps,self.eb,11*self.sps))
        self.set_tx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, (11*self.sps*self.nfilts)))

    def get_Const_PLD(self):
        return self.Const_PLD

    def set_Const_PLD(self, Const_PLD):
        self.Const_PLD = Const_PLD
        self.packet_tx_0.set_pld_const(self.Const_PLD)

    def get_tx_rrc_taps(self):
        return self.tx_rrc_taps

    def set_tx_rrc_taps(self, tx_rrc_taps):
        self.tx_rrc_taps = tx_rrc_taps
        self.packet_tx_0.set_psf_taps(self.tx_rrc_taps)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_pad_start(self):
        return self.pad_start

    def set_pad_start(self, pad_start):
        self.pad_start = pad_start
        self.packet_tx_0.set_pad_start(self.pad_start)

    def get_pad_end(self):
        return self.pad_end

    def set_pad_end(self, pad_end):
        self.pad_end = pad_end
        self.packet_tx_0.set_pad_end(self.pad_end)

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format
        self.packet_tx_0.set_hdr_format(self.hdr_format)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq * 1e6, 0)

    def get_enc_hdr(self):
        return self.enc_hdr

    def set_enc_hdr(self, enc_hdr):
        self.enc_hdr = enc_hdr
        self.packet_tx_0.set_hdr_enc(self.enc_hdr)

    def get_enc(self):
        return self.enc

    def set_enc(self, enc):
        self.enc = enc
        self.packet_tx_0.set_pld_enc(self.enc)

    def get_amp(self):
        return self.amp

    def set_amp(self, amp):
        self.amp = amp

    def get_Const_HDR(self):
        return self.Const_HDR

    def set_Const_HDR(self, Const_HDR):
        self.Const_HDR = Const_HDR
        self.packet_tx_0.set_hdr_const(self.Const_HDR)




def main(top_block_cls=uhd_packet_tx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
