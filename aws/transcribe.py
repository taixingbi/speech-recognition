from botocore.exceptions import ClientError
import boto3, botocore
import os
from django.http import Http404

from django.conf import settings
import time
from aws.s3 import s3Bucket

import json
import datetime

class aws:
    def __init__(self, keyName= '101_test1.wav'):
        print("\n-----------------------------------aws...-----------------------------------------------")
        #print(jobId)

        jobName= keyName.split('_')[1]
        self.transcriptionJobName= keyName.split('.')[0] # test1

        self.jobName= jobName
        self.name= jobName.split('.')[0] # test1
        self.ext= jobName.split('.')[1] # wav, mp3


        self.inBucket= 'thrivee-dev'
        self.inKey= 'audiotranscribe/'  + self.jobName  #'audiotranscribe/test1.wav'

        self.outBucket= 'aws-transcribe-test-tmp'

        print(self.inBucket)
        print(self.inKey)

        self.client = boto3.client(
            'transcribe',
            region_name="us-east-1",
            aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY
        )

    def text(self):
        print("text..")
    
        t1= datetime.datetime.now()

        try:
            res = self.client.delete_transcription_job(
                TranscriptionJobName= self.transcriptionJobName
            )
            print("\ndelete_transcription_job: ", res)
        except:
            print(self.name, "The requested job couldn't be found" )

    #try:
        print("\nclient.start_transcription_job...")
        self.client.start_transcription_job(
            TranscriptionJobName= self.transcriptionJobName,
            LanguageCode= "en-US",
            MediaFormat= self.ext,
            Media= {
                #'MediaFileUri':  'https://s3.us-east-1.amazonaws.com/thrivee-dev/audiotranscribe/test1.wav'
                'MediaFileUri':  'https://s3.us-east-1.amazonaws.com/' + self.inBucket + '/' + self.inKey
            },
            OutputBucketName= self.outBucket,
            #OutputBucketName= 'aws-transcribe-test-tmp',

        )
    # except:
    #     return "Error: client.start_transcription_job", ""

        print("\nget_transcription_job...")
        while True:
            res = self.client.get_transcription_job(
                TranscriptionJobName= self.transcriptionJobName
            )

            if res['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED': 
                print("\nCOMPLETED", res)
                break

            if res['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED': 
                print(res)               
                return "Error: client.get_transcription_job->TranscriptionJobStatus FAILED", ""

            #print(res)
            time.sleep(3)

        t2=  datetime.datetime.now()
        t21 = str( round((t2 - t1).total_seconds(), 2) ) + 's'
        print( t21 )

        if not self.downloadOutJson():
            return "Error: downloadS3 failed"

        text= self.readJson()
        
        print("*********************** AWS text ***********************")
        print(text)
        print("********************************************************")

        return text, t21

    def downloadOutJson(self):
        key= self.transcriptionJobName + '.json'
        fileName= 'media/' + key
        print(self.outBucket, key)
        print(fileName)
        res= s3Bucket(self.outBucket, key, fileName).loadFile()

        return True

    def readJson(self):
        print("\nreadJson..")

        f= 'media/' + self.transcriptionJobName + '.json'
        with open(f) as f:
            data = json.load(f)

        text= data['results']['transcripts'][0]['transcript']
        print(text)
        return text



if __name__ == "__main__": 
    jobId= '101'
    text, t21= aws(jobId).text()

