import os
import json
from datetime import datetime

from flask import Flask, render_template, request
import boto3


app = Flask(__name__)

S3_BUCKET = "saugat"
from_email = "cloudcomputing@webapp.com"
# config_set_name = os.environ["SES_CONFIG_SET_NAME"]
config_set_name = "config_set.yaml"


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

        send_email(all_emails, s3_URI)

        #   f.save(secure_filename(f.filename))
        return 'All files uploaded successfully'
		
def s3_upload(filepath, filename):
    # connect to s3
    s3 = boto3.client('s3')

    # upload to s3
    s3.upload_file(filepath, S3_BUCKET, str(filename))

    # s3 URI
    s3_URI = f"https://s3.us-east-2.amazonaws.com/{S3_BUCKET}/{filename}"

    return s3_URI





def send_email(emails, s3_URI):
    client = boto3.client('ses')

    body_html = f"""<html>
        <head></head>
        <body>
          <h2>Link to uploaded file: {s3_URI}</h2>
          <br/>
        </body>
        </html>
        """

    email_message = {
        'Body': {
            'Html': {
                'Charset': 'utf-8',
                'Data': body_html,
            },
        },
        'Subject': {
            'Charset': 'utf-8',
            'Data': "Cloud Computing Course Project",
        },
    }

    ses_response = client.send_email(
        Destination={
            'ToAddresses': emails,
        },
        Message=email_message,
        Source=from_email,
        ConfigurationSetName=config_set_name,
    )

    print(f"ses response id received: {response['MessageId']}.")


if __name__ == '__main__':
   app.run(port=7000, debug = True)