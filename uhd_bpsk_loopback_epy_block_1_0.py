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
            name='Add TX Time Tag',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.usrp = usrp
        self.set_tag_propagation_policy(gr.TPP_DONT)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        time = self.usrp.get_time_now()

        output_items[0][:] = input_items[0]
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tagTuple:
            print ("Key: " + pmt.to_python(tag.key) + " " + str(tag.offset) + " " + str(tag.value))

        return len(output_items[0])
