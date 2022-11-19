import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import warnings
import numpy as np

warnings.filterwarnings("ignore")


def check_distribution(total_order_data=False):
    if total_order_data:
        df = pd.read_csv(os.path.join(os.getcwd(), 'order_data.csv'))
    else:
        df = pd.read_csv(os.path.join(os.getcwd(), 'fraud_order_data.csv'))

    data_dis = df.merchant.hist(bins=50)
    plt.show()


def plot_first_graph(column_name='status'):
    # plot pie
    df_total = pd.read_csv(os.path.join(os.getcwd(), 'order_data.csv'))
    df_fraud = pd.read_csv(os.path.join(os.getcwd(), 'fraud_order_data.csv'))

    # subplot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 8))

    ax1.bar(df_total[column_name].value_counts().index, df_total[column_name].value_counts().values)
    ax2.bar(df_fraud[column_name].value_counts().index, df_fraud[column_name].value_counts().values)

    ax1.set_title('Total Data')
    ax2.set_title('Fraud Data')

    ax1.tick_params(rotation=30)
    ax2.tick_params(rotation=30)

    fig.suptitle(f'{column_name}')
    plt.show()


def manual_filter(filter_number=3):
    threshold = {
        'status': ['good'],
        'Grade': ['A'],
        'price': [92900],  # larger than this is suspecious
        'shipping_prefecture': ['big_city'],
        'Domain': ['other'],
        'canceller': ['system_canceller'],
        'payment_method': ['―'],
    }
    df_total = pd.read_csv(os.path.join(os.getcwd(), 'order_data.csv'))
    # df_fraud = pd.read_csv(os.path.join(os.getcwd(), 'fraud_order_data.csv'))

    # filter each row and give it a new column of classification
    for row in df_total.iterrows():
        score = 0
        for column in threshold.keys():
            if column == 'price':
                if row[1][column] > threshold[column][0]:
                    score += 1
            elif column == 'Domain' or column == 'canceller':
                if row[1][column] == 'other' or row[1][column] == 'system_canceller':
                    score += 2
            elif row[1][column] in threshold[column]:
                score += 1
        if score >= filter_number:
            df_total.loc[row[0], 'classification'] = 'suspecious'
        else:
            df_total.loc[row[0], 'classification'] = 'normal'

    print(df_total['classification'].value_counts())

    df_total.to_csv(f'order_data_with_classification_manual_using_{filter_number}.csv', index=False)


if __name__ == '__main__':
    # check_distribution(total_order_data=False)
    # check_distribution(total_order_data=True)

    for i in range(3, 6):
        manual_filter(filter_number=i)

