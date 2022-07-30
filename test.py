# from flask import Flask

# app = Flask(__name__)


# @app.route('/hello')
# def hello():
#     return 'Hello, World!'


import json
import boto3
import pymysql
from sqlalchemy import create_engine
import pandas as pd

def lambda_handler(event, context):
    send_email_test()
    
def send_email_test():
    
    ses = boto3.client('ses')

    body = """
	    Lambda SES
    """

    ses.send_email(
	    Source = 'pifibab259@galotv.com',
	    Destination = {
		    'ToAddresses': [
			    'wipop51631@galotv.com',
                'pasoyod661@aregods.com'
		    ]
	    },
	    Message = {
		    'Subject': {
			    'Data': 'SES Demo',
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
        'body': json.dumps('Successfully sent email from Lambda using Amazon SES')
    }

# host='database-1.cdyzfzfcsxe4.us-east-2.rds.amazonaws.com'
# port=int(1433)
# user='admin'
# passw='sau97kari'
# database='database-1'

# cnxn_str = ("Driver={SQL Server Native Client 11.0};"
#             "Server=USXXX00345,67800;"
#             "Database=DB02;"
#             "UID=Alex;"
#             "PWD=Alex123;")
# cnxn = pyodbc.connect(cnxn_str)

import pymssql

# connection={
#    'host': 'database-1.cdyzfzfcsxe4.us-east-2.rds.amazonaws.com',
#    'username': 'admin',
#    'password': 'sau97kari',
#    'db': 'database-1' 
# }
# con=pymssql.connect(connection['host'],connection['username'],connection['password'],connection['db'])

# cursor=con.cursor()

# import pyodbc as pydb

# connection = pydb.connect('DRIVER={SQL Server Native Client 11.0};SERVER=database-1.cdyzfzfcsxe4.us-east-2.rds.amazonaws.com,1433;UID=admin;PWD=sau97kari;DATABASE=database-1')

# print("Connecting....")

# connection.close()

def db_test():
    mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=False)
    lst = ['a', 'b', 'c']
    df = pd.DataFrame(lst)
    df.to_sql(name='list', con=mydb, if_exists='replace', index=False)

    return

import pandas as pd
import config

#SQL
import mysql.connector 
from mysql.connector import errorcode
from sqlalchemy import create_engine

lst = ['a', 'b', 'c', 'd']
df = pd.DataFrame(lst)

print(df)

cnx = mysql.connector.connect(
        host = config.host,
        user = config.user,
        password = config.pwd)

print("here")
print(cnx)
cursor = cnx.cursor()
#insert Database Name
db_name = 'cloudprojects_ttt'
print("here 2")

#creates db
# def create_database(cursor, database):
#     try:
#         cursor.execute(
#             "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
#     except mysql.connector.Error as err:
#         print("Failed creating database: {}".format(err))
#         exit(1)


# try:
cursor.execute("USE {}".format('cloudprojects'))
# except mysql.connector.Error as err:
#     print("Database {} does not exists.".format(db_name))
#     if err.errno == errorcode.ER_BAD_DB_ERROR:
#         create_database(cursor, 'cloudprojects')
#         print("Database {} created successfully.".format(db_name))
#         cnx.database = 'cloudprojects'
#     else:
#         print(err)
#         exit(1)

engine = create_engine(f"mysql+mysqlconnector://{config.user}:{config.pwd}@{config.host}/{config.db_name}")

df.to_sql(db_name, con=engine, if_exists='append')


# if __name__ == "__main__":

    # send_email_test()
    # db_test()