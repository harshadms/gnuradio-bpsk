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

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Py Message Parser',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.port_in = "data_in"
        self.message_port_register_in(pmt.intern(self.port_in ))
        self.set_msg_handler(pmt.intern(self.port_in), self.handle_msg)

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

    def handle_msg(self, msg):
        a = pmt.to_python(msg)
        chars = a[1]

        print (chars)
        
        string_ = []
        for i in chars:
            if i == 35:
                string_.append("<ETX>")
                break
            
            string_.append(chr(i))
        
        print (''.join(string_))
        
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        pass
