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




    def activateSimModule(self,tx_pin,rx_pin):
        try:
            self.GSM = UART(1, baudrate=9600, timeout=1000, rx=rx_pin, tx=tx_pin)

            self.logline('Waiting for AT command response...')
            self.atcmd('AT')
            self.atcmd('ATZ')
            time.sleep_ms(500)
            self.atcmd('ate0')
            self.atcmd('AT+CPIN?')
            self.atcmd('AT+CREG?')
            self.atcmd('AT+CNMI=0,0,0,0,0')
        except:
            print("Not Able to Connect to UART Please check your tx_pin or rx_pin nos")
            sys.exit()
            

        
        

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
