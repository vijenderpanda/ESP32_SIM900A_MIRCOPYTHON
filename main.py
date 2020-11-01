## The file name needs to be renamed to main.py for it work on the ESP 32 board

import utime
from util import create_mqtt_client, get_telemetry_topic, get_c2d_topic, parse_connection
import ujson
from machine import Pin

start_motor = Pin(7, Pin.OUT)
stop_motor = Pin(8, Pin.OUT)
tx_pin = 4 #sim module connect to ESP tx pin no
rx_pin = 2 #sim module connect to ESP rx pin no

HOST_NAME = "HostName"
SHARED_ACCESS_KEY_NAME = "SharedAccessKeyName"
SHARED_ACCESS_KEY = "SharedAccessKey"
SHARED_ACCESS_SIGNATURE = "SharedAccessSignature"
DEVICE_ID = "DeviceId"
MODULE_ID = "ModuleId"
GATEWAY_HOST_NAME = "GatewayHostName"


## Parse the connection string into constituent parts
dict_keys = parse_connection("HostName=AgroHub.azure-devices.net;DeviceId=ESP32GSM;SharedAccessKey=Ss0B8++gPjvEoMeZ25bMzP85c30GhRqfmmvA+5CEvTM=")
shared_access_key = dict_keys.get(SHARED_ACCESS_KEY)
shared_access_key_name =  dict_keys.get(SHARED_ACCESS_KEY_NAME)
gateway_hostname = dict_keys.get(GATEWAY_HOST_NAME)
hostname = dict_keys.get(HOST_NAME)
device_id = dict_keys.get(DEVICE_ID)
module_id = dict_keys.get(MODULE_ID)



print(shared_access_key,"\n",shared_access_key_name,"\n",gateway_hostname,"\n",hostname)
## Create you own shared access signature from the connection string that you have
## Azure IoT Explorer can be used for this purpose.
sas_token_str = "SharedAccessSignature sr=AgroHub.azure-devices.net%2Fdevices%2FESP32GSM&sig=svPIW%2BG8EMjDOF0q1TTaZ%2FeURTxCtz2CBJXHpNG%2F4dA%3D&se=1639117699"

## Create username following the below format '<HOSTNAME>/<DEVICE_ID>'
username = hostname + '/' + device_id + '/?api-version=2018-06-30'


## Create UMQTT ROBUST or UMQTT SIMPLE CLIENT
mqtt_client = create_mqtt_client(client_id=device_id, hostname=hostname, username=username, password=sas_token_str, port=8883, keepalive=120, ssl=True)

print("connecting")
mqtt_client.reconnect()

def callback_handler(topic, message_receive):
    # Handle All subscriped topics including Direct method -----------
    if topic.startswith(b'$iothub/methods/POST/'):
        print("Received message with topic", topic)
        topic = topic.decode('utf-8').split('/')
        methodName = topic[3]
        rid = topic[4]
        msg = message_receive.decode()
        msg = ujson.loads(msg)
        response_topic = "$iothub/methods/res/200/"+rid
        if methodName =='start':
            print("Starting the Application")
            start_motor.value(1)
            stop_motor.value(0)
            mqtt_client.publish(topic=response_topic, msg=ujson.dumps("{'Status':'ok'}"))
        elif methodName == 'stop':
            print("Stopping the Motor")
            start_motor.value(0)
            stop_motor.value(1)
            mqtt_client.publish(topic=response_topic, msg=ujson.dumps("{'Status':'ok'}"))
            
        else:
            print("The Method name requested is " + methodName +"\n"+"Not Implemented any Action on ESP32 Module to handle Please check your method name")
            
            
        print("Payload is ---",msg)
    else:
        #Handle Normal Messages Form Iot HUb
        print("Received message with topic", topic)
        print(message_receive)




subscribe_topic = get_c2d_topic(device_id)
mqtt_client.set_callback(callback_handler)
mqtt_client.subscribe(topic=subscribe_topic)
mqtt_client.subscribe(topic="$iothub/methods/POST/#")
print("Publishing")
topic = get_telemetry_topic(device_id)


import boot
SSID = boot.SSID
PWD = boot.PWD
while True:
    try:
        msg = mqtt_client.check_msg()
        print("Waiting for commands from Iot HUB")
        utime.sleep(2)
    except:
        try:
            
            status = do_connect(SSID, PWD)
            if status:
                print("Wifi Conected")
        except:
            status = connectSIM(tx_pin,rx_pin)
            if status:
                print("Sim Network Connected")
      
                
            
            
