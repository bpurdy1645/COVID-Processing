import pandas as pd
import sys
import sns_post

error_sns_arn = 'sns arn'
error_sns_subject = 'sns subject'


def url_to_dataframe(url):
    try:
        df = pd.read_csv(url)
        return df

    except Exception as e:
        error_message = "Getting Data loaded into our Dataframes failed due to {}".format(e)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, error_message)
        sys.exit(1)
