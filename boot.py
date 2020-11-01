## connect to wifi at boot time.
import network
from connectsim import SimClass

SSID = "PandaHome"
PWD = "123456789"



def do_connect(ssid, pwd):
    """
    To Connect to A Wifi Network
    Please Use Connect do_connect Method wih
    params : ssid -- Your Wifi SSID/Name
             pwd  -- Your Wifi Password

    """
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
    return sta_if.isconnected()
 



def wifiAP():
    """ To Create a Wifi HotSpot use this method
    """
    ssid = 'MicroPython-AP'
    password = '123456789'

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)

    while ap.active() == False:
      pass

    print('Connection successful')
    print(ap.ifconfig())
    return ap.isconnected()


def connectSIM():
    sim = SimClass()
    sim.activateSimModule()
    status = sim.connectGPRS()
    
    return status
    

# # do_connect(SSID, PWD)

# wifiAP()

import webrepl
webrepl.start()
