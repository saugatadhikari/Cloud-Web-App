import os
import json
from datetime import datetime

from flask import Flask, render_template, request
import boto3
import pandas as pd

#SQL
import mysql.connector 
from mysql.connector import errorcode
from sqlalchemy import create_engine

import config

app = Flask(__name__)

S3_BUCKET = "saugat"
from_email = "cloudcomputing@webapp.com"

# SQL connection
CONNECTION = mysql.connector.connect(
        host = config.host,
        user = config.user,
        password = config.pwd)

CURSOR = CONNECTION.cursor()
TABLE_NAME = 'filenames_table'

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/fileupload')
def template():
   return render_template('frontend.html')
	

@app.route('/fileuploader', methods = ['GET', 'POST'])
def file_uploader():
    if request.method == 'POST':
        f = request.files['file']
        txt = request.form['emails']
        all_emails = txt.split(",")

        if len(all_emails) > 5:
            return "Error!!! Only 5 emails allowed"
        print(f.filename)
        print(txt.split(","))

        tmp_folder = "./tmp"
        if not os.path.exists(tmp_folder):
            os.mkdir(tmp_folder)

        tmp_filepath = os.path.join(tmp_folder, str(f.filename))
        f.save(tmp_filepath)

        # upload file to s3 bucket and get URI
        s3_URI = s3_upload(tmp_filepath, str(f.filename))
        print('File uploaded successfully')

        try:
            send_email_test(all_emails, s3_URI)
        except:
            return 'Unverified email addresses: please check!'

        # Store filenames to Database
        try:
            CURSOR.execute("USE {}".format(config.db_name))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                db_create(CURSOR, config.db_name)
                CONNECTION.database = config.db_name
            else:
                exit(1)
        
        conn_engine = create_engine(f"mysql+mysqlconnector://{config.user}:{config.pwd}@{config.host}/{config.db_name}")

        df = pd.DataFrame([{'filename': f.filename}])
        df.to_sql(TABLE_NAME, con=conn_engine, if_exists='append')

        return 'Emails sent successfully'
		
def s3_upload(filepath, filename):
    # connect to s3
    s3 = boto3.client('s3')

    # upload to s3
    s3.upload_file(filepath, S3_BUCKET, str(filename))

    # s3 URI
    s3_URI = f"https://s3.us-east-2.amazonaws.com/{S3_BUCKET}/{filename}"

    return s3_URI


def lambda_handler(event, context):
    send_email_test()
    
def send_email_test(all_emails, s3_uri):
    
    ses = boto3.client('ses')

    body = f"""
	    Link of file uploaded to S3 bucket: {s3_uri}
    """

    ses.send_email(
	    Source = 'pifibab259@galotv.com',
	    Destination = {
		    'ToAddresses': all_emails
	    },
	    Message = {
		    'Subject': {
			    'Data': 'S3 File URI',
			    'Charset': 'UTF-8'
		    },
		    'Body': {
			    'Text':{
				    'Data': body,
				    'Charset': 'UTF-8'
			    }
		    }
	    }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Email successfully sent!')
    }

def db_create(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print(f"Database could not be created. Error: {err}")
        exit(1)
    
    return

if __name__ == '__main__':
   app.run(port=7000, debug = True)