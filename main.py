from multiprocessing import Process
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
import time
import threading
from Coffee import Coffee_handler
import datetime

class System:
    def __init__(self):
        # init queue
        self.queue = []

        # connect to broker
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1")

    def on_connect(self, client, userdata, flags, rc):
        print("[system] MQTT Connected with result code " + str(rc))
        self.client.subscribe("/XS001/SYSTEM")

    def on_message(self, client, userdata, msg):
        # print(msg.topic+" "+str(msg.payload))
        print("[system] msg_receiver push:", json.loads(msg.payload))
        self.queue.append(json.loads(msg.payload))

    def msg_receiver(self):
        self.client.loop_forever()

    def msg_send(self,topic,dict):
        msgs = \
            [
                {
                    'topic': topic,
                    'payload': json.dumps(dict)
                }
            ]
        publish.multiple(msgs, hostname="127.0.0.1")

if __name__ == '__main__':

    system = System()

    mr = threading.Thread(target=system.msg_receiver)
    mr.start()

    #multiprocess
    coffee_handler = Process(target=Coffee_handler)
    coffee_handler.start()
    coffee_handler.join


    request_list=[]

    time.sleep(1)
    # 1)edit the request format to msg what you want to test  (line 61 - 69)
    ####################### system send message #############################
    request = {
        'seq': str(datetime.datetime.now()),
        'cmd': 'stop',
        'par1': '',
        'par2': '',
        'par3': '',
        'par4': ''
    }
    system.msg_send('/XS001/COFFEE', request)
    #######################################################################

    while True:
        if (len(system.queue) > 0):
            system.queue.pop()