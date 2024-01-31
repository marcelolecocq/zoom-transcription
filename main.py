import os

from dotenv import load_dotenv
import assemblyai as aai
import webvtt
import requests
import urllib.request
import numpy as np

import pandas as pd
from tabulate import tabulate


from utils.zoom import ZoomClient

load_dotenv()

ZOOM_ACCOUNT_ID = os.environ.get('ZOOM_ACCOUNT_ID')
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET')
aai.settings.api_key = os.environ.get('ASSEMBLYAI_API_KEY')

transcriber = aai.Transcriber()

client = ZoomClient(account_id=ZOOM_ACCOUNT_ID, client_id=ZOOM_CLIENT_ID, client_secret=ZOOM_CLIENT_SECRET)

recs = client.get_recordings('steph@io-sphere.io')
#print(recs['meetings'][0]['id'])
#print(recs['meetings'][0]['recording_files'][2])
if recs['meetings']:  
    rec_id = recs['meetings'][0]['id']
    #trans_id=recs['meetings'][0]['recording_files'][2]['id']
    my_url = client.get_download_url(rec_id)
    #trans_url =client.get_download_url(trans_id)
    
#     # transcript = transcriber.transcribe(my_url)
#     # print(transcript.text)
#     # with open('transcript.txt', 'w') as f:
#     #     f.write(transcript.text)
else:
    print('No meetings to transcribe.')

# Adding the vtt transformer

# import urllib.request
# query_parameters = {"downloadformat": "vtt"}
# response = requests.get(my_url, params=query_parameters)
# print(type(response.content))

# with open(response.content) as f:
#     corpus = f.read()

#print(text)
#print(response.content)
with urllib.request.urlopen(my_url) as f:
    html = f.read().decode('utf-8')
print(html)    
# start=[]
# end=[]
# text=[]
# speaker=[]
# for caption in webvtt.read(response.content):
#     start.append(caption.start)
#     end.append(caption.end)
#     text.append(caption.text)
#     speaker.append(caption.raw_text)


# #print(type(my_url))
# print(html)

#trans_url
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

print(cleanedtext)
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
listx=df['Speaker'].str.split('>', n=1, expand=True)
df["Speaker"]=listx[0]
df["Speaker"]=(df["Speaker"].str.replace("<v ",""))
df["Speaker"]=df["Speaker"].str.split(":").str[0]
df["Text"]=df["Text"].str.split(":").str[1]
df['StartTime'] = pd.to_datetime(df['StartTime'])
df['EndTime'] = pd.to_datetime(df['EndTime'])
df['time_delta'] = (df['EndTime']-df['StartTime'])/ np.timedelta64(1, 's')
print(f"total time spoken =  '{df['time_delta'].sum()}'")

df.tail(10)
#print(speaker)
# #print(tabulate(df.head(), headers='keys', tablefmt='psql'))
