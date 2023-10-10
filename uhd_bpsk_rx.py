#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: gfe42f6a4a

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import digital
from gnuradio import fec
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from packet_rx import packet_rx  # grc-generated hier_block
import math
import uhd_bpsk_rx_epy_block_0 as epy_block_0  # embedded python block
import uhd_bpsk_rx_epy_block_1_1 as epy_block_1_1  # embedded python block



class uhd_bpsk_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "uhd_bpsk_rx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.Const_PLD = Const_PLD = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.Const_PLD.set_npwr(1.0)
        self.Const_PLD.gen_soft_dec_lut(8)
        self.sps = sps = 4
        self.samp_rate = samp_rate = 0.5e6
        self.rep = rep = 3
        self.rate = rate = 2
        self.polys = polys = [109, 79]
        self.nfilts = nfilts = 32
        self.k = k = 7
        self.hdr_format = hdr_format = digital.header_format_counter(digital.packet_utils.default_access_code, 3, Const_PLD.bits_per_symbol())
        self.eb = eb = 0.6
        self.rx_rrc_taps = rx_rrc_taps = firdes.root_raised_cosine(nfilts, nfilts*samp_rate,samp_rate / sps, eb, (11*sps*nfilts))
        self.rx_gain = rx_gain = 31
        self.pfs = pfs = sps*2+1
        self.lb = lb = 2*math.pi/sps/100
        self.frf = frf = eb
        self.freq = freq = 915
        self.dec_hdr = dec_hdr = fec.repetition_decoder.make(hdr_format.header_nbits(),rep, 0.5)
        self.dec = dec = fec.cc_decoder.make(8000,k, rate, polys, 0, (-1), fec.CC_TERMINATED, False)
        self.amp = amp = 21.5
        self.Const_HDR = Const_HDR = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.Const_HDR.set_npwr(1.0)
        self.Const_HDR.gen_soft_dec_lut(8)

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "serial=31EABEA")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        _last_pps_time = self.uhd_usrp_source_0.get_time_last_pps().get_real_secs()
        # Poll get_time_last_pps() every 50 ms until a change is seen
        while(self.uhd_usrp_source_0.get_time_last_pps().get_real_secs() == _last_pps_time):
            time.sleep(0.05)
        # Set the time to PC time on next PPS
        self.uhd_usrp_source_0.set_time_next_pps(uhd.time_spec(int(time.time()) + 1.0))
        # Sleep 1 second to ensure next PPS has come
        time.sleep(1)

        self.uhd_usrp_source_0.set_center_freq(freq*1e6, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_rx_agc(True, 0)
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                2,
                samp_rate,
                (samp_rate/sps),
                eb,
                (11*sps)))
        self.packet_rx_0 = packet_rx(
            eb=eb,
            hdr_const=Const_HDR,
            hdr_dec=dec_hdr,
            hdr_format=hdr_format,
            pld_const=Const_PLD,
            pld_dec=dec,
            psf_taps=rx_rrc_taps,
            sps=sps,
        )
        self.epy_block_1_1 = epy_block_1_1.blk(usrp=0)
        self.epy_block_0 = epy_block_0.blk(verbose=False, addr=1)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, frf, pfs, lb)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.packet_rx_0, 'precrc'), (self.epy_block_0, 'data_in'))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.epy_block_1_1, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.packet_rx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.epy_block_1_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "uhd_bpsk_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_Const_PLD(self):
        return self.Const_PLD

    def set_Const_PLD(self, Const_PLD):
        self.Const_PLD = Const_PLD
        self.packet_rx_0.set_pld_const(self.Const_PLD)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_lb(2*math.pi/self.sps/100)
        self.set_pfs(self.sps*2+1)
        self.set_rx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate / self.sps, self.eb, (11*self.sps*self.nfilts)))
        self.packet_rx_0.set_sps(self.sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(2, self.samp_rate, (self.samp_rate/self.sps), self.eb, (11*self.sps)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate / self.sps, self.eb, (11*self.sps*self.nfilts)))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(2, self.samp_rate, (self.samp_rate/self.sps), self.eb, (11*self.sps)))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

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
        self.set_rx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate / self.sps, self.eb, (11*self.sps*self.nfilts)))

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format
        self.packet_rx_0.set_hdr_format(self.hdr_format)

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_frf(self.eb)
        self.set_rx_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate / self.sps, self.eb, (11*self.sps*self.nfilts)))
        self.packet_rx_0.set_eb(self.eb)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(2, self.samp_rate, (self.samp_rate/self.sps), self.eb, (11*self.sps)))

    def get_rx_rrc_taps(self):
        return self.rx_rrc_taps

    def set_rx_rrc_taps(self, rx_rrc_taps):
        self.rx_rrc_taps = rx_rrc_taps
        self.packet_rx_0.set_psf_taps(self.rx_rrc_taps)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_pfs(self):
        return self.pfs

    def set_pfs(self, pfs):
        self.pfs = pfs

    def get_lb(self):
        return self.lb

    def set_lb(self, lb):
        self.lb = lb
        self.digital_fll_band_edge_cc_0.set_loop_bandwidth(self.lb)

    def get_frf(self):
        return self.frf

    def set_frf(self, frf):
        self.frf = frf

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq*1e6, 0)

    def get_dec_hdr(self):
        return self.dec_hdr

    def set_dec_hdr(self, dec_hdr):
        self.dec_hdr = dec_hdr
        self.packet_rx_0.set_hdr_dec(self.dec_hdr)

    def get_dec(self):
        return self.dec

    def set_dec(self, dec):
        self.dec = dec
        self.packet_rx_0.set_pld_dec(self.dec)

    def get_amp(self):
        return self.amp

    def set_amp(self, amp):
        self.amp = amp

    def get_Const_HDR(self):
        return self.Const_HDR

    def set_Const_HDR(self, Const_HDR):
        self.Const_HDR = Const_HDR
        self.packet_rx_0.set_hdr_const(self.Const_HDR)




def main(top_block_cls=uhd_bpsk_rx, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
