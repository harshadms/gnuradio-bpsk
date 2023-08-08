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

    def __init__(self, verbose=False):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Py Message Parser',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.data_in = "data_in"
        self.cmd_in = "cmd_in"
        
        self.message_port_register_in(pmt.intern(self.cmd_in ))
        self.message_port_register_in(pmt.intern(self.data_in ))

        self.set_msg_handler(pmt.intern(self.data_in), self.handle_data)
        self.set_msg_handler(pmt.intern(self.cmd_in), self.handle_cmd)

        self.verbose = verbose
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.cnt = 0

    def handle_data(self, msg):
        a = pmt.to_python(msg)

        
        chars = a[1]

        string_ = []
        for i in chars:
            if i == 35:
                if self.verbose:
                    print (chars)
                    string_.append("<ETX>")

                break
            
            string_.append(chr(i))
        
        string_ = ''.join(string_)

        if "Testing" in string_:
            self.cnt = self.cnt + 1

        if not self.verbose:
            string_ = string_.split("<ETX>")[0]

        print (f"Rx message: {string_}")
    
    def handle_cmd(self, msg):
        msg = pmt.to_python(msg)

    def handle_cmd(self, msg):
        msg = pmt.to_python(msg)
        
        try:
            cmd = msg[1][0]
            test = int(msg[1][1])
        except:
            return

        if cmd == 1:
            print ("Count = %d/%d" % (self.cnt, test))
            self.cnt = 0
                   

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        pass
