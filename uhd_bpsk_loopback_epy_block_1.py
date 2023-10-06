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

    def __init__(self, delay=10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Add TX Time Tag',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.usrp = None
        self.sample_count = 0

        self.tx_time_out = "tx_time_out"
        self.reset = "reset"

        self.message_port_register_out(pmt.intern(self.tx_time_out ))
        self.message_port_register_in(pmt.intern(self.reset ))

        self.set_msg_handler(pmt.intern(self.reset), self.handle_rst_msg)

        self.delay = delay 

        self.tx_secs = 0
        self.tx_fracs = 0

        self.tx_time_set = False

    def handle_rst_msg(self, msg):
        reset_msg = pmt.to_python(msg)
        print (reset_msg)

        if self.tx_time_set and reset_msg[1] and reset_msg[0] == 'reset':
            self.tx_time_set = False

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        time = self.usrp.get_time_now()

        output_items[0][:] = input_items[0]

        if not self.tx_time_set:
            self.tx_secs = int(time.get_real_secs())+self.delay
            self.tx_fracs = time.get_real_secs() - int(time.get_real_secs())
            self.tx_time_set = True
            
            self.add_item_tag(0, self.sample_count, pmt.intern('tx_time'), pmt.to_pmt((self.tx_secs, self.tx_fracs)))

            #print (f"Tx time set to: {self.tx_secs + self.tx_fracs}")

            pmt_msg = pmt.to_pmt(('tx_time', self.tx_secs+self.tx_fracs))

            self.message_port_pub(pmt.intern(self.tx_time_out ), pmt_msg)
        
        # tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))

        # for tag in tagTuple:
        #     print ("Key: " + pmt.to_python(tag.key) + " " + str(tag.offset) + " " + str(tag.value))

        self.sample_count = self.sample_count + len(output_items[0])
        return len(output_items[0])
