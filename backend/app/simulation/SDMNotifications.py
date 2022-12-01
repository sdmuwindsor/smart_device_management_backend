import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime,timedelta
from ThermostatAnomaly import ThermostatAnomalyDetection
from LightAnomaly import LightAnomalyDetection
import sys
import os

# from app.utils.mail import send_mails
# sys.path.append(f"{os.getcwd()}"+"/app")


import os
from redmail import outlook
from pathlib import Path

class Notifications:
    def __init__(self,username='usr',password='Sdm!4321',host='sdm.mysql.database.azure.com',database='sdm'):
        self.engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(username,password,host,database))
        # self.engine = engine
        self.conn = self.engine.connect()
        self.current_time = datetime.now()
        self.yesterday_time = (self.current_time - timedelta(1)).strftime('%Y-%m-%d')
        self.start_time = datetime.strptime(self.yesterday_time+' 00:00:00','%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.strptime(self.yesterday_time+' 23:59:59','%Y-%m-%d %H:%M:%S')
        self.light_anomaly_detection_ob = LightAnomalyDetection(engine=self.engine)
        self.thermostat_anomaly_detection_ob = ThermostatAnomalyDetection(engine=self.engine)
    
    def send_report(self,name, to_email, file_path, device_name, room_name):
        outlook.username = "sdm.mac.2022@outlook.com"
        outlook.password = "kYDLu6bs2Wz3jcG"

        outlook.send(
            receivers=[to_email],
            subject=f"Alert! Anamoly Detected",
            text="Hi "+name.title()+"\n\nThis is an auto generated email.\nThis email is sent to report an anamoly detected by our system for your smart device '"+device_name+"' in '"+room_name+"' room.\nPFA, the anamoly detection report.\n\nThank You\nSDM Team",
            attachments={
                'anamoly.pdf':Path(file_path)
            }
        )

    def get_notifications(self):
        notifications_msg = []
        self.users_df = pd.read_sql("SELECT * FROM users", self.conn)
        for i,row in self.users_df.iterrows():
            user_id = row['id']
            first_name = row['first_name']
            email_id = row['email']
            self.rooms_df = pd.read_sql("SELECT * FROM rooms where user_id={0}".format(user_id),self.conn)
            for j,roww in self.rooms_df.iterrows():
                room_name = roww['name']
                room_id = roww['id']
                self.devices_df = pd.read_sql("SELECT * FROM devices where room_id={0}".format(room_id),self.conn)
                for k,rowww in self.devices_df.iterrows():
                    device_name = rowww['name']
                    device_id = rowww['id']
                    device_category = rowww['category']
                    if device_category == 'light':
                        tmp_device_df = pd.read_sql("SELECT * FROM {0} WHERE device_id='{1}' and created>={1} and created <='{2}'".format('lights',device_id,self.start_time,self.end_time), self.conn)
                        if tmp_device_df.shape[0] > 0:
                            self.light_anomaly_detection_ob.detect_anomaly(device_id,self.start_time,self.end_time)
                            self.send_report(first_name, email_id, self.light_anomaly_detection_ob.pdf_file_path, device_name, room_name)
                            notifications_msg.append([user_id,'Anomaly Graph For '+str(room_name),'We have sent you an email with the Anomaly Report for Light Device '+str(device_id)+' Please check your email.']) 
                    elif device_category == 'thermostat':
                        tmp_device_df = pd.read_sql("SELECT * FROM {0} WHERE device_id='{1}' and created>={1} and created <='{2}'".format('thermostats',device_id,self.start_time,self.end_time), self.conn)
                        if tmp_device_df.shape[0] > 0:
                            self.thermostat_anomaly_detection_ob.detect_anomaly(device_id,self.start_time,self.end_time)
                            self.send_report(first_name, email_id, self.thermostat_anomaly_detection_ob.pdf_file_path, device_name, room_name)
                        notifications_msg.append([user_id,'Anomaly Graph For '+str(room_name),'We have sent you an email with the Anomaly Report for Thermostat Device '+str(device_id)+' Please check your email.']) 
        notifications_df = pd.DataFrame(notifications_msg,columns=['user_id','title','message'])
        print(notifications_df.head(5))
        if notifications_df.shape[0] > 0:
            notifications_df.to_sql('notifications',self.engine,if_exists='append',index=False)
        else:
            print("No Notifications Generated")


ob=Notifications()
ob.get_notifications()
