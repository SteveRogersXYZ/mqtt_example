from multiprocessing import Process
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
import time
import threading

class Coffee():
    def __init__(self):
        # init queue
        self.queue = []

        # connect to broker
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1")

    #subscribe topic
    def on_connect(self, client, userdata, flags, rc):
        print("[coffee_handler] MQTT Connected with result code "+str(rc))
        self.client.subscribe("/XS001/COFFEE")

    #statements executed in func [client.loop_forever()]
    def on_message(self, client, userdata, msg):
        #2) handler receive message
        ####################### handler receive message #############################
        print("[coffee_handler] msg_receiver push:", json.loads(msg.payload))
        self.queue.append(json.loads(msg.payload))
        #############################################################################

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

def Coffee_handler():

    #init
    coffee = Coffee()

    #init thread
    mr = threading.Thread(target=coffee.msg_receiver)
    mr.start()

    while True:
        time.sleep(1)
        if(len(coffee.queue)>0):
            request = coffee.queue.pop()
            #3)edit here! Execute the appriate function according to cmd and parmeters
            ####################### handler process #############################
            if(request["cmd"]=='get_status'):
                pass
            elif (request["cmd"] == 'connect'):
                pass
            elif (request["cmd"] == 'get_connection'):
                pass
            elif (request["cmd"] == 'disconnect'):
                pass
            elif (request["cmd"] == 'is_connected'):
                pass
            elif(request["cmd"]=='stop'):
                #rtn = func()
                #4)make response message from result of your function
                ####################### handler send message #######################
                response = {
                    'seq': request["seq"], #(same sqe with the request msg)
                    'type':'response',     #event/response
                    'cmd': request["cmd"], #command (same cmd with the request msg)
                    'dev': request["dev"], #device code
                    'num': request["num"], #device number
                    'code':'',             #error code
                    'msg':'',              #error message
                    'value':'',            #if the cmd need 'return value'
                    'status':'STOPPED'     #status
                }
                coffee.msg_send('/XS001/SYSTEM', response)
                ####################################################################
            elif(request["cmd"]=='is_stop'):
                pass
            elif(request["cmd"]=='initialize'):
                pass
            elif(request["cmd"]=='is_ready'):
                pass
            elif(request["cmd"]=='test'):
                pass
            elif(request["cmd"]=='clean'):
                pass
            elif(request["cmd"]=='get_error'):
                pass
            elif(request["cmd"]=='extract'):
                pass
            else:
                pass
            ####################################################################