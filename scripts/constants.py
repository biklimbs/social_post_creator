"""
This file contains all CONSTANT identifiers
"""
import os
HOME_PATH=os.path.dirname(os.path.realpath(__file__))+"/"

#---Luminati credentials---
USERNAME='lum-customer-hl_6db6f10b-zone-static-route_err-pass_dyn'
PASSWORD='27mn831qzkm0'
PORT=22225

#---Server credentials---
HOST= "spark.vmokshagroup.com"
USER="spark"
PASSWORD="Power@1234"
SOURCE_DATABASE='genieali'

#---Tables---
COUNTRY_TABLE="p_country"
STATE_TABLE="p_state"
CITY_TABLE="p_city"
S3_IMAGE_URL_TABLE="s_s3_image_url"


#---Sql queries---
COUNTRY_QUERY='SELECT *  FROM '+COUNTRY_TABLE
STATE_QUERY='SELECT *  FROM '+STATE_TABLE
CITY_QUERY='SELECT *  FROM '+CITY_TABLE
SQL_QUOTE="\""

#---constant variable---
#FILENAME_UPLOAD="best-ugadi-wishes-and-messages.jpg"
BUCKET_NAME="vmoksha-ali"
UPLOAD_FOLDER="./uploads"

#---Config file name---
CONFIG_FILENAME=HOME_PATH+'credential.config'