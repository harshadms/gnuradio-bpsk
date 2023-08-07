"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import pmt
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, usrp=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Compare Timestamps',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.usrp = usrp
        self.sample_count = 0

        self.tx_time_in = "tx_time_in"
        self.corr_est_in = "corr_est_in"

        self.message_port_register_in(pmt.intern(self.tx_time_in))
        self.message_port_register_in(pmt.intern(self.corr_est_in))

        self.set_msg_handler(pmt.intern(self.tx_time_in), self.handle_msg)
        self.set_msg_handler(pmt.intern(self.corr_est_in), self.handle_msg_ce)

        self.tx_time_set = False
        self.rx_time_set = False
        self.corr_est_set = False

        self.tx_time = []
        self.rx_time = []

    
    def handle_msg(self, msg):
        tx_time = pmt.to_python(msg)
        if not self.tx_time_set:
            #self.tx_time_set = True
            self.tx_time.append(tx_time[1])
            #print (f"Tx time: {self.tx_time}")
            with open("./rx_tx_timestamps.csv","a") as f:
                f.write(f"t,{tx_time[1]}\n")

    def handle_msg_ce(self, msg):
        tx_time = pmt.to_python(msg)
        if not self.corr_est_set:
            self.corr_est_set = True
            #print (f"Tx time: {self.tx_time}")
            with open("./rx_tx_timestamps.csv","a") as f:
                f.write(f"ce,{tx_time[1]}\n")

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        
        self.sample_count = self.sample_count + len(input_items[0])
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))

        if not self.rx_time_set:
            for tag in tagTuple:
                if pmt.to_python(tag.key) == "rx_time2":
                    self.rx_time_set = True
                    self.rx_time.append(pmt.to_double(tag.value))

                    with open("./rx_tx_timestamps.csv","a") as f:
                        f.write(f"r,{pmt.to_double(tag.value)}\n")

                    #print ("Key: " + pmt.to_python(tag.key) + " " + str(tag.offset) + " " + str(tag.value))
                    #rtt = self.rx_time - self.tx_time
                    #print (f"Rx time: {self.rx_time}")
                    #print (f"Tx time: {self.tx_time}")
                    #print (f"\n\nRTT: {rtt}s")


            
        return 0
