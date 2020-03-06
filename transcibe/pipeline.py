import os
from database.orm import DBRead
from django.shortcuts import render
import json
import requests
from django.conf import settings
from aws.s3 import s3Bucket
import time
from django.http import Http404
import datetime

from pydub import AudioSegment as am
from transcibe.baseline import baseline
from aws.transcribe import aws


class pipeline():

    def __init__(self, key):# key(filename): ffd2366229cc0d059cf1ae09c54d7b6c.wav
        print("\n\telepathy Service init")

        self.key= key
        self.name= key.split(".")[0]

        settings.SESSION_ID += 1
        self.keyout= str(settings.SESSION_ID) + '_' + self.name + ".wav"

        self.data= {
            "text": "",
            "s3_bucket": settings.BUCKET,
            "s3_key": settings.PREKEY + '/' + key,
            "server": "",
            "jobSession": settings.SESSION_ID,
            "time": "",
        }

    def downloadS3(self):
        print("\nloadS3...")

        #key= self.key
        #key= 'test1.wav'
        bucket=  settings.BUCKET

        key= settings.PREKEY + '/' + self.key
        #fileName= 'media/' + self.key
        path= "media/" + self.keyout
        print(path)

        s3Bucket(bucket, key, path).loadFile()
        
        self.filter(path)

        return path

    def filter(self, path, sample_rate= 16000, channel= 1):
        print(path)
        audio = am.from_file(path)
        audio = audio.set_frame_rate(sample_rate)
        audio = audio.set_channels(channel)
        print("channel", channel)
        print("sample_rate", sample_rate)
        audio.export( path, format='wav')

    def clearInput(self):
        print("\nclearInput...")
        
        folder= "media/" + str(settings.SESSION_ID)+ "*"
        cmd= 'sudo rm -r ' + folder
        print("cmd: ", cmd)

        try:
            os.system(cmd)
        except:
            raise Http404("clearInput cmd not working")

        return True

    def service(self, server= 'google web api'):

        t1= datetime.datetime.now()
        path= self.downloadS3() #load audio from s3
        self.filter(path)

        if server== 'google web api':
            text, t21= baseline(self.keyout).text()

        if server== 'aws':
            text, t21=aws(self.keyout).text()

        self.data['text']= text
        self.clearInput()

        t2=  datetime.datetime.now()
        t21 = str( round((t2 - t1).total_seconds(), 2) ) + 's'
        self.data['time']= t21
        self.data['server']= server
        self.data['server']= server

        print("\nsuccessfully...")

        return self.data