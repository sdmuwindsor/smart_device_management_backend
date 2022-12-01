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
import sys
import os

#sys.path.append(f"{os.getcwd()}"+"/app")
#from app.db.session import engine
class LightAnomalyDetection:
    def __init__(self,engine,table_name='lights',username='usr',password='Sdm!4321',host='sdm.mysql.database.azure.com',database='sdm'):
        self.table_name = table_name
        #self.engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(username,password,host,database))
        self.engine = engine
        self.conn = self.engine.connect()
    
    def detect_anomaly(self,device_id,start_time,end_time,html_file_path='Light_Report.html'):
        current_time = datetime.now()
        self.device_df = pd.read_sql("SELECT * FROM {0} WHERE device_id='{1}' and created>={1} and created <='{2}'".format(self.table_name,device_id,start_time,end_time), self.conn)
        #self.start_time = self.device_df['created'][0]
        #self.end_time = current_time
        self.device_df.rename(columns={'brightness':'Brightness','created':'Date','device_id':'DeviceId'},inplace=True)
        temp_df = copy.deepcopy(self.device_df)
        temp_df.set_index('Date',inplace=True)
        quantile_ad = QuantileAD(high=0.99, low=0.01)
        self.anomalies = quantile_ad.fit_detect(temp_df['Brightness'])
        self.anomalies = self.anomalies.reset_index()
        self.anomalies.rename(columns={'Brightness':'Anomaly'},inplace=True)
        self.anomalies['Brightness'] = self.device_df['Brightness']
        self.anomaly_df = self.anomalies[self.anomalies['Anomaly']==True]
        self.anomaly_df.reset_index(drop=True,inplace=True)
        self.plot_graph(html_file_path)
    
    def plot_graph(self,html_file_path):
        #path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        #config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        if os.path.exists(html_file_path):
            os.remove(html_file_path)
        with open(html_file_path, 'a') as report:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x = self.anomalies['Date'].tolist(),
                y = self.anomalies['Brightness'].tolist(),
                name='Non Anomaly'
                ))
            fig.add_trace(
                go.Scatter(
                    name='Anomaly',
                    mode='markers',
                    x=self.anomalies[self.anomalies['Anomaly']==True]['Date'].tolist(),
                    y= self.anomalies[self.anomalies['Anomaly']==True]['Brightness'].tolist(),
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
                yaxis_title="Brightness ---->",
                title="Anomaly Graph")
            report.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
            table_fig = go.Figure(data=[go.Table(header=dict(values=self.anomaly_df.columns.tolist()),
                             cells=dict(values=[self.anomaly_df[col].tolist() for col in self.anomaly_df.columns.tolist()]))])
            table_fig.update_layout(title="Probable Anomaly Points For Brightness")
            report.write(table_fig.to_html(full_html=False, include_plotlyjs='cdn')) 
            #webbrowser.open(html_file_path)
            path = os.path.abspath(html_file_path)
            pdf_file_path = html_file_path.split(".html")[0] + ".pdf"
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)
            converter.convert(f'file:///{path}', pdf_file_path)
            self.pdf_file_path = pdf_file_path