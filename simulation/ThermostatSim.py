import random
import datetime
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

class ThermostatSimulation:
    def __init__(self,table_name='thermostat',username='usr',password='Sdm!4321',host='sdm.mysql.database.azure.com',database='sdm'):
        self.table_name = table_name
        self.engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(username,password,host,database))
        self.conn = self.engine.connect()
        self.df_thermostat_path = "./Historical_IoT_Data/Room1_Thermostat.csv"
        self.get_historical_data()
    
    def get_historical_data(self):
        self.df_thermostat = pd.read_csv(self.df_thermostat_path)
        
    def generate_synthetic_data(self,device_id,no_of_records=3709):
        self.device_id = device_id
        self.df_synthetic_thermostat = pd.DataFrame()

        self.random_timeseries()
        self.df_synthetic_thermostat["Relative_Humidity_Percentage"] = self.time_series 
        self.df_synthetic_thermostat["Relative_Humidity_Percentage"] = self.df_synthetic_thermostat["Relative_Humidity_Percentage"] + self.df_thermostat["Relative_Humidity_Percentage"]
        self.df_synthetic_thermostat["Relative_Humidity_Percentage"] = abs(self.df_synthetic_thermostat["Relative_Humidity_Percentage"])

        self.random_timeseries()
        self.df_synthetic_thermostat["Indoor_Temperature_C"] = self.time_series 
        self.df_synthetic_thermostat["Indoor_Temperature_C"] = self.df_synthetic_thermostat["Indoor_Temperature_C"] + self.df_thermostat["Indoor_Temperature_C"]
        self.df_synthetic_thermostat["Indoor_Temperature_C"] = abs(self.df_synthetic_thermostat["Indoor_Temperature_C"])

        self.random_timeseries()
        self.df_synthetic_thermostat["Outdoor_Temperature_C"] = self.time_series 
        self.df_synthetic_thermostat["Outdoor_Temperature_C"] = self.df_synthetic_thermostat["Outdoor_Temperature_C"] + self.df_thermostat["Outdoor_Temperature_C"]
        self.df_synthetic_thermostat["Outdoor_Temperature_C"] = abs(self.df_synthetic_thermostat["Outdoor_Temperature_C"])

        current_time = datetime.datetime.now()
        self.df_synthetic_thermostat["Date"] = [current_time + datetime.timedelta(minutes=10*i) for i in range(self.df_thermostat.shape[0])]
        self.df_synthetic_thermostat['DeviceId'] = ["Device"+str(device_id) for i in range(self.df_thermostat.shape[0])] 
        self.store_synthetic_data()
        #self.plot_graph()
    
    def random_timeseries(self,count=3709):
        initial_value = random.random()
        volatility = random.random()
        self.time_series = [initial_value, ]
        for _ in range(count):
            self.time_series.append(self.time_series[-1] + initial_value * random.gauss(0, 1) * volatility)
    
    def store_synthetic_data(self):
        self.df_synthetic_thermostat.rename(columns={'Relative_Humidity_Percentage':'humidity',
                                                     'Indoor_Temperature_C':'indoortemperature',
                                                     'Outdoor_Temperature_C':'outdoortemperature',
                                                     'Date':'date',
                                                     'DeviceId':'deviceid'},inplace=True)
        self.df_synthetic_thermostat.to_sql(self.table_name, self.engine, if_exists='append',index=False)
        
    
    def plot_graph(self):
        self.df_synthetic_thermostat.rename(columns={'humidity':'Relative_Humidity_Percentage',
                                                     'indoortemperature':'Indoor_Temperature_C',
                                                     'outdoortemperature':'Outdoor_Temperature_C',
                                                     'date':'Date',
                                                     'deviceid':'DeviceId'},inplace=True)
        self.df_synthetic_thermostat.drop(columns=['DeviceId'],inplace=True)
        for df in [self.df_thermostat,self.df_synthetic_thermostat]:
            fig = px.line(df, x="Date", y=df.columns)
            fig.show()
        self.df_synthetic_brightness.to_sql(self.table_name, self.engine, if_exists='append',index=False)