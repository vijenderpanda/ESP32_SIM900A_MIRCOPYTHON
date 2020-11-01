# import machine
# import sys
# import time


# try:
#     import usocket as _socket
# except:
#     import _socket
# try:
#     import ussl as ssl
# except:
#     import ssl

# DEBUG=True

# def logline(str):
#     if DEBUG:
#         print(str)

# def log(str):
#     sys.stdout.write(str)

# def connect():
#     from machine import UART

#     # GSM_PWR = machine.Pin(4, machine.Pin.OUT)
#     # GSM_RST = machine.Pin(5, machine.Pin.OUT)
#     # GSM_MODEM_PWR = machine.Pin(23, machine.Pin.OUT)

#     # GSM_PWR.value(0)
#     # GSM_RST.value(1)
#     # GSM_MODEM_PWR.value(1)

#     GSM = UART(1, baudrate=9600, timeout=1000, rx=4, tx=2)

#     GSM_APN = 'portalnmms'
#     logline('Waiting for AT command response...')
#     self.atcmd('AT', GSM)
#     self.atcmd('ATZ', GSM)
#     time.sleep_ms(500)
#     self.atcmd('ate0', GSM)
#     self.atcmd('AT+CPIN?', GSM)
#     self.atcmd('AT+CREG?', GSM)
#     self.atcmd('AT+CNMI=0,0,0,0,0', GSM)

#     logline("Connecting to GSM...")

#     self.atcmd('AT+CGDCONT=1,"IP","' + GSM_APN + '"', GSM)
#     self.atcmd('ATD*99***1#', GSM)

#     return connectGPRS(GSM)


# def self.atcmd(cmd, GSM, wait=500, tries=20):
#     GSM.write(cmd + '\r\n')
#     time.sleep_ms(wait)

#     for retry in range(tries):
#         resp = GSM.read()
#         if resp:
#             print(resp)
#             return resp
#         else:
#             log('.')
#             time.sleep_ms(wait)
#     else:
#         raise Exception("Modem not responding!")


# def connectGPRS(GSM):
#     import network
#     GPRS = network.PPP(GSM)
#     GPRS.active(True)
#     GPRS.connect()

#     for retry in range(20):

#         ret = GPRS.isconnected()

#         if ret:
#             break
#         else:
#             log('.')
#             time.sleep_ms(2000)
#     else:
#         raise Exception("Modem not responding!")

#     logline(GPRS.ifconfig())
#     return GPRS

# connect()
# print("Done")
DEBUG=True

import network
import machine
import sys
import time
from machine import UART,Pin
class SimClass:
    def __init__(self):
        try:
            import usocket as _socket
        except:
            import _socket
        try:
            import ussl as ssl
        except:
            import ssl
        self.gsmPW = Pin(21,Pin.OUT)
        self.gsmPW.value(0)
        time.sleep(6)
    
    def logline(self,str):
        if DEBUG:
            print(str)

    def log(self,str):
        sys.stdout.write(str)




    def activateSimModule(self):
        self.GSM = UART(1, baudrate=9600, timeout=1000, rx=4, tx=2)
        
        self.logline('Waiting for AT command response...')
        self.atcmd('AT')
        self.atcmd('ATZ')
        time.sleep_ms(500)
        self.atcmd('ate0')
        self.atcmd('AT+CPIN?')
        self.atcmd('AT+CREG?')
        self.atcmd('AT+CNMI=0,0,0,0,0')

        
        

    def atcmd(self,cmd, wait=500, tries=20):
        self.GSM.write(cmd + '\r\n')
        time.sleep_ms(wait)

        for retry in range(tries):
            resp = self.GSM.read()
            if resp:
                print(resp)
                return resp
            else:
                self.log('.')
                time.sleep_ms(wait)
        else:
            raise Exception("Modem not responding!")


    def connectGPRS(self):
        GSM_APN = 'portalnmms'
        self.logline("Connecting to GSM...")
        self.atcmd('AT+CGDCONT=1,"IP","' + GSM_APN + '"')
        self.atcmd('ATD*99***1#')
        self.GPRS = network.PPP(self.GSM)
        self.GPRS.active(True)
        self.GPRS.connect()

        for retry in range(20):
            ret = self.GPRS.isconnected()
            if ret:
                break
            else:
                self.log('.')
                time.sleep_ms(2000)
        else:
            raise Exception("Modem not responding!")

        self.logline(self.GPRS.ifconfig())
        return self.GPRS

    def disconnectatcmd(self,cmd):
        self.GSM.write(cmd + '\r\n')
        return True


    def disconnectGPRS(self,wait=500, tries=5):
        self.gsmPW.value(1)
        return True



class UseSIM:
    def __init__(self):
        try:
            import usocket as _socket
        except:
            import _socket
        try:
            import ussl as ssl
        except:
            import ssl
        self.gsmPW = Pin(21,Pin.OUT)
        self.gsmPW.value(0)
        time.sleep(6)
    
    def logline(self,str):
        if DEBUG:
            print(str)

    def log(self,str):
        sys.stdout.write(str)
    
    def atcmd(self,cmd, wait=500, tries=20):
        self.GSM.write(cmd + '\r\n')
        time.sleep_ms(wait)

        for retry in range(tries):
            resp = self.GSM.read()
            if resp:
                print(resp)
                if not resp == b'\r\nNO CARRIER\r\n':
                    return resp
            else:
                self.log('.')
                time.sleep_ms(wait)
        else:
            raise Exception("Modem not responding!")


    def callMobile(self):
        time.sleep(5)
        self.GSM = UART(1, baudrate=9600, timeout=1000, rx=4, tx=2)
        
        self.logline('Waiting for AT command response...')
        self.atcmd('AT')
        self.atcmd('ATZ')
        time.sleep_ms(500)
        self.atcmd('ate0')
        self.atcmd('AT+CPIN?')
        self.atcmd('AT+CREG?')
        self.atcmd('AT+COPS?')
        self.atcmd('ATD7710988033i;')
        while True:
            resp = self.GSM.readline()
            print(resp)
            time.sleep(1)

        return self.GSM
