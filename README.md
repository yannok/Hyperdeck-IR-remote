# Hyperdeck-IR-remote
IR remote control of mutiple Blackmagic Hyperdeck recorders

This script has been designed to be able to start a recording on multiple Blackmagic Hyperdeck devices at the exact same moment using an infrared remote control. 
There must be less than one frame difference between the beginning of the recordings.

Using multithreading was not fulfilling the synchro requiements so the only solution found was the use of tmux panes, synchronize them all and launch the record commands in all panes at the same moment. That provides the correct solution. The commands to each Hyperdeck are sent through telnet on port 9993.

Once launched, the behaviour can be inspected by attaching to the mux session, from a terminal : <br>
<code>tmux a</code>

Requirements: python3, tmux, libtmux (pip)


<code>sudo apt install python3</code><br>
<code>sudo apt install tmux</code><br>
<code>pip3 install --user libtmux</code><br>

<b>Instructions:</b><br> 
-Change the IP of your hyperdecks accordingly (hyperdeck_ip_list)<br>
-Change the IR numbers according to your remote control (event.value == xx)<br>
To find out the values sent by your remote, use evtest 

launch from a terminal : <br>
<code>python3 irdemo.py</code>


