from botocore.exceptions import ClientError
import logging
logger = logging.getLogger(__name__)

import boto3, botocore
import os
from django.http import Http404

from django.conf import settings

class s3Bucket:
    def __init__(self, bucket, key, fileName):
        self.bucket= bucket
        self.key= key
        self.fileName= fileName
        self.s3 = boto3.client(
            's3',
            region_name="us-east-1",
            #aws_access_key_id='AKIARJLDNDHB3VFXXTOI',
            #aws_secret_access_key='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'
            aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY
        )

    def uploadFile(self):
        print("\nloading..  from S3 ", self.bucket, self.key)

        try: 
            self.s3.upload_file(self.fileName, self.bucket, self.key)
            print("succefully upload S3  from " + self.bucket + "/" +self.key + " to " + self.fileName)
            return self.fileName
        except ClientError as e:
            logging.error(e)
            return False


    def loadFile(self, overwirte= False):
        print("\nloading..  from S3 ", self.bucket, self.key)

        try:
            self.s3.download_file(self.bucket, self.key, self.fileName)
            print("succefully load S3  from " + self.bucket + "/" +self.key + " to " + self.fileName)
            return self.fileName

        except ClientError as e:
            logger.error(e)
            #raise Http404("Poll does not exist")

            raise Http404(e, "fail loading from S3 " + self.bucket + "/" + self.key + " to " + self.fileName)

