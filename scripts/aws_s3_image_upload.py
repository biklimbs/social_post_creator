"""
This script uploads image file to aws s3 and store s3 url to mysql database.
"""
#---standard library---
import os,sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
from time import sleep
from datetime import datetime
import re
import warnings
warnings.filterwarnings("ignore")

#---Third party library---
import pymysql.cursors
from termcolor import colored
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
import glob
from configparser import ConfigParser

#---Local library---
from logger_config import *
import logger_config
from constants import *
from sql_helper import *
from read_configuration import *

#---Configuring log filename---
log_file=os.path.splitext(os.path.basename(__file__))[0]+".log"
log = logger_config.configure_logger('default', ""+DIR+""+LOG_DIR+"/"+log_file+"")

#---Developer details---
__author__="Bikash Limboo"
__maintainer__="Bikash Limboo"

#---Returns s3 object---
def create_s3_object(parser):
    """
    This function takes "ACCESS_KEY" and "SECRET_KEY" and creates an s3 object
    and returns it.
    """
    return boto3.resource('s3', aws_access_key_id=parser.get('aws_credential','ACCESS_KEY'),aws_secret_access_key=parser.get('aws_credential','SECRET_KEY'))

#---Uploads image file to s3 and returns url---
def upload_to_aws_s3(s3,bucket_name):
    """
    This function tahes "s3" object and "bucket_name" as parameter.
    Uploads specified image file to s3 and returns corresponding url.
    """
    try:
        bucket_obj = s3.Bucket(name=bucket_name)
        FILEPATH_NAME=get_file()
        img_object = bucket_obj.Object(FILEPATH_NAME)
        FILENAME_UPLOAD = os.path.basename(FILEPATH_NAME) 
        img_object.upload_file(FILENAME_UPLOAD)
        image_url="https://"+bucket_name+".s3.amazonaws.com/"+FILENAME_UPLOAD
        log.info("File uploaded successfully to s3")
        return image_url
        
    except Exception as e:
        log.error(str(e))
        return None

#---Inserts into database---
def insert_into_db(image_url):
    connection=connect_to_db()
    local_time=datetime.now().strftime ("%Y-%m-%d %H:%M:%S")#Get current datetime.
    with connection.cursor() as cursor:
        try:
            sql = "INSERT INTO "+S3_IMAGE_URL_TABLE+" (`s3_url`, `local_time`) values(%s,%s)"
            data=(str(image_url),str(local_time))
            cursor.execute(sql,data)
            connection.commit()
            log.info("Inserting into table")
        except pymysql.err.IntegrityError as e:
            log.error(str(e))
        except Exception as e:
            log.error(str(e))	
    connection.close()
    return "updated Successfully"

#---Returns filename from upload folder---
def get_file():
    """
    This function select a single image file from "uploads" folder.
    """
    with os.scandir('./uploads/') as entries:
        for entry in entries:
            return entry.name

#---Upload image to s3---
def s3_upload():
    try:
        parser=read_config_file()
        s3 = create_s3_object(parser)
        image_url = upload_to_aws_s3(s3,BUCKET_NAME)
        if image_url:
            insert_status=insert_into_db(image_url)
            log.info(insert_status)
            
        else:
            log.error("Error while uploading ")
    except Exception as e:
        log.error(colored(str(e),"red"))
    return image_url



#s3_upload()
'''
#---Main function---
def main():
    try:
        s3 = create_s3_object()
        image_url = upload_to_aws_s3(s3,BUCKET_NAME)
        if image_url:
            insert_status=insert_into_db(image_url)
            log.info(insert_status)
        else:
            log.error("Error while uploading ")
    except Exception as e:
        log.error(colored(str(e),"red"))
    
#---Main function called---
if __name__=="__main__":
	main()
'''