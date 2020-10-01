import pandas as pd
import sys
import sns_post

error_sns_arn = 'sns arn'
error_sns_subject = 'sns subject'


def rename_columns(df):
    try:
        col_names = df.columns

        for cols in col_names:
            if cols == 'Date':
                df.rename(columns={'Date': 'date'}, inplace=True)

            if cols == 'Recovered':
                df.rename(columns={'Recovered': 'recovered'}, inplace=True)

    except Exception as e:
        message = "Renaming of Columns failed due to {}".format(e)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, message)
        sys.exit(1)


def check_data_types(df):
    try:
        col_names = df.columns

        for cols in col_names:
            if cols == 'date' and df.dtypes[cols] != 'datetime64[ns]':
                df['date'] = df['date'].astype('datetime64[ns]')
            elif cols in ['cases', 'deaths', 'recovered'] and df.dtypes[cols] != 'float64':
                df[cols] = df[cols].astype('float64')

        return df

    except Exception as e:
        message = "Checking Data Types failed due to {}".format(e)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, message)
        sys.exit(1)


def remove_foreign_data(df):
    check_cols = ['Country/Region', 'date', 'recovered']

    try:
        col_names = df.columns
        result = all(elem in col_names for elem in check_cols)

        if result:
            df_us = df[df['Country/Region'] == 'US'][['date', 'recovered']]
            return df_us

    except Exception as e:
        message = "Removing foreign data failed due to {}".format(e)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, message)
        sys.exit(1)


def filter_df_by_date(df, max_date):

    try:
        max_date = pd.to_datetime(max_date)
        df_date = df[df['date'] > max_date]
        
        return df_date

    except Exception as e:
        message = "Filtering Dataframe by Data failed due to {}".format(e)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, message)
        sys.exit(1)


def merge_dataframes(left_df, right_df, join_col):
    try:
        df_join = pd.merge(left_df, right_df, on=join_col, how='left')
        return df_join

    except Exception as e:
        message = "Merging Dataframes failed due to {}".format(e)
        sns_post.post_sns_message_one(error_sns_arn, error_sns_subject, message)
        sys.exit(1)
