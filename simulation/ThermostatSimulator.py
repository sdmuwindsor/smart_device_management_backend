import pandas as pd
import functools as ft
from sdv.lite import TabularPreset

class ThermostatSimulation:
    def __init__(self):
        self.df_humidity_path = "./Historical_IoT_Data/Room1_Humidity.csv"
        self.df_temperature_path = "./Historical_IoT_Data/Room1_ThermostatTemperature.csv"
        self.df_outside_temperature_path = "./Historical_IoT_Data/Room1_Virtual_OutdoorTemperature.csv"
        self.metadata = {'fields': {'ID': {'type': 'numerical', 'subtype': 'integer'},
                                    'Relative_Humidity_Perc': {'type': 'numerical', 'subtype': 'integer'},
                                    'Temperature_C': {'type': 'numerical', 'subtype': 'float'},
                                    'Outside_Temperature_C': {'type': 'numerical', 'subtype': 'float'}},
                            'constraints': [],
                            'primary_key': 'ID'}
        self.device_id = 1
        self.model_thermostat = TabularPreset(name='FAST_ML', metadata=self.metadata)
        self.get_historical_data()
        self.train_preset_model()
    
    def get_historical_data(self):
        self.df_relative_humidity = pd.read_csv(self.df_humidity_path,sep="\t", header=None, names=['Timestamp','Relative_Humidity_Perc'])
        self.df_thermostat_temp = pd.read_csv(self.df_temperature_path,sep="\t", header=None, names=['Timestamp','Temperature_C'])
        self.df_outside_temp = pd.read_csv(self.df_outside_temperature_path,sep="\t", header=None, names=['Timestamp','Outside_Temperature_C'])
        dfs_thermostat = [self.df_relative_humidity, self.df_thermostat_temp, self.df_outside_temp]
        self.df_thermostat = ft.reduce(lambda left, right: pd.merge(left, right, on='Timestamp'), dfs_thermostat)
        self.df_thermostat['Timestamp'] = self.df_thermostat.index
        self.df_thermostat.rename(columns={'Timestamp':'ID'},inplace=True)
        
    def train_preset_model(self):
        self.model_thermostat.fit(self.df_thermostat)
        
    def generate_synthetic_data(self,no_of_records):
        self.df_synthetic_thermostat = self.model_thermostat.sample(num_rows=no_of_records,randomize_samples=True)
    
    def store_synthetic_data(self):
        self.df_synthetic_path = "Thermostat "+ str(self.device_id) + ".xlsx"
        self.df_synthetic_thermostat.to_excel(self.df_synthetic_path,index=False)
        self.device_id = self.device_id + 1
        return self.df_synthetic_path


