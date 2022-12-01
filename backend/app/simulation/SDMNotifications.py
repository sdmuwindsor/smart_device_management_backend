import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime,timedelta
from ThermostatAnomaly import ThermostatAnomalyDetection
from LightAnomaly import LightAnomalyDetection

class Notifications:
    def __init__(self,username='usr',password='Sdm!4321',host='sdm.mysql.database.azure.com',database='sdm'):
        self.engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(username,password,host,database))
        self.conn = self.engine.connect()
        self.current_time = datetime.now()
        self.yesterday_time = (self.current_time - timedelta(1)).strftime('%Y-%m-%d')
        self.start_time = datetime.strptime(self.yesterday_time+' 00:00:00','%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.strptime(self.yesterday_time+' 23:59:59','%Y-%m-%d %H:%M:%S')
        self.light_anomaly_detection_ob = LightAnomalyDetection()
        self.thermostat_anomaly_detection_ob = ThermostatAnomalyDetection()
    
    def get_notifications(self):
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
                        self.light_anomaly_detection_ob.detect_anomaly(device_id,self.start_time,self.end_time)
                    elif device_category == 'thermostat':
                        self.thermostat_anomaly_detection_ob.detect_anomaly(device_id,self.start_time,self.end_time)