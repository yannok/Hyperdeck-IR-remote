# Hyperdeck-IR-remote
IR remote control of mutiple Blackmagic Hyperdeck recorders

This script has been designed to be able to start a recording on multiple Blackmagic Hyperdeck devices at the exact same moment using an infrared remote control. 
There must be less than one frame difference between the beginning of the recordings.
Using multithreading was not fulfilling the requiements of launching the records exactly at the same moment so the only solution was to use tmux panes, synchronize them all and launch the record commands in all panes at the same moment. That provides the correct solution. The commands to each Hyperdeck are sent through telnet on port 9993.

Requirements: python3, tmux, libtmux (pip)

sudo apt install python3
sudo apt install tmux
pip3 install --user libtmux

Instructions: 
-Change the IP of your hyperdecks accordingly (hyperdeck_ip_list)
-Change the IR numbers according to your remote control (event.value == xx)
To find out the values sent by your remote, use evtest 




