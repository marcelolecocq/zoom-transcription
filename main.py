import os
import json

from dotenv import load_dotenv
import assemblyai as aai
import webvtt
import requests
import urllib.request
import numpy as np

import pandas as pd
pd.set_option('display.max_rows', None)
from tabulate import tabulate


from utils.zoom import ZoomClient

load_dotenv()

ZOOM_ACCOUNT_ID = os.environ.get('ZOOM_ACCOUNT_ID')
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET')
aai.settings.api_key = os.environ.get('ASSEMBLYAI_API_KEY')

transcriber = aai.Transcriber()

client = ZoomClient(account_id=ZOOM_ACCOUNT_ID, client_id=ZOOM_CLIENT_ID, client_secret=ZOOM_CLIENT_SECRET)

#We would need a look here with usernames, and iterate for the number of meetings (index-1)
#recs = client.get_recordings('marcelo@io-sphere.io')
list_of_meeting_hosts = ['marcelo@io-sphere.io'
                         ,'steph@io-sphere.io'
                         ,'harry@io-sphere.io'
                         ,'eben@io-sphere.io'
                         ,'greg@io-sphere.io']

recs = client.get_recordings_old('steph@io-sphere.io', '2024-01-08','2024-02-18')
# print(recs)
# print(type(recs))
#print(recs['meetings'][0]['id'])
#print(recs['meetings'][0]['recording_files'][2])
df_final=[]
if recs['meetings']: 
    for i in range(len(recs['meetings'])):
        rec_id = recs['meetings'][i]['id']
        #trans_id=recs['meetings'][0]['recording_files'][2]['id']
        my_url = client.get_download_url(rec_id)
        with urllib.request.urlopen(my_url) as f:
            html = f.read().decode('utf-8')
            #print(html)    

            text= html
            for i in range(0,10):
                j=str(i)
                text = text.replace(j+":", "0"+j+":")
                text = text.replace("."+j+" ", ".00"+j)
                text = text.replace(":"+j+".", ":0"+j+".")
                for k in range(0,10):
                    l=str(k)
                    text = text.replace("."+j+l+" ", ".0"+j+l)
                    text = text.replace("."+j+l+"\n", ".0"+j+l+"\n")
                    text = text.replace(":"+j+"0"+l+":",":"+j+l+":")

            for i in range(0,10):
                j=str(i)
                for k in range(0,10):
                    l=str(k)
                    text = text.replace(":"+j+"0"+l+":",":"+j+l+":")
                    
            for i in range(0,10):
                j=str(i)
                text = text.replace("."+j+"\n",".00"+j+"\n")

            cleanedVTT=text.split(".", 1)[0]+".vtt"
            f = open(cleanedVTT, "w")
            f.write(text)
            f.close()   

            with open(cleanedVTT) as f:
                cleanedtext = f.read()

            #print(cleanedtext)
            import webvtt
            start=[]
            end=[]
            text=[]
            speaker=[]
            for caption in webvtt.read(cleanedVTT):
                start.append(caption.start)
                end.append(caption.end)
                text.append(caption.text)
                speaker.append(caption.raw_text)

            df = pd.DataFrame(list(zip(start,end,text,speaker)), columns = ['StartTime', 'EndTime',"Text","Speaker"])
            
            df_final.append(df) 
            #print(f"total time spoken =  '{df['time_delta'].sum()}'")
            

else:
    print('No meetings to transcribe.')

df = pd.concat(df_final, ignore_index=True)
df = df[(df['Text'].str.contains(":"))] # removes rows that dont contain a ":" delimiter
print(df)
listx=df['Speaker'].str.split('>', n=1, expand=True)
df["Speaker"]=listx[0]
df["Speaker"]=(df["Speaker"].str.replace("<v ",""))
df["Speaker"]=df["Speaker"].str.split(":").str[0]
df["Text"]=df["Text"].str.split(":").str[1]
df['StartTime'] = pd.to_datetime(df['StartTime'])
df['EndTime'] = pd.to_datetime(df['EndTime'])
df['time_delta'] = (df['EndTime']-df['StartTime'])/ np.timedelta64(1, 's')
df.groupby(['Speaker'], sort=True)['time_delta'].sum()

print(df.head())

    

#df.tail(10)
#print(speaker)
# #print(tabulate(df.head(), headers='keys', tablefmt='psql'))

# stephe_record = client.get_recordings_old('harry@io-sphere.io', '2024-01-20','2024-01-30')
# #print(stephe_record['meetings'])
# print(len(stephe_record['meetings']))
# print(len(stephe_record['meetings']))
# print(json.dumps(stephe_record['meetings'][0], indent=4))
 
import plotly.graph_objects as go
df_group = df.groupby(['Speaker'], as_index=False).agg({'time_delta': 'sum'})
fig = go.Figure(go.Bar(
            x=df_group['time_delta'],
            y=df_group['Speaker'],
            orientation='h'))
fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.show() 


# stephe_record = client.get_recordings_old('steph@io-sphere.io', '2024-01-20','2024-01-30')
# #print(stephe_record['meetings'])
# print(len(stephe_record['meetings']))
# print(len(stephe_record['meetings']))
# print(json.dumps(stephe_record['meetings'][0], indent=4))
 