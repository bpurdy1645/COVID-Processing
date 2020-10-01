import boto3
import sys
import json


access_key = 'access_key'
secret_key = 'secret_key'
region_nm = ''
sns_client = boto3.client('sns', aws_access_key_id = access_key, aws_secret_access_key= secret_key, region_name = region_nm)


def post_sns_message_df(df, arn, subject):
    try:
        df_dict = df.to_dict('records')

        for row in df_dict:
            message = json.dumps(row, default=str)
            sns_client.publish(TopicArn = arn, Subject = subject, Message = message)
            print(f"This message has been sent: {message}")

    except Exception as e:
        print("Issue publishing message to SNS Topic: " + str(e))
        sys.exit(1)


def post_sns_message_one(arn, subject, message):
    try:
        sns_client.publish(TopicArn= arn, Subject = subject, Message = message)
        print(f"This message has been sent: {message}")

    except Exception as e:
        print("Issue publishing message to SNS Topic: " + str(e))
        sys.exit(1)

