import pandas as pd
import functools as ft
from sdv.lite import TabularPreset

class LightSimulation:
    def __init__(self):
        self.df_brightness_path = "./Historical_IoT_Data/Room1_Brightness.csv"
        self.metadata = {'fields': {'ID': {'type': 'numerical', 'subtype': 'integer'},
                                    'Brightness_Lux': {'type': 'numerical', 'subtype': 'float'}},
                            'constraints': [],
                            'primary_key': 'ID'}
        self.device_id = 1
        self.model_brightness = TabularPreset(name='FAST_ML', metadata=self.metadata)
        self.get_historical_data()
        self.train_preset_model()
    
    def get_historical_data(self):
        self.df_brightness = pd.read_csv(self.df_brightness_path,sep="\t", header=None, names=['Timestamp','Brightness_Lux'])
        self.df_brightness['Timestamp'] = self.df_brightness.index
        self.df_brightness.rename(columns={'Timestamp':'ID'},inplace=True)
    
    def train_preset_model(self):
        self.model_brightness.fit(self.df_brightness)
        
    def generate_synthetic_data(self,no_of_records):
        self.df_synthetic_brightness = self.model_brightness.sample(num_rows=no_of_records,randomize_samples=True)
    
    def store_synthetic_data(self):
        self.df_synthetic_path = "Light "+ str(self.device_id) + ".xlsx"
        self.df_synthetic_brightness.to_excel(self.df_synthetic_path,index=False)
        self.device_id = self.device_id + 1
        return self.df_synthetic_path

