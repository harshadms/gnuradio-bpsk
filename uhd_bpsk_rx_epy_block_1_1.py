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
            name='Add RX Time Tag',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.usrp = usrp
        self.samp_time = 0
        self.sample_count = 0
        self.first_sample = False
        

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #time = self.usrp.get_time_now()
        #rx_time = time.get_real_secs()
        output_items[0][:] = input_items[0]
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))

        for tag in tagTuple:
            if pmt.to_python(tag.key) == "rx_time":
                self.frac_secs_samps = pmt.to_python(tag.value)[1] * 500e3
                self.first_sample = True

        if self.first_sample:
            self.samp_time = self.samp_time - self.frac_secs_samps
            self.first_sample = False
        
        self.add_item_tag(0, self.sample_count, pmt.intern('rx_samp_count'), pmt.to_pmt(self.samp_time))
	
        self.sample_count = self.sample_count + len(output_items[0])
        self.samp_time = self.samp_time + len(output_items[0])
        return len(output_items[0])
