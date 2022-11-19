from constant import df_order_data, df_fraud_order_data
from data_processing.cleaning import change_col_names_and_delete_some, change_date_to_datetime_type,\
    clean_extracted_csv


if __name__ == '__main__':
    change_col_names_and_delete_some(df=df_order_data, total_order_data=True)
    change_col_names_and_delete_some(df=df_fraud_order_data, total_order_data=False)
    # a = change_col_names_and_delete_some(df=df_fraud_order_data, total_order_data=False)

    #
    # a = change_date_to_datetime_type(True)
    #
    # print(a.dtypes)

    # a = clean_extracted_csv(total_order_data=False)
    b = clean_extracted_csv(total_order_data=True)
    # print(a.order_date[:15])
