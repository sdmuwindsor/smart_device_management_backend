import copy
import plotly
import plotly.io as pio
from datetime import datetime
import plotly.graph_objects as go
from adtk.detector import QuantileAD

class AnomalyDetection:
    def __init__(self,table_name='light',username='root',password='root',host='localhost',database='smartdb'):
        self.table_name = table_name
        self.engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(username,password,host,database))
        self.conn = self.engine.connect()
    
    def detect_anomaly(self,device_id):
        #current_time = datetime.now()
        current_time = datetime(2022, 11, 13, 14, 47, 8, 0)
        self.device_df = pd.read_sql("SELECT * FROM {0} WHERE DeviceId='{1}' and Date <='{2}'".format(self.table_name,device_id,current_time), self.conn)
        temp_df = copy.deepcopy(self.device_df)
        temp_df.set_index('Date',inplace=True)
        quantile_ad = QuantileAD(high=0.99, low=0.01)
        self.anomalies = quantile_ad.fit_detect(temp_df['Brightness'])
        self.anomalies = self.anomalies.reset_index()
        self.anomalies.rename(columns={'Brightness':'Anomaly'},inplace=True)
        self.anomalies['Brightness'] = self.device_df['Brightness']
        self.anomaly_df = self.anomalies[self.anomalies['Anomaly']==True]
        self.anomaly_df.reset_index(drop=True,inplace=True)
        self.plot_graph()
    
    def plot_graph(self,save=True,fname='Light_Anomaly_Graph.html'):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x = self.anomalies['Date'].tolist(),
            y = self.anomalies['Brightness'].tolist()
            ))
        fig.add_trace(
            go.Scatter(
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
            width=1000,
            height=1000,
            xaxis_title="Date ----> ",
            yaxis_title="Brightness ---->")
        #fig.show()
        if save:
            plotly.offline.plot(fig, filename=fname, auto_open=False)
        self.anomaly_graph_html = fig.to_html()