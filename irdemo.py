#!/usr/bin/python3
import evdev
import asyncio
import subprocess
from multiprocessing import Pool
from itertools import repeat
from time import sleep
import libtmux

last_event_time = 0
last_event_value = 0
hyperdeck_ip_list = ["192.168.10.11", "192.168.10.12", "192.168.10.13",
                     "192.168.10.21", "192.168.10.22", "192.168.10.23",
                     "192.168.10.31", "192.168.10.32", "192.168.10.33",
                     "192.168.10.41", "192.168.10.42", "192.168.10.43"]

tmuxServer = libtmux.Server()
tmuxSession = tmuxServer.new_session(
    session_name="hypersession", kill_session=True, attach=False)
tmuxWindow = tmuxSession.attached_window

# returns path of gpio ir receiver device
def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.name == "gpio_ir_recv"):
            print("Using device", device.path, "\n")
            return device

    print("No device found!")
    sys.exit()


def record_all():
    print("REC ALL")
    tmuxSession.attached_pane.send_keys('RECORD')
    tmuxSession.attached_pane.send_keys('C-m')


def play_all():
    print("PLAY ALL")
    tmuxSession.attached_pane.send_keys('PLAY')
    tmuxSession.attached_pane.send_keys('C-m')


def stop_all():
    print("STOP ALL")
    tmuxSession.attached_pane.send_keys('STOP')
    tmuxSession.attached_pane.send_keys('C-m')


async def helper(dev):
    async for event in dev.async_read_loop():
        global last_event_time, last_event_value
        if (event.value != 0):  # IGNORE EVENT 0 TRIGGERED ON RELEASE
            # REMOTES USUALLY SEND THE SAME SIGNAL MULTIPLE TIMES
            if (event.sec - last_event_time > 1) or (event.value != last_event_value):
                last_event_value = event.value
                last_event_time = event.sec
                print(repr(event.value))
                if (event.value == 69):
                    record_all()
                elif (event.value == 70):
                    stop_all()
                elif (event.value == 71):
                    play_all()
                elif (event.value == 74):
                    print("TODO : KILL EVERYTHING and EXIT nicely")


def init_tmux_session():
    nbPanes = len(hyperdeck_ip_list)
    panesList = []
    for i in range(0, nbPanes):
        panesList.append(tmuxWindow.split_window(attach=False))
        tmuxWindow.select_layout('tiled')
        panesList[i].send_keys('telnet {} 9993'.format(hyperdeck_ip_list[i]))
    tmuxSession.set_option('synchronize-pane', True)
    # TO CLOSE FAILED TELNET PANES:
    tmuxSession.attached_pane.send_keys('C-d')  
    # TO REMOVE PREVIOUS CTRL+D ANNOYING COMMAND IN ACTIVE TELNET PANES (will display 'syntax error' but ok anyway):
    tmuxSession.attached_pane.send_keys('C-m')


def main():
    init_tmux_session()
    device = get_ir_device()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(helper(device))
    print("Fini!")


if __name__ == "__main__":
    main()
