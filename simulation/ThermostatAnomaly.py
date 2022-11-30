import os
import copy
#import pdfkit
import plotly
#import webbrowser
import pandas as pd
import plotly.io as pio
from datetime import datetime
from pyhtml2pdf import converter
import plotly.graph_objects as go
from adtk.detector import QuantileAD
from sqlalchemy import create_engine
from plotly.subplots import make_subplots

class ThermostatAnomalyDetection:
     def __init__(self,table_name='thermostat',username='usr',password='Sdm!4321',host='sdm.mysql.database.azure.com',database='sdm'):
        self.table_name = table_name
        self.engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(username,password,host,database))
        self.conn = self.engine.connect()
    
     def detect_anomaly(self,device_id,html_file_path='Thermostat_Report.html'):
        current_time = datetime.now()
        self.device_df = pd.read_sql("SELECT * FROM {0} WHERE deviceid='{1}' and date <='{2}'".format(self.table_name,device_id,current_time), self.conn)
        self.device_df.rename(columns={'humidity':'Relative_Humidity_Percentage',
                                       'indoortemperature':'Indoor_Temperature_C',
                                       'outdoortemperature':'Outdoor_Temperature_C',
                                       'date':'Date',
                                       'deviceid':'DeviceId'},inplace=True)
        temp_df = copy.deepcopy(self.device_df)
        temp_df.set_index('Date',inplace=True)
        quantile_ad = QuantileAD(high=0.99, low=0.01)
        
        self.anomalies_humidity = quantile_ad.fit_detect(temp_df['Relative_Humidity_Percentage'])
        self.anomalies_humidity = self.anomalies_humidity.reset_index()
        self.anomalies_humidity.rename(columns={'Relative_Humidity_Percentage':'Anomaly'},inplace=True)
        self.anomalies_humidity['Relative_Humidity_Percentage'] = self.device_df['Relative_Humidity_Percentage']
        self.anomaly_humidity_df = self.anomalies_humidity[self.anomalies_humidity['Anomaly']==True]
        self.anomaly_humidity_df.reset_index(drop=True,inplace=True)

        self.anomalies_intemp = quantile_ad.fit_detect(temp_df['Indoor_Temperature_C'])
        self.anomalies_intemp = self.anomalies_intemp.reset_index()
        self.anomalies_intemp.rename(columns={'Indoor_Temperature_C':'Anomaly'},inplace=True)
        self.anomalies_intemp['Indoor_Temperature_C'] = self.device_df['Indoor_Temperature_C']
        self.anomaly_intemp_df = self.anomalies_intemp[self.anomalies_intemp['Anomaly']==True]
        self.anomaly_intemp_df.reset_index(drop=True,inplace=True)

        self.anomalies_outtemp = quantile_ad.fit_detect(temp_df['Outdoor_Temperature_C'])
        self.anomalies_outtemp = self.anomalies_outtemp.reset_index()
        self.anomalies_outtemp.rename(columns={'Outdoor_Temperature_C':'Anomaly'},inplace=True)
        self.anomalies_outtemp['Outdoor_Temperature_C'] = self.device_df['Outdoor_Temperature_C']
        self.anomaly_outtemp_df = self.anomalies_outtemp[self.anomalies_outtemp['Anomaly']==True]
        self.anomaly_outtemp_df.reset_index(drop=True,inplace=True)
        self.plot_graph(html_file_path)
    
     def plot_graph(self,html_file_path):
        #path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        #config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        if os.path.exists(html_file_path):
            os.remove(html_file_path)
        with open(html_file_path, 'a') as report:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x = self.anomalies_humidity['Date'].tolist(),
                y = self.anomalies_humidity['Relative_Humidity_Percentage'].tolist(),
                name='Non Anomaly'
                ))
            fig.add_trace(
                go.Scatter(
                    name='Anomaly',
                    mode='markers',
                    x=self.anomalies_humidity[self.anomalies_humidity['Anomaly']==True]['Date'].tolist(),
                    y= self.anomalies_humidity[self.anomalies_humidity['Anomaly']==True]['Relative_Humidity_Percentage'].tolist(),
                    opacity=0.5,
                    marker=dict(
                        color='Red',
                        size=10,
                        line=dict(
                            color='Red',
                            width=2
                        )
                    )
                )
            )
            fig.update_layout(
                autosize = True,
                #width=1000,
                #height=1000,
                xaxis_title="Date ----> ",
                yaxis_title="Humidity ---->",
                title="Anomaly Graph For Humidity")
            report.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
            table_fig = go.Figure(data=[go.Table(header=dict(values=self.anomaly_humidity_df.columns.tolist()),
                             cells=dict(values=[self.anomaly_humidity_df[col].tolist() for col in self.anomaly_humidity_df.columns.tolist()]))])
            table_fig.update_layout(title="Probable Anomaly Points For Humidity")
            report.write(table_fig.to_html(full_html=False, include_plotlyjs='cdn'))

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x = self.anomalies_intemp['Date'].tolist(),
                y = self.anomalies_intemp['Indoor_Temperature_C'].tolist(),
                name='Non Anomaly'
                ))
            fig.add_trace(
                go.Scatter(
                    name='Anomaly',
                    mode='markers',
                    x=self.anomalies_intemp[self.anomalies_intemp['Anomaly']==True]['Date'].tolist(),
                    y= self.anomalies_intemp[self.anomalies_intemp['Anomaly']==True]['Indoor_Temperature_C'].tolist(),
                    opacity=0.5,
                    marker=dict(
                        color='Red',
                        size=10,
                        line=dict(
                            color='Red',
                            width=2
                        )
                    )
                )
            )
            fig.update_layout(
                autosize = True,
                #width=1000,
                #height=1000,
                xaxis_title="Date ----> ",
                yaxis_title="Indoor Temperature ---->",
                title="Anomaly Graph For Indoor Temperature")
            report.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
            table_fig = go.Figure(data=[go.Table(header=dict(values=self.anomaly_intemp_df.columns.tolist()),
                             cells=dict(values=[self.anomaly_intemp_df[col].tolist() for col in self.anomaly_intemp_df.columns.tolist()]))])
            table_fig.update_layout(title="Probable Anomaly Points For Indoor Temperature")
            report.write(table_fig.to_html(full_html=False, include_plotlyjs='cdn'))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x = self.anomalies_outtemp['Date'].tolist(),
                y = self.anomalies_outtemp['Outdoor_Temperature_C'].tolist(),
                name='Non Anomaly'
                ))
            fig.add_trace(
                go.Scatter(
                    name='Anomaly',
                    mode='markers',
                    x=self.anomalies_outtemp[self.anomalies_outtemp['Anomaly']==True]['Date'].tolist(),
                    y= self.anomalies_outtemp[self.anomalies_outtemp['Anomaly']==True]['Outdoor_Temperature_C'].tolist(),
                    opacity=0.5,
                    marker=dict(
                        color='Red',
                        size=10,
                        line=dict(
                            color='Red',
                            width=2
                        )
                    )
                )
            )
            fig.update_layout(
                autosize = True,
                #width=1000,
                #height=1000,
                xaxis_title="Date ----> ",
                yaxis_title="Outdoor Temperature ---->",
                title="Anomaly Graph For Outdoor Temperature")
            report.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
            table_fig = go.Figure(data=[go.Table(header=dict(values=self.anomaly_outtemp_df.columns.tolist()),
                             cells=dict(values=[self.anomaly_outtemp_df[col].tolist() for col in self.anomaly_outtemp_df.columns.tolist()]))])
            table_fig.update_layout(title="Probable Anomaly Points For Outdoor Temperature")
            report.write(table_fig.to_html(full_html=False, include_plotlyjs='cdn')) 
            #webbrowser.open(html_file_path)
            path = os.path.abspath(html_file_path)
            pdf_file_path = html_file_path.split(".html")[0] + ".pdf"
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)
            converter.convert(f'file:///{path}', pdf_file_path)
            self.pdf_file_path = pdf_file_path