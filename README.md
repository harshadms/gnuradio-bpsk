# GNURadio-BPSK TX/RX

### Instructions
* Install gnuradio - github.com/harshadms/gnuradio
* Generate hier flowgraphs. Open hier_* files in gnuradio and generate the flowgraph (F5). This will add 2 blocks packet_rx and packet_tx to the list of available blocks. (THIS IS A MUST)
* Loopback test: 
    1. Connect antennas to TX/RX and RX2 or connect these two ports with a cable and an attenuater (> 9dB)
    2. Execute ./loopback/uhd_bpsk_loopback.py in one terminal
    3. Execute ./zeromq_input.py in another terminal. Observe the received messages 
    
* Delayed transmission: Change the delay value in "Add TX Time Tag" block

### Directory Structure

1. ./rx - Contains all the standalone receiver files and flowgraphs
2. ./tx - Contains all the standalone transmitter files and flowgraphs
3. ./loopback - Files for a combined transmitter and receiver 
4. ./debug - Put debugging scripts. There is a jupyter notebook, mainly for used inspecting generated data and signal dumps.
5. ./misc - Random flowgraphs, can ignore

### Important files

1. ./zeromq_input.py - A python script to send a custom message to the transmitter. Transmitter then modulates the data and then transmits it using USRP Sink. By default it will accept any custom text via stdin. Alternatively you can also specify a repeat count like
``` python zeromq_input.py 10 ```
This will repeat the message "Testing-123456789" 10 times.



