import json
import load_data
import transform_data
import database_work
import sns_post


def main_handler(event, context):
    
    ''''''''''''''''''''''''''''''''''''''
    # Get my Panda Dataframes populated
    ''''''''''''''''''''''''''''''''''''''
    print('About to load data')
    df_nycovid_load = load_data.url_to_dataframe('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
    df_jhrec_load = load_data.url_to_dataframe('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv?opt_id=oeu1597168528396r0.6261539629653985')
    
    ''''''''''''''''''''''''''''''''''''''
    # Rename any necessary columns
    ''''''''''''''''''''''''''''''''''''''
    print('About to rename data')
    transform_data.rename_columns(df_nycovid_load)
    transform_data.rename_columns(df_jhrec_load)
    
    ''''''''''''''''''''''''''''''''''''''
    # Reduce Dataframe down to US data only
    ''''''''''''''''''''''''''''''''''''''
    print('About to remove foreign data')
    df_jhrec_us_only = transform_data.remove_foreign_data(df_jhrec_load)
    
    ''''''''''''''''''''''''''''''''''''''
    # Check our Data Types and make sure our data is what we expect it to be
    ''''''''''''''''''''''''''''''''''''''
    print('About to check data types')
    df_nycovid_checked = transform_data.check_data_types(df_nycovid_load)
    df_jhrec_dt_checked = transform_data.check_data_types(df_jhrec_us_only)
    
    ''''''''''''''''''''''''''''''''''''''
    # Merge our Dataframes
    ''''''''''''''''''''''''''''''''''''''
    print('About to merge dataframes')
    df_covid_complete = transform_data.merge_dataframes(df_nycovid_checked, df_jhrec_dt_checked, 'date')
    
    ''''''''''''''''''''''''''''''''''''''
    # Check rows in Aurora MySQL
    # Push necessary data to SNS
    ''''''''''''''''''''''''''''''''''''''
    arn = 'sns arn'
    subject = 'sns subject'
    
    covid_row_count = database_work.covid_row_count('covid', 'covid_cases')
    
    if covid_row_count == 0:
        print("0 rows in the database, need to insert entire dataframe")
        sns_post.post_sns_message_df(df_covid_complete, arn, subject)
    
    else:
        max_covid_date = database_work.max_cases_date('covid', 'covid_cases')
            
        df_to_sns = transform_data.filter_df_by_date(df_covid_complete, max_covid_date)
        
        if not df_to_sns.empty:
            sns_post.post_sns_message_df(df_to_sns, arn, subject)
        else:
            print("Dataframe is Empty")