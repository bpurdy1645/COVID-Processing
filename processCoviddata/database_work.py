import pymysql
import sys
import sns_post

ENDPOINT = "db endpoint"
PORT = 3306
USR = ""
PSWD = ""
REGION = ""
DBNAME = ""

error_sns_arn = 'sns arn
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
        
        
def covid_row_count(schema_nm, table_nm):
    try:
        my_conn = getConnection()
        
        cur = my_conn.cursor()
        sql = "SELECT COUNT(*) FROM " + schema_nm + "." + table_nm
        cur.execute(sql)
        
        query_results = cur.fetchone()
        
        cur.close()
        
        return query_results[0]

    except Exception as e:
        error_message = "Getting Row Count from MySQL failed due to {}".format(e)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, error_message)
        sys.exit(1)
    
    finally:
        my_conn.close()


def max_cases_date(schema_nm, table_nm):
    try:
        my_conn = getConnection()
        
        cur = my_conn.cursor()
        sql = "SELECT MAX(CASES_DT) FROM " + schema_nm + "." + table_nm
        cur.execute(sql)
        
        query_results = cur.fetchone()
        print(f"Max date I see in the DB is {query_results}")
        
        cur.close()
        
        return query_results[0]

    except Exception as e:
        error_message = "Getting Max Cases Date from MySQL failed due to {}".format(e)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, error_message)
        sys.exit(1)
        
    finally:
        my_conn.close()