from django.conf import settings
from .models import Ml_test
from .serializers import Ml_testSerializer

from .models import Teleconference_transcribe
from .serializers import Teleconference_transcribeSerializer
from django.http import Http404

import pandas as pd 

class DBRead():
    def __init__(self):
        self.print= None
     
    def ml_test(self, name="hunter"):
        try:
            e= Ml_test.objects.filter( name= name )
        except:
            raise Http404("can not access to mysql")

        serializer = Ml_testSerializer( e, many=True)
        
        if not serializer.data:
            raise Http404("filename can not found in table")

        return serializer.data


    def update(self, filename=None, transcription=None):
        try:
            e= Teleconference_transcribe.objects.filter( filename= filename )
        except:
            raise Http404("can not access to mysql")

        serializer = Teleconference_transcribeSerializer( e, many=True)
        
        if not serializer.data:
            raise Http404("filename can not found in table")

        row= e.update(transcription_baseline= transcription)
        print("successfully update db ")

        return serializer.data
     








         
 #print(timeslot)

        # today= datetime.date.today() 
        # TimeslotToday= Timeslot.objects.filter( start_date__range=(today, today + datetime.timedelta(days=1)) )
        # print("TimeslotToday:  ",TimeslotToday)

        # minute = datetime.timedelta(minutes=500)
        # today= datetime.date.today() 
        # now= datetime.datetime.now()
     

        # print("st    ", datetime.datetime(2019, 11, 15, 15, 30) )
        # x=              datetime.datetime.utcnow()
        # x=              datetime.datetime(2019, 11, 15, 16, 30) 
        # x= now
        # print("xx    ", x )
        # print("ed    ", datetime.datetime(2019, 11, 15, 17, 30))

     
        #inSlot_ = Timeslot.objects.filter(start_date__lt= x, end_date__gt= x)

        #inSlot= Timeslot.objects.filter( start_date__lt= now + minute ).filter( end_date__gt= now - minute )

        #inSlot= Timeslot.objects.filter( start_date__lt= now ).filter( end_date__gt= now ) # utc

        # TimeslotToday= Timeslot.objects.filter( start_date__range=(today, today + datetime.timedelta(days=1)) )
        # print("TimeslotToday:  ",TimeslotToday)
        #2019-11-15 15:30:00  -  2019-11-15 16:30:00