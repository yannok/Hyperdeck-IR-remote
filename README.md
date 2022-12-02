# Hyperdeck-IR-remote
IR remote control of mutiple Blackmagic Hyperdeck recorders

This script has been designed to be able to start a recording on multiple Blackmagic Hyperdeck devices at the same moment
Hyperdecks are controled with telnet on port 9993

Using multithread was not laucnhing the records exactly at the same moment so the only solution was to use tmux panes, synchronize them all and launch the record
commands in all panes at the same moment. That provides the correct solution.

Requirements: 
tmux installed on the system
libtmux installed by pip


Change the IP of your hyperdecks accordingly (of course)
Change the IR numbers according to your remote control

