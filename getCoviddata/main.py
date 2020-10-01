import json
import pymysql
import sns_post


ENDPOINT = "db endpoint"
PORT = port number
USR = ""
PSWD = ""
DBNAME = ""


#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#' My SNS Information for Error Tracking '
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
error_sns_arn = 'sns arn'
error_sns_subject = 'sns subject'


#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#' Square away my connection to RDS '
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def getConnection():
    try:
        conn = pymysql.connect(ENDPOINT, user=USR, passwd=PSWD, db=DBNAME, connect_timeout=3)
        return conn
        
    except Exception as e:
            error_message = "Error connecting to MySQL Database {}".format(e)
            print(error_message)
            sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, error_message)
            sys.exit(1)

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#' Main Handler '
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def main_handler(event, context):
    try:
        for record in event['Records']:
            
            covid_data = json.loads(record["body"])
            
            message_details = json.loads(covid_data['Message'])
            
            sql = "INSERT INTO covid.covid_cases VALUES ('{0}', {1}, {2}, {3})".format(message_details["date"][0:10], message_details["cases"], message_details["deaths"], message_details["recovered"])
            
            my_conn = getConnection()
            cur = my_conn.cursor()
            cur.execute(sql)
            
            my_conn.commit()
            cur.close()            

    except Exception as e:
        error_message = "Inserting Rows into MySQL failed due to {}".format(e)
        print(error_message)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, error_message)
        sys.exit(1)
        
    finally:
        my_conn.close()        