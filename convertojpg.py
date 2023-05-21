import json
import urllib.parse
import boto3
from io import BytesIO
from PIL import Image
import os
import uuid

print('Loading function')

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    
    # Extract str and convert to dict formatted event message from SQS event message format
    messsage_event = json.loads(event['Records'][0]['body'])
    
    bucket = messsage_event['Records'][0]["s3"]['bucket']['name']
    key = urllib.parse.unquote_plus(messsage_event['Records'][0]["s3"]['object']['key'], encoding='utf-8')
    #print(key)
    filename = key.split('.')[0]
    print(filename)
    
    #print("CONTENT TYPE: " + response['ContentType'])
    # Load and open image from S3
    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    s3_client.download_file(bucket, key, download_path)
    #file_byte_string = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()
    with Image.open(download_path) as image:
        image.convert('RGB').save(download_path + filename + ".jpg","JPEG")


    s3_client.upload_file(download_path, bucket, filename + '.jpg')
    #s3_client.upload_file("/" + filename  + '.jpg', bucket, filename + '.jpeg')
        
    #return response['ContentType']
    return event
  
              