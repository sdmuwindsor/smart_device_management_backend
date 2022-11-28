import paho.mqtt.client as mqtt
import json
import os
import time
import logging,random,os
import sys,getopt
import threading

brokers=["test.mosquitto.org"]

class mqtt_connection:
    brokers=["test.mosquitto.org"]
    N=0
    connected_topics = []
    sensor_status_topics = []
    control_topics = []
    device_id = []
    disconnect_flag = []
    connection_thread_list = []
    
    def __init__(self,deviceId,sensorType,states):
        mqtt_connection.device_id.append(deviceId)
        self.mqtt_connection_id = mqtt_connection.N
        mqtt_connection.N+=1
        
        options=dict()
        options["broker"]=mqtt_connection.brokers[0]
        options["port"]=1883
        options["verbose"]=False
        options["username"]=""
        options["password"]=""
        options["cname"]="device_"+str(deviceId)
        options["sensor_type"]=sensorType
        options["topic_base"]="sensors"
        options["interval"]=2 #loop time when sensor publishes in verbose
        options["interval_pub"]=60 # in non chatty mode publish
        options["keepalive"]=120
        options["loglevel"]=logging.ERROR
        options["mqttclient_log"] = False
        options["sensor_pub_interval"] = 60
        options["QOS0"]=0

        self.connected_topic = options["sensor_type"]+"/connected/"+options["cname"]
        self.sensor_status_topic=options["sensor_type"]+"/"+options["cname"]
        self.topic_control=self.sensor_status_topic+"/control"
        mqtt_connection.connected_topics.append(self.connected_topic)
        mqtt_connection.sensor_status_topics.append(self.sensor_status_topic)
        mqtt_connection.control_topics.append(self.topic_control)
        
        options["topics"]=[(self.topic_control,0)]
        options["states"]=states
        self.options = options
        mqtt_connection.disconnect_flag.append(True)
        
    def establish_connection(self):
        mqtt.Client.last_pub_time=time.time()
        mqtt.Client.topic_ack=[] 
        mqtt.Client.run_flag=True
        mqtt.Client.subscribe_flag=False
        mqtt.Client.sensor_status=1
        mqtt.Client.sensor_status_old=None
        mqtt.Client.bad_connection_flag=False
        mqtt.Client.connected_flag=False
        mqtt.Client.disconnect_flag=False
        mqtt.Client.disconnect_time=0.0
        mqtt.Client.disconnect_flagset=False
        mqtt.Client.pub_msg_count=0

        self.client = mqtt.Client(self.options['cname'])
        self.client.on_connect = self.on_connect        #attach function to callback
        self.client.on_message = self.on_message        #attach function to callback
        self.client.on_disconnect = self.on_disconnect  #attach function to callback
        self.client.will_set(self.connected_topic, 0, qos=0, retain=True) #set will
        mqtt_connection.disconnect_flag[self.mqtt_connection_id]=False
        
        self.start_flag=True #used to always publish when starting
        run_flag=True
        bad_conn_count=0
        while run_flag:
            self.client.loop(0.05)
            if not self.client.connected_flag:
                if self.Connect(self.client,self.options["broker"],self.options["port"],self.options["keepalive"],run_forever=True) !=-1:
                    if not self.wait_for(self.client,"CONNACK"):
                        run_flag=False #break
                else:
                    run_flag=False #break
            #subbscribes to control in on_connect calback

            if self.client.connected_flag:
                self.publish_status(self.client)
            if mqtt_connection.disconnect_flag[self.mqtt_connection_id]:
                break
        if self.client.connected_flag:
            self.client.publish(self.connected_topic,0,retain=True)
            time.sleep(1)
            self.client.disconnect()
    
    def connect_sensor(self):
        t = threading.Thread(target=self.establish_connection, args=())
        t.start()
        mqtt_connection.connection_thread_list.append(t)

    @staticmethod
    def disconnect_sensor(deviceId):
        for i in range(mqtt_connection.N):
            if mqtt_connection.device_id[i]==deviceId:
                if mqtt_connection.disconnect_flag[i]:
                    print("device with Id",deviceId,"was disconnected")
                    break
                mqtt_connection.disconnect_flag[i]=True
                mqtt_connection.connection_thread_list[i].join()
                print("device with Id",deviceId,"disconnected successfully")
                break

    def check_sensor_connection_status(self):
        return mqtt_connection.connection_thread_list[self.mqtt_connection_id].is_alive()
        # for i in range(mqtt_connection.N):
        #     if not mqtt_connection.connection_thread_list[i].is_alive():
        #         print("device with Id",mqtt_connection.device_id[i],"is not connected")
        #     else:
        #         print("device with Id",mqtt_connection.device_id[i],"is connected")

    def update_sensor_state(self, value):
        if value in self.options['states']:
            self.client.sensor_status = value

    def get_state(self):
        return self.client.sensor_status

    def on_message(self, client, userdata, msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore")).split('.')[0]
        logging.debug("Message Received "+m_decode)
        self.message_handler(client, m_decode, topic)

    def message_handler(self, client, msg, topic):
        if topic==self.topic_control: #got control message
            print("control message ",msg)
            self.update_status(client, msg)

    def on_connect(self, client, userdata, flags, rc):
        logging.debug("Connected flags"+str(flags)+"result code "+str(rc)+"client1_id")
        if rc==0:
            client.connected_flag=True
            client.publish(self.connected_topic, 1, retain=True)
            #publish connection status
            client.subscribe(self.options["topics"])
        else:
            client.bad_connection_flag=True

    def on_disconnect(self, client, userdata, rc):
        logging.debug("disconnecting reason  " + str(rc))
        client.connected_flag=False
        client.disconnect_flag=True
        client.subscribe_flag=False 

    def update_status(self, client, status):
        status=status.upper()
        if status in self.options['states']: #Valid status
            client.sensor_status=status #update

    def publish_status(self, client):
        pubflag=False
        if self.start_flag:
            self.start_flag=False
            pubflag=True
        if time.time()-client.last_pub_time >= self.options["interval_pub"]:
            pubflag=True
        if time.time()-client.last_pub_time >= self.options["interval"] and self.options['verbose']:
            pubflag=True
        logging.debug("old "+str(client.sensor_status_old))
        logging.debug("new "+ str(client.sensor_status))    
        if client.sensor_status_old!=client.sensor_status or pubflag:
            client.publish(self.sensor_status_topic,client.sensor_status,0,True)
            print("publish on",self.sensor_status_topic,\
                  " message  ",client.sensor_status)
            client.last_pub_time=time.time()
            client.sensor_status_old=client.sensor_status
            
    def Connect(self, client, broker, port, keepalive, run_forever=False):
        """Attempts connection set delay to >1 to keep trying
        but at longer intervals  """
        connflag=False
        delay=5
        #print("connecting ",client)
        badcount=0 # counter for bad connection attempts
        while not connflag:
            logging.info("connecting to broker "+str(broker))
            print("connecting to broker "+str(broker)+":"+str(port))
            print("Attempts ",badcount)
            try:
                res=client.connect(broker,port,keepalive)      #connect to broker
                if res==0:
                    connflag=True
                    return 0
                else:
                    logging.debug("connection failed ",res)
                    badcount +=1
                    if badcount>=3 and not run_forever: 
                        return -1
                        raise SystemExit #give up
                    elif run_forever and badcount<3:
                        delay=5
                    else:
                        delay=30

            except:
                client.badconnection_flag=True
                logging.debug("connection failed")
                badcount +=1
                if badcount>=3 and not run_forever: 
                    return -1
                    raise SystemExit #give up
                elif run_forever and badcount<3:
                    delay=5*badcount
                elif delay<300:
                    delay=30*badcount
            time.sleep(delay)

        return 0

    def wait_for(self, client, msgType, period=.25, wait_time=40, running_loop=False):
        #running loop is true when using loop_start or loop_forever
        client.running_loop=running_loop #
        wcount=0  
        while True:
            logging.info("waiting"+ msgType)
            if msgType=="CONNACK":
                if client.on_connect:
                    if client.connected_flag:
                        return True
                    if client.bad_connection_flag: #
                        return False
            if not client.running_loop:
                client.loop(.01)  #check for messages manually
            time.sleep(period)
            #print("loop flag ",client.running_loop)
            wcount+=1
            if wcount>wait_time:
                print("return from wait loop taken too long")
                return False
