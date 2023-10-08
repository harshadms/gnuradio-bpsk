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

    def __init__(self, display_value=False):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Tag Dump (Unique only)',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.tags = []
        self.display_value = display_value
        self.id = 0
    
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0]
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))

        for tag in tagTuple:
            if not pmt.to_python(tag.key) == "rx_samp_count": # not in self.tags:
                self.tags.append(pmt.to_python(tag.key))

                if self.display_value:
                    print (str(self.id) + ": Key: " + pmt.to_python(tag.key) + " " + str(tag.offset) + " " + str(tag.value))
                else:
                    print ("Key: " + pmt.to_python(tag.key))

                #rtt = self.rx_time - self.tx_time
                #print (f"Rx time: {self.rx_time}")
                #print (f"Tx time: {self.tx_time}")
                #print (f"\n\nRTT: {rtt}s")
        
        self.id = self.id + 1
        return len(output_items[0])
