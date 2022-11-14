import random
import datetime
import pandas as pd
from sqlalchemy import create_engine

class LightSimulation:
    def __init__(self,table_name='light',username='root',password='root',host='localhost',database='smartdb'):
        self.table_name = table_name
        self.engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(username,password,host,database))
        self.conn = self.engine.connect()
        self.df_brightness_path = "./Historical_IoT_Data/Room1_Brightness.csv"
        self.get_historical_data()
    
    def get_historical_data(self):
        self.df_brightness = pd.read_csv(self.df_brightness_path,sep="\t", header=None, names=['Timestamp','Brightness'])
        self.df_brightness['Date'] = self.df_brightness['Timestamp'].apply(lambda val:pd.Timestamp(val,unit='s'))
        self.df_brightness.drop(columns=['Timestamp'],inplace=True)
        
    def generate_synthetic_data(self,device_id,no_of_records=11037):
        self.device_id = device_id
        self.df_synthetic_brightness = pd.DataFrame()
        self.random_timeseries()
        self.df_synthetic_brightness["Brightness"] = self.time_series 
        self.df_synthetic_brightness["Brightness"] = self.df_synthetic_brightness["Brightness"] + self.df_brightness["Brightness"]
        self.df_synthetic_brightness["Brightness"] = abs(self.df_synthetic_brightness["Brightness"])
        current_time = datetime.datetime.now()
        self.df_synthetic_brightness["Date"] = [current_time + datetime.timedelta(minutes=10*i) for i in range(self.df_brightness.shape[0])]
        self.df_synthetic_brightness['DeviceId'] = ["Device"+str(device_id) for i in range(self.df_brightness.shape[0])] 
        self.store_synthetic_data()
    
    def random_timeseries(self,count=11037):
        initial_value = random.random()
        volatility = random.random()
        self.time_series = [initial_value, ]
        for _ in range(count):
            self.time_series.append(self.time_series[-1] + initial_value * random.gauss(0, 1) * volatility)
    
    def store_synthetic_data(self):
        #self.df_synthetic_path = "Lightt "+ str(self.device_id) + ".xlsx"
        #self.df_synthetic_brightness.to_excel(self.df_synthetic_path,index=False)
        self.df_synthetic_brightness.to_sql(self.table_name, self.engine, if_exists='append',index=False)