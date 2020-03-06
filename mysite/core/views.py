import os
import json

import logging
logger = logging.getLogger(__name__)
from django.http import HttpResponse

from django.http import Http404
from django.http import HttpResponseServerError
from django.core.exceptions import EmptyResultSet

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.http import JsonResponse
from django.utils import timezone


# from django.contrib.staticfiles import finders
import pandas as pd 

 #db
from database.orm import DBRead

#s3
from aws.s3 import s3Bucket
from aws.ses import SES

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout

import time

from django.conf import settings

# from database.models import Teleconference_transcribe
# from database.serializers import Teleconference_transcribeSerializer

from database.orm import DBRead

from transcibe.pipeline import pipeline



dataTime= {
    "time": timezone.localtime(),
}

# views
class Home(TemplateView):
    template_name = 'home.html'

#logout
def logout_view(request):
    logout(request)
    return render(request,'home.html')

# -----------------------------------------for api-------------------------------------
class Demo(): 

    #/test/
    def test(request):  
        print("\n\n*************************************transcribe test*************************************")

        # data= DBRead().update("demo.wav", "cool test")
        # print(data)

        dataJson= {
            "test1": "test"
        }

        return JsonResponse(dataJson)

    #/test/s3/
    def s3(request):  
        print("\n\n************************************* s3 test*************************************")

        #bucket='thrivee-dev/audiotranscribe'
        bucket=  'thrivee-dev'

        key= 'audiotranscribe/test.wav'

        fileName= 'media/' + key.split('/')[1]
        print(fileName)
        res= s3Bucket(bucket, key, fileName).loadFile()

        data= {
            "s3": res,
        }
        
        return JsonResponse(data)
    
    #/test/db
    def db(request):  
        print("\n\n************************************* db test*************************************")
        
        data= DBRead().ml_test()
        print(data)
        
        data= {
            "db test": data
        }
        
        return JsonResponse(data)

    def ses(request):  
        print("\n\n************************************* ese test*************************************")

        SES().gmail()

        data= {
            "ses": "ses",
        }
        
        return JsonResponse(data)


    #/api/demo
    def demo(request, key):  #s3 key
        print("\n\n*************************************transcription api Service *************************************")

        data= pipeline(key).service()
        
        return JsonResponse(data)

        # df= pd.DataFrame(data, index=[0])
        # return HttpResponse( df.to_html() )
    
    def aws(request, key):  #s3 key
        print("\n\n*************************************transcription api Service *************************************")

        data= pipeline(key).service('aws')
        
        return JsonResponse(data)

        # df= pd.DataFrame(data, index=[0])
        # return HttpResponse( df.to_html() )
          
