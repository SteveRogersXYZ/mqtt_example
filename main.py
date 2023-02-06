from multiprocessing import Process
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
import time
import threading

class Coffee():

    def __init__(self ):
        # [OFF]/[ON]/[READY]/[RUNNING]/[ERROR]/[STOPPED]
        self.status = 'OFF'
        self.connection = 'DISCONNECTED'

        self.queue = []
        # mqtt subscribe
        # create Client instance
        self.client = mqtt.Client()

        # connect to broker
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1")

    def cmd_to_mqtt(self,dict):
        msgs = \
            [
                {
                    'topic': "/XE/taskmanager/from_coffee",
                    'payload': json.dumps(dict)
                }
            ]
        return msgs

    def on_connect(self,client, userdata, flags, rc):
        print("[coffee] MQTT Connected with result code " + str(rc))
        self.client.subscribe("/XE/taskmanager/to_coffee")

    def on_message(self,client, userdata, msg):
        print("[coffee] msg_subscriber push: "+ str(json.loads(msg.payload)))
        self.queue.append(json.loads(msg.payload))

    def msg_subscriber(self):
        self.client.loop_forever()

    def get_status(self):
        #(!)
        #
        #
        #
        return self.status

    def connect(self):
        print("[coffee] CONNECTING")
        # (!)coffee()
        #
        #
        #
        print("[coffee] CONNECTED")
        self.connection = 'CONNECTED'

    def get_connection(self):
        #
        #
        #
        #
        return self.connection

    def disconnect(self):
        print("[coffee] DISCONNECTING")
        # (!)coffee()
        #
        #
        #
        print("[coffee] DISCONNECTED")
        self.connection = 'DISCONNECTED'

    def is_connected(self):
        if self.get_connection() == 'CONNECTED':
            return True
        else:
            return False

    def stop(self):
        print("[coffee] STOPPING")
        # (!)coffee()
        #
        #
        #
        print("[coffee] STOPPED")
        self.status = 'STOPPED'

    def is_stop(self):
        if self.get_status() == 'STOPPED':
            return True
        else:
            return False

    def initialize(self):
        print("[coffee] INITIALIZING")
        #(!)coffee()
        #
        #
        #
        print("[coffee] READY")
        self.status = 'READY'

    def is_ready(self):
        if self.get_status() == 'READY':
            return True
        else:
            return False

    def test(self,line):
        print("[coffee] TESTING: "+str(line))
        #(!)
        #
        #
        #
        print("[coffee] TEST FINISHED")

    def clean(self):
        print("[coffee] CLEANING")
        #(!)
        #
        #
        #
        print("[coffee] CLEAN FINISHED")

    def extract(self):
        print("[coffee] EXTRACTING")
        #(!)
        #
        #
        #
        print("[coffee] EXTRACTING FINISHED")


def Coffee_handler():

    cof =Coffee()
    sb = threading.Thread(target=cof.msg_subscriber)
    sb.start()

    while True:
        if len(cof.queue)>0:
            cmd = cof.queue.pop()
            if(cmd['cmd'] == 'stop'):
                cof.stop()
                dict = {
                    'rtn':'TRUE',
                    'dev':'cof',
                    'num': '1',
                    'err':'0000',
                    'msg': '',
                    'value':'',
                    'status':'ready'
                }
                publish.multiple(cof.cmd_to_mqtt(dict), hostname="127.0.0.1")


def on_connect(client, userdata, flags, rc):
    print("[task_manager] MQTT Connected with result code "+str(rc))
    client.subscribe("/XE/taskmanager/from_coffee")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print("[task_manager] msg_subscriber push: %s", json.loads(msg.payload))
    queue.append(json.loads(msg.payload))

def msg_subscriber():
    client.loop_forever()

def cmd_to_mqtt(dict):
    msgs = \
    [
        {
            'topic':"/XE/taskmanager/to_coffee",
            'payload': json.dumps(dict)
        }
    ]
    return msgs

if __name__ == '__main__':
    print('Created by stupid steve. 2023.02.06')

    #coffee_multi_process
    coffee = Process(target=Coffee_handler)
    coffee.start()
    coffee.join

    #task_manager
    client = mqtt.Client()
    # connect to broker
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1")

    queue = []

    #init_thread
    sb = threading.Thread(target=msg_subscriber)
    sb.start()

    dict = {
        'cmd': 'stop',
    }
    msgs = cmd_to_mqtt(dict)

    while True:
        time.sleep(1)
        print('')
        publish.multiple(msgs, hostname="127.0.0.1")

