## connect to wifi at boot time.
import network


def do_connect(ssid, pwd):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
 
# # This file is executed on every boot (including wake-boot from deepsleep)
# #import esp
# #esp.osdebug(None)
 



def wifiAP():
    ssid = 'MicroPython-AP'
    password = '123456789'

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)

    while ap.active() == False:
      pass

    print('Connection successful')
    print(ap.ifconfig())




# # Attempt to connect to WiFi network
# do_connect('Pandahome ff 2', 'Panda4875')
# do_connect('iOT DEPT', 'tksggn@1234')

wifiAP()

import webrepl
webrepl.start()