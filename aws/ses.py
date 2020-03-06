#email
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

import boto3
from botocore.exceptions import ClientError

class SES:
    def __init__(self):
        print("\n\n*****************************************SES service*****************************************")

    def gmail(self, content=None):
        SENDER= 'bitaihang@gmail.com'
        RECIPIENT= 'bitaihang@gmail.com'

        if not content:
            content= {}
            content['SUBJECT']= "gmail SUBJECT"
            content['BODY_TEXT']= "gmail BODY_TEXT"
            content['BODY_HTML']= "gmail BODY_HTML"

        SUBJECT= content['SUBJECT']
        BODY_TEXT= content['BODY_TEXT']
        BODY_HTML= content['BODY_HTML']

        msg = EmailMultiAlternatives( SUBJECT, BODY_TEXT, SENDER, [ RECIPIENT ] )
        msg.attach_alternative(BODY_HTML, "text/html")
        msg.send()
