#!/usr/bin/python
import evdev
import asyncio
import subprocess
from multiprocessing import Pool
from itertools import repeat
from time import sleep
import libtmux

last_event_time = 0
last_event_value = 0
#hyperdeck_ip_list = ["192.168.10.11", "192.168.10.12", "192.168.10.13", "192.168.10.21", "192.168.10.22", "192.168.10.23", "192.168.10.31", "192.168.10.32", "192.168.10.33", "192.168.10.41", "192.168.10.42",  "192.168.10.43"]
hyperdeck_ip_list = ["192.168.10.11", "192.168.10.12", "192.168.10.13", "192.168.10.31", "192.168.10.32", "192.168.10.33"]

#tmuxServer = None
#tmuxSession = None
#tmuxWindow = None

tmuxServer = libtmux.Server()
tmuxSession = tmuxServer.new_session(session_name="hypersession", kill_session=True, attach=False)
tmuxWindow = tmuxSession.new_window(attach=False, window_name="hyperwindow")


# returns path of gpio ir receiver device
def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.name == "gpio_ir_recv"):
            print("Using device", device.path, "\n")
            return device

    print("No device found!")
    sys.exit()

### UNUSED ###############################################################
def play_deck(hyperdeck_ip):
    command = "echo 'PLAY' | telnet {} 9993".format(hyperdeck_ip)
    subprocess.Popen(command, shell=True)

def rec_deck(hyperdeck_ip):
    command = "echo 'RECORD' | telnet {} 9993".format(hyperdeck_ip)
    subprocess.Popen(command, shell=True)

def stop_deck(hyperdeck_ip):
    command = "echo 'STOP' | telnet {} 9993".format(hyperdeck_ip)
    subprocess.Popen(command, shell=True)

def print_ips(hyperdeck_ip):
    command = "echo {}".format(hyperdeck_ip)
    subprocess.Popen(command, shell=True)
#########################################################################

def record_all():
    print("REC ALL")
    #pool = Pool()
    #pool.map(rec_deck,hyperdeck_ip_list)
    tmuxSession.attached_pane.send_keys('RECORD')
    tmuxSession.attached_pane.send_keys('C-m')

def play_all():
    print("PLAY ALL")
    #pool = Pool()
    #pool.map(play_deck, hyperdeck_ip_list)
    tmuxSession.attached_pane.send_keys('PLAY')
    tmuxSession.attached_pane.send_keys('C-m')

def stop_all():
    print("STOP ALL")
    #pool = Pool()
    #pool.map(stop_deck, hyperdeck_ip_list)
    tmuxSession.attached_pane.send_keys('STOP')
    tmuxSession.attached_pane.send_keys('C-m')

async def helper(dev):
    async for event in dev.async_read_loop():
        global last_event_time,last_event_value
        #print("event.sec = " + str(event.sec) + " / last_event_time = " + str(last_event_time))
        # check last time event to avoid capturing multi
        if (event.value != 0):  # AN EVENT 0 is TRIGGERED on RELEASE
          if (event.sec - last_event_time > 1) or (event.value != last_event_value):
            last_event_value=event.value
            last_event_time=event.sec
            print(repr(event.value))
            if(event.value == 69):
              record_all()
            elif (event.value == 70):
              stop_all()
            elif (event.value == 71):
              play_all()
            elif (event.value == 74):
                print("TODO : KILL EVERYTHING and EXIT nicely")

def init_tmux_session():
    ## ANOTHER WAY TO CREATE TMUX SESSION WITHOUT libtmux --> subprocess.Popen(['tmux', 'new', '-d', '-s', 'myName'])
    nbPanes = len(hyperdeck_ip_list)
    panesList = []
    for i in range(0, nbPanes):
        panesList.append(tmuxWindow.split_window(attach=False))
        tmuxWindow.select_layout('tiled')
        panesList[i].send_keys('telnet {} 9993'.format(hyperdeck_ip_list[i]))
    tmuxSession.set_option('synchronize-pane', True)
    tmuxSession.attached_pane.send_keys('C-d') # TO KILL FAILED TELNET SESSIONS
    tmuxSession.attached_pane.send_keys('C-m') # TO REMOVE PREVIOUS CTRL+D ANNOYING COMMAND IN TELNET SESSIONS (will display 'syntax error' but ok anyway)

 
def main():
    init_tmux_session()
    device = get_ir_device()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(helper(device))    
    print("Fini!")

if __name__ == "__main__":
    main()

