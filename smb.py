import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
from dash.dependencies import Input, Output, State
import paho.mqtt.client as mqtt
import time
import pandas as pd
import sqlite3
import os
import base64
from six.moves.urllib.parse import quote
from sqlalchemy import create_engine
from datetime import datetime,timedelta
import unicodedata

FA ="https://use.fontawesome.com/releases/v5.8.1/css/all.css"

server = Flask(__name__)
#server.config['DEBUG'] = True
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')

#server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
db_URI = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
engine = create_engine(db_URI)

class User(db.Model):
    __tablename__ = 'datatable'

    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(26))
    devId = db.Column(db.String(15))
    SPA = db.Column(db.String(10))
    TA = db.Column(db.String(10))

    def __repr__(self):
        return '<User %r %r  %r %r>' % (self.stamp, self.devId, self.SPA, self.TA)

class smb(db.Model):
    __tablename__ = 'smbtable'

    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(26))
    devId = db.Column(db.String(15))
    str1 = db.Column(db.String(10))
    str2 = db.Column(db.String(10))
    str3 = db.Column(db.String(10))
    str4 = db.Column(db.String(10))
    str5 = db.Column(db.String(10))
    str6 = db.Column(db.String(10))
    str7 = db.Column(db.String(10))
    str8 = db.Column(db.String(10))
    str9 = db.Column(db.String(10))
    str10 = db.Column(db.String(10))
    str11 = db.Column(db.String(10))
    str12 = db.Column(db.String(10))
    str13 = db.Column(db.String(10))

    vol1 = db.Column(db.String(10))
    vol2 = db.Column(db.String(10))
    vol3 = db.Column(db.String(10))
    vol4 = db.Column(db.String(10))
    vol5 = db.Column(db.String(10))
    vol6 = db.Column(db.String(10))
    vol7 = db.Column(db.String(10))
    vol8 = db.Column(db.String(10))
    vol9 = db.Column(db.String(10))
    vol10 = db.Column(db.String(10))
    vol11 = db.Column(db.String(10))
    vol12 = db.Column(db.String(10))
    vol13 = db.Column(db.String(10))
   
    temp = db.Column(db.String(10))
    
    

    def __repr__(self):
        return '<User %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r>' % (self.stamp, self.devId, self.str1, self.str2, self.str3, self.str4, self.str5, self.str6, self.str7, self.str8, self.str9, self.str10, self.str11, self.str12, self.str13, self.vol1, self.vol2, self.vol3, self.vol4, self.vol5, self.vol6, self.vol7, self.vol8, self.vol9, self.vol10, self.vol11, self.vol12, self.vol13, self.temp)

db.create_all()
def on_connect(client, userdata, flags, rc):
    print("Connected!", rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_publish(client, userdata, mid):
    print("Publish:", client)

def on_log(client, userdata, level, buf):
    print("log:", buf)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
messagelist=[]
smbdict={}
teststr=""
devicetime=[]
def on_message(client, userdata, message):
    #data={}
    data1={}
    payload = str(message.payload.decode("utf-8")) + " "
    print("payload=",payload,len(payload))
    #messagelist=
    if len(payload)>37 and len(payload)!=45:
        #print("hi")
        teststr=payload[:7]+payload[32:]
        #print(teststr)
        #devicetime[0]=payload[7:11]
        
        #devicetime[1]=payload[12:31]
        #print(devicetime)
        data = dict(x.split(":") for x in teststr.split(","))
        #print(payload[12:31])
        data['Time']=payload[12:31]#devicetime[1]
        print("smb data=",data)
    #data = dict(x.split(":") for x in teststr.split(","))
    elif len(payload)==45:
        teststr=payload[:7]+payload[34:]
        #print(teststr)
        data = dict(x.split(":") for x in teststr.split(","))
        #print(payload[13:32])
        data['Time']=payload[13:32]#devicetime[1]
        print("smb data=",data)

    print("teststr=",teststr)

    messagelist.append(payload)
    if len(messagelist)>4:
        #for i in (0,3):
            messagelist.remove(messagelist[0])
    print("messagelist=",messagelist)
    if len(payload)==34:
        data1 = dict(x.split(": ") for x in payload.split(" , "))
    #data = dict(x.split(":") for x in teststr.split(","))
    #data['Time']=devicetime[1]
    print("smb dict=",smbdict)
    #print("data=",data1)
    #print("smb data=",data)
    print("len dataa=",len(data))
    if (len(data1)==34):
        print("len",len(data1))
        admin = User(stamp=str(datetime.now()+timedelta(minutes=330)),devId=data1['devId'],SPA=data1['SPA'],TA=data1['TA'])
        db.session.add(admin)
        db.session.commit()


    elif (len(payload)==45 and (len(smbdict)==28)):

    #elif ((len(data)==3) and (len(smbdict)==28) and (data['temp'] is not None)):
        smbdict['temp']=data['temp']
        print("smb dict=",smbdict)
        smbdata = smb(stamp=smbdict['Time'],devId=smbdict['Dev'],temp=smbdict['temp'],str1=smbdict['str1'],vol1=smbdict['vol1'],str2=smbdict['str2'],vol2=smbdict['vol2'],str3=smbdict['str3'],vol3=smbdict['vol3'],str4=smbdict['str4'],vol4=smbdict['vol4'],str5=smbdict['str5'],vol5=smbdict['vol5'],str6=smbdict['str6'],vol6=smbdict['vol6'],str7=smbdict['str7'],vol7=smbdict['vol7'],str8=smbdict['str8'],vol8=smbdict['vol8'],str9=smbdict['str9'],vol9=smbdict['vol9'],str10=smbdict['str10'],vol10=smbdict['vol10'],str11=smbdict['str11'],vol11=smbdict['vol11'],str12=smbdict['str12'],vol12=smbdict['vol12'],str13=smbdict['str13'],vol13=smbdict['vol13'])
        db.session.add(smbdata)
        db.session.commit()
        smbdict.clear()
    
    #print("len dataa=",len(data))
    #elif payload:
    #    print("pay=",payload)
    #    messageli=messagelist+list(payload)
    #    print("messagelist=",messageli)
    elif len(data)==4:
    #elif ((len(payload)>37) and (len(payload)!=45)):
        print("hi dict")
        print(len(smbdict))
        if len(smbdict)==0:
            smbdict.update(data)
            print(len(smbdict))
        #else:# len(smbdict)==4
        #if 'str2' not in smbdict:
        elif (('str2' not in smbdict) and ('str2' in data)):
            print("str2")
            smbdict['str2']=data['str2']
            smbdict['vol2']=data['vol2']
        #elif 'str3' not in smbdict:
        elif (('str3' not in smbdict) and ('str3' in data)):
            print("str3")
            smbdict['str3']=data['str3']
            smbdict['vol3']=data['vol3']
        #elif 'str4' not in smbdict:
        elif (('stri4' not in smbdict) and ('str4' in data)):
            print("str4")
            smbdict['str4']=data['str4']
            smbdict['vol4']=data['vol4']
        #elif 'str5' not in smbdict:
        elif (('stri5' not in smbdict) and ('str5' in data)):
            print("str5")
            smbdict['str5']=data['str5']
            smbdict['vol5']=data['vol5']
        #elif 'str6' not in smbdict:
        elif (('str6' not in smbdict) and ('str6' in data)):
            print("str6")
            smbdict['str6']=data['str6']
            smbdict['vol6']=data['vol6']
        #elif 'str7' not in smbdict:
        elif (('str7' not in smbdict) and ('str7' in data)):
            print("str7")
            smbdict['str7']=data['str7']
            smbdict['vol7']=data['vol7']
        #elif 'str8' not in smbdict:
        elif (('str8' not in smbdict) and ('str8' in data)):
            print("str8")
            smbdict['str8']=data['str8']
            smbdict['vol8']=data['vol8']
        elif (('str9' not in smbdict) and ('str9' in data)):
            print("str9")
            smbdict['str9']=data['str9']
            smbdict['vol9']=data['vol9']
        elif (('str10' not in smbdict) and ('str10' in data)):
            print("str10")
            smbdict['str10']=data['str10']
            smbdict['vol10']=data['vol10']
        elif (('str11' not in smbdict) and ('str11' in data)):
            print("str11")
            smbdict['str11']=data['str11']
            smbdict['vol11']=data['vol11']
        elif (('str12' not in smbdict) and ('str12' in data)):
            print("str12")
            smbdict['str12']=data['str12']
            smbdict['vol12']=data['vol12']
        elif (('str13' not in smbdict) and ('str13' in data)):
            print("str13")
            smbdict['str13']=data['str13']
            smbdict['vol13']=data['vol13']
        print(smbdict)

client = mqtt.Client()
print("client=",client)

client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_connect = on_connect
client.on_message = on_message
time.sleep(1)

subtop="tracker/device/sub"
pubtop="tracker/device/pub"
client.username_pw_set("cbocdpsu", "3_UFu7oaad-8")
client.connect('soldier.cloudmqtt.com', 14035,60)
client.loop_start()
client.subscribe(subtop)
client.loop()

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "15rem",
    "padding": "2rem 2rem",
    "fontSize":"30rem"
}

PLOTLY_LOGO = "https://i2.wp.com/corecommunique.com/wp-content/uploads/2015/09/smarttrak1.png"


navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="50px",width="auto")),
                    dbc.Col(dbc.NavbarBrand( html.H2("TRACKER DASHBOARD",style={"align":"center",'padding-right':'20rem','fontSize':'50px','align':'center','font-style': 'Georgia', 'font-weight': 'bold','color':'navy-blue'}))),

                ],),),],color="#D3C489",)


content = html.Div(id="page-content")

app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

app.config['suppress_callback_exceptions']=True


app.layout = html.Div([navbar,content,
    dcc.Location(id='url', refresh=False),
        html.Div([         
           dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Graph', value='/page-1',style={'backgroundColor':'purple'}),
                #dcc.Tab(label='Graph', value='/page-1',style={'backgroundColor':'#B2A29E'}),
                dcc.Tab(label='Table',  value='/page-2',style={'backgroundColor':'green', 'font-weight': 'bold'}),
                dcc.Tab(label='Read',  value='/page-3',style={'backgroundColor':'brown'}),
                dcc.Tab(label='Write', value='/page-4',style={'backgroundColor':'blue'}),
],value='/page-1')]),
        ],style={'backgroundColor':'#00C0C0'})    

page_2_graph = dbc.Jumbotron([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3('Graph'),
                    dcc.Dropdown(id='devices',
                options=[{'label': 'R1', 'value': 'R1 '},{'label': 'G2', 'value': 'G2 '},{'label': 'R2', 'value': 'R2 '}],
                value='R1 ', style={"width":"auto","height":"auto"}),
            dcc.DatePickerRange(id='my-date-picker-range',
                min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
                max_date_allowed=datetime.now(),
                initial_visible_month=datetime.now(),
                end_date=datetime.now(),
                start_date=datetime.now()-timedelta(days=1)),
            html.Div(id='output-container-date-picker-range'),
            html.Div(id='dd-output-container'),
            dcc.Graph(id='graph-with-slider',style={"width":"auto","height":"300px"}),
            dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),dcc.Link(href='/page-1'),
],style={'maxHeight':"470px","overflowY":"scroll"})),
    ]),
 # ],style={'maxHeight':"400px","overflowX":"scroll","overflowY":"scroll",'width':'600px'})],style={"border":"2px black solid",'maxHeight':'500px','width':'600px','padding': '0px 20px 20px 20px'}),])
  
  ], style={"border":"2px black solid"}),
  ])

page_1_table = dbc.Jumbotron([
    dbc.Container(html.Div([html.H3('Table Data'),
        dcc.DatePickerRange(
            id='my-date-picker-range2',
            min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
            max_date_allowed=datetime.now(),
            initial_visible_month=datetime.now(),
            end_date=datetime.now(),
            start_date=datetime.now()-timedelta(days=1)),
    html.Div(id='output-container-date-picker-range2'),
               html.A(dbc.Button("Download CSV",
            id='download-link',color="primary"),
            style={"padding": "auto"},
            download="data.csv",
            href="",target="_blank"),
            dcc.Link(href='/page-2'),
            html.Div([html.Table(id="live-update-text")],style={'maxHeight':"330px","overflowY":"scroll"}),
]),style={"border":"2px black solid","padding":"0 rem"}),])


         

page_3_read = html.Div([
    html.H4('You can read the data using these dropdown buttons'),
    dcc.Dropdown(
        id='devices1',
        options=[
            {'label': 'R1', 'value': 'R1'},
            {'label': 'G2', 'value': 'G2'},
            {'label': 'R2', 'value': 'R2'}
        ],
        value='', style={"width":"auto"}),
    dcc.Dropdown(
        id='options1',
        options=[
            {'label': 'GETALL', 'value': 'GETALL'},
            {'label': 'LAT', 'value': 'LAT'},
            {'label': 'LONGITUDE', 'value': 'LONGITUDE'},
            {'label': 'RTC', 'value': 'RTC'},
            {'label': 'SUN', 'value': 'SUN'},
            {'label': 'TRACKER', 'value': 'TRACKER'},
            {'label': 'ZONE', 'value': 'ZONE'},
            {'label': 'MODE', 'value': 'MODE'},
            {'label': 'HR', 'value': 'HR'},
            {'label': 'MIN', 'value': 'MIN'},
            {'label': 'SEC', 'value': 'SEC'},
            {'label': 'DATE', 'value': 'DATE'},
            {'label': 'MONTH', 'value': 'MONTH'},
            {'label': 'YEAR', 'value': 'YEAR'},
                    ],
        value='', style={"width":"auto"}),
    #inline=True,
    dbc.Button("Read", id="buttons1"),

html.Div(id='display'),
     dcc.Link(href='/page-3'),
html.Div(messagelist)],style={'minHeight':"500px","overflowY":"scroll",'backgroundColor':'info'})

page_4_write=html.Div([
    html.H4('Using these you can write the commands for setting the values in the device'),
    dcc.Dropdown(
        id='device',
        options=[
            {'label': 'R1 ', 'value': 'R1'},
            {'label': 'G2 ', 'value': 'G2'},
            {'label': 'R2 ', 'value': 'R2'}
        ],
        value='',style={"width":"auto"}
    ),
    #html.H4(''),
    dcc.Dropdown(
        id='options',
        options=[
            {'label': 'LAT', 'value': 'LAT'},
            {'label': 'LONGITUDE', 'value': 'LONGITUDE'},
            {'label': 'SEC', 'value': 'SEC'},
            {'label': 'MIN', 'value': 'MIN'},
                        {'label': 'HOUR', 'value': 'HR'},
            {'label': 'DATE', 'value': 'DATE'},
            {'label': 'MONTH', 'value': 'MONTH'},
            {'label': 'YEAR', 'value': 'YEAR'},
            {'label': 'EAST', 'value': 'EAST'},
            {'label': 'WEST', 'value': 'WEST'},
            {'label': 'TIMEZONE', 'value': 'TIMEZONE'},
            {'label': 'REVLIMIT', 'value': 'REVLIMIT'},
            {'label': 'FWDLIMIT', 'value': 'FWDLIMIT'},
            {'label': 'AUTOMODE', 'value': 'AUTOMODE'},
            {'label': 'MANUALMODE', 'value': 'MANUALMODE'},
        ],
        value='',style={"width":"auto"}
    ),
  dcc.Input(id="input2", type="text"),
  html.Div(id="output"),
        dbc.Button("Write", id="write button"),
            dcc.Link(href='/page-4'),

        ],style={'minHeight':"500px",'backgroundColor':'white'}#,"overflowY":"scroll"}
)
def conv(x):
    val=unicodedata.normalize('NFKD', x).encode('ascii','ignore')
    print("val=",val)
    return val
def table(rows):
    #unicodedata.normalize('NFKD', rows).encode('ascii','ignore')
    table_header=[
        html.Thead(html.Tr([html.Th('Id'),html.Th('stamp'),html.Th('devId'),html.Th('sun angle') ,html.Th('tracker angle')#, html.Th('motor status') ,
         ]))]
    table_body=[
        #html.Tbody(html.Tr([html.Td(dev['id']),html.Td(dev['stamp']),html.Td(dev['devId']),html.Td(dev['SPA']),html.Td(dev['TA'])]))for dev in rows]
        html.Tbody(html.Tr([html.Td(dev[0]),html.Td(dev[1]),html.Td(dev[2]),html.Td(dev[3]),html.Td(dev[4])]))for dev in rows]
        #html.Tbody(html.Tr([html.Td(conv(dev.id)),html.Td(conv(dev.stamp)),html.Td(conv(dev.devId)),html.Td(conv(dev.SPA)),html.Td(conv(dev.TA))]))for dev in rows]
        #html.Tbody(html.Tr([html.Td(dev.id),html.Td(dev.stamp),html.Td(dev.devId),html.Td(dev.SPA),html.Td(dev.TA)]))for dev in rows]
    table=dbc.Table(table_header+table_body,bordered=True,striped=True,hover=True,style={"backgroundColor":"white"})
    return table

@app.callback(
        Output('display', 'children'),
        [Input('devices1', 'value'),Input('options1', 'value'),Input('buttons1','n_clicks')])

def output(val1,val2,n):
    if n:
        client.publish(pubtop,"{} READ:{}".format(val1,val2))
        return "published for getting {}".format(val2)

@app.callback(
        Output('output', 'children'),
        [Input('device', 'value'),Input('options', 'value'),Input('input2','value'),Input('write button', 'n_clicks')])

def update_output(valueDEV,valueOP,value2,x):
    print("dev=",valueDEV,"options=",valueOP,"value=",value2)
    list1=["EAST","WEST","AUTOMODE","MANUALMODE","STOP"]
    if ((valueOP in list1) and (x is not None)):
        client.publish(pubtop,"{} WRITE:{}".format(valueDEV,valueOP))


        print("executing")
        return 'You have published "{} write {}"'.format(valueDEV,valueOP)

    elif((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:{}_{}".format(valueDEV,valueOP,value2))


        return 'You have published "{} {} write {}"'.format(valueDEV,valueOP,value2)
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('devices', 'value'),Input('my-date-picker-range', 'start_date'),Input('my-date-picker-range', 'end_date')])

def update_figure(selected_device,start,end):
    connection1 = engine#.connnect()
    print("start=",start,"end=",end,"dt.now=",datetime.now())
    df=pd.read_sql("select * from datatable",connection1)
    filtered_d = df[df.devId == selected_device]# and ([df.stamp == i] for i in (start,end,timedelta(microseconds=1)))]
    filtered_df = filtered_d.loc[(filtered_d['stamp'] > start) & (filtered_d['stamp'] <= end)]# and ([df.stamp == i] for i in (start,end,timedelta(microseconds=1)))]
    #filtered_df= filtered_d[[str(i) in str([filtered_d.stamp]for stamp in )] for i in (start,end,timedelta(days=1)]
    print("filtered df=",filtered_df)

    return {
                                'data': [
                                    {'x': filtered_df.stamp, 'y':filtered_df.SPA
                                    #.where(df.devname=='dev_01')
                                    , 'name': 'SPA'},
                                    {'x': filtered_df.stamp, 'y':filtered_df.TA
                                                                  , 'name': 'TA'}, ],
            'layout': {
                'title': 'SPA and TA'
                }}


@app.callback(Output("live-update-text", "children"),
              [Input("live-update-text", "className"),Input('my-date-picker-range2', 'start_date'),Input('my-date-picker-range2', 'end_date')])
def update_output_div(input_value,start,end):
    connection1 = engine#.connnect()
    print("start=",start,"end=",end,"dt.now=",datetime.now())
    df=pd.read_sql("select * from datatable",connection1)
    #filtered_d = df[df.devId == selected_device]# and ([df.stamp == i] for i in (start,end,timedelta(microseconds=1)))]
    filtered_df = df.loc[(df['stamp'] > start) & (df['stamp'] <= end)]
    #rows = User.query.all()
    print("table filtereddf=",filtered_df.stamp)
    print("table filtereddf=",filtered_df.all)
#    for 
#    filterdf[i]=filtered_df[i].astype(str).str.split(',')
    #return [html.Table(table(rows)
    #filtered_df=filtered_df.convert_dtypes(self: ~FrameOrSeries, infer_objects: bool = True, convert_string: bool = True, convert_integer: bool = True, convert_boolean: bool = True)
    #filtered_df=filtered_df.convert_dtypes()
#    filtered_df=filtered_df.all
    filtered_df=filtered_df.values.tolist()
    return [html.Table(table(filtered_df)
        )]


#@app.callback(Output("download-link", "url"),
#@app.callback(Output("download-link", "url"),
#              [Input("download-link", "className")])
def update_download_link(input_value):
    connection1 = engine
    df=pd.read_sql("select * from datatable",connection1)
    return [html.Table(table(filtered_df)
        )]

#@app.callback(Output("download-link", "data"),
#              [Input("downoad-link", "n_clicks"),Input('my-date-picker-range2', 'start_date'),Input('my-date-picker-range2', 'end_date')])
def update_download_link(input_value,start,end):
  if n_clicks:  
    connection1 = engine
    #df=pd.read_sql_table("select * from datatable",connection1)
    df=pd.read_sql_table("datatable",connection1)
    filtered_df = df.loc[(df['stamp'] > start) & (df['stamp'] <= end)]

    cv = filtered_df.to_csv("data.csv",index=False, encoding='utf-8')
#    cv = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(cv)
    return cv

    
#@app.callback(Output("download-link", "url"),
#@app.callback(Output("download-link", "url"),
#              [Input("downoad-link", "className")])
def update_download_link(input_value):
    connection1 = engine
    df=pd.read_sql("select * from datatable",connection1)
    cv = df.to_csv("data.csv",index=False)#, encoding='utf-8')
    #cv = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(cv)
    return cv

@app.callback(dash.dependencies.Output('url', 'pathname'),
              [dash.dependencies.Input('tabs', 'value')])
def tab_updates_url(value):
    return value
    
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')],
              )
def display_page(pathname):
    if pathname == '/page-2':
        return page_1_table
    elif pathname == '/page-1':
        return page_2_graph
    elif pathname == '/page-3':
        return page_3_read
    elif pathname =='/page-4':
        return page_4_write
    #else:
     #   pathname == '/page-1'
      #  return page_2_graph

        

if __name__ == '__main__':
    app.run_server(debug=True,threaded=True, use_reloader=True)
