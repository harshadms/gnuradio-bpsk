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

    def __init__(self, samp_rate=1e6, pad_end=0, pad_start=0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Compare Timestamps',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.samp_rate = samp_rate
        self.sample_count = 0

        self.tx_time_in = "tx_time_in"
        self.reset = "reset"

        self.message_port_register_in(pmt.intern(self.tx_time_in))
        self.message_port_register_in(pmt.intern(self.reset))

        self.set_msg_handler(pmt.intern(self.tx_time_in), self.handle_msg)
        self.set_msg_handler(pmt.intern(self.reset), self.handle_rst_msg)

        self.tx_time_set = False
        self.rx_samp_count_set = False
        self.corr_time_set = False
        self.frac_set = False

        self.tx_time = []
        self.rx_time = 0

        self.pad_end = pad_end
        self.pad_start = pad_start
        
        with open("./rx_tx_timestamps.csv","w") as f:
            f.write("id,tx_time, rx_samp_count, corr_index, frac_sample, rx_time, dt\n")
	     
        self.id = 0

    def handle_msg(self, msg):
        tx_time = pmt.to_python(msg)
        if not self.tx_time_set:
            self.tx_time = tx_time[1] + (self.pad_start/self.samp_rate)
            self.tx_time_set = True
            # with open("./rx_tx_timestamps.csv","a") as f:
            #     f.write(f"{self.id},t,{self.tx_time}\n")

    def handle_rst_msg(self, msg):
        reset_msg = pmt.to_python(msg)
        
        if self.rx_samp_count_set and reset_msg[1] == 1 and reset_msg[0] == 'reset':
            self.rx_samp_count_set = False
            self.tx_time_set = False

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        
        self.sample_count = self.sample_count + len(input_items[0])
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))

        if not self.rx_samp_count_set:
            for tag in tagTuple:
                if pmt.to_python(tag.key) == "rx_samp_count" and not self.rx_samp_count_set:
                    self.rx_samp_count_set = True
                    self.rx_samp_count = pmt.to_double(tag.value)
            
                if pmt.to_python(tag.key) == "corr_index" and not self.corr_time_set:
                    self.corr_time_set = True                  
                    #self.corr_time = (pmt.to_double(tag.value) * 2)/ self.samp_rate
                    self.corr_time = pmt.to_double(tag.value)

                if pmt.to_python(tag.key) == "time_est3" and not self.frac_set:
                    self.frac_set = True
                    #self.corr_time = (pmt.to_double(tag.value) * 2)/ self.samp_rate
                    self.frac = pmt.to_double(tag.value)
            
            print (self.tx_time_set, self.corr_time_set, self.frac_set)

            if self.tx_time_set and self.corr_time_set and self.frac_set:
                with open("./rx_tx_timestamps.csv","a") as f:
                    self.rx_time = (self.rx_samp_count + self.corr_time + self.frac)/ 500e3 #self.rx_time - self.corr_time
                    f.write(f"{self.id},{self.tx_time},{self.rx_samp_count},{self.corr_time},{self.frac},{self.rx_time},{self.rx_time - self.tx_time}\n")
                    
                self.tx_time_set = False
                self.corr_time_set = False
                self.frac_set = False
                self.id = self.id + 1
            
        return len(input_items[0])

