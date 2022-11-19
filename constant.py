import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")


def read_target_file():
    return pd.read_excel('APAC Growth Data Analyst Test.xlsx', sheet_name='Order Data'),\
           pd.read_excel('APAC Growth Data Analyst Test.xlsx', sheet_name='Fraud Orders Data')


df_order_data, df_fraud_order_data = read_target_file()


if __name__ == '__main__':
    df_order_data, df_fraud_order_data = read_target_file()
    print(df_order_data)
    print(df_fraud_order_data)