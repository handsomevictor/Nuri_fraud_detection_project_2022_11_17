import pandas as pd
import os
import numpy as np
import datetime

from constant import df_order_data, df_fraud_order_data


def delete_apparently_useless_columns(df):
    """
    So far, shipping_company is useless for sure
    """
    try:
        df = df.drop(columns=['shipping_company'])
    except KeyError:
        pass
    return df


def delete_apparently_wrong_rows(df):
    # first delete the rows in Grade does not have ABCD
    df = df[df['Grade'].str.contains('A|B|C|D')]

    # delete the rows in order_date, payment_date, shipping_date, shipping_mail_sent_date that doesn't have a date
    # df = df[df['order_date'].astype(str).str.contains('\d{4}-\d{2}-\d{2} \d{2}:\d{2}')]
    # print(df[['order_date', 'payment_date', 'shipping_date']])
    # df = df[df['payment_date'].astype(str).str.contains('\d{4}-\d{2}-\d{2} \d{2}:\d{2}')]
    # df = df[df['shipping_date'].astype(str).str.contains('\d{4}-\d{2}-\d{2} \d{2}:\d{2}')]

    try:
        df = df[df['shipping_mail_sent_date'].astype(str).str.contains('\d{4}-\d{2}-\d{2} \d{2}:\d{2}')]
    except KeyError:
        pass
    return df


def change_col_names_and_delete_some(df, total_order_data=True):
    mapping_rule = {'マーチャント': 'merchant',
                    '注文番号': 'id',
                    '対応状況(名称)': 'status',
                    '受注日': 'order_date',
                    '入金日': 'payment_date',
                    '発送日': 'shipping_date',
                    '商品ID': 'product_id',
                    '商品名': 'product_name',
                    '価格': 'price',
                    '個数': 'quantity',
                    '小計': 'subtotal',
                    '支払合計': 'total',
                    'ショップ用メモ欄': 'memo_content',
                    '配送先_都道府県(名称)': 'shipping_prefecture',
                    '支払方法(名称)': 'payment_method',
                    'キャンセル者': 'canceller',
                    '商品コード': 'product_code',
                    '合計': 'total_price',
                    '対応状況(ID)': 'status_id',
                    'Orderline value': 'orderline_value',
                    '決済状況': 'payment_status',
                    '配送業者(ID)': 'shipping_company_id',
                    '配送業者(名称)': 'shipping_company',
                    '出荷メール送信日': 'shipping_mail_sent_date'}

    df.rename(columns=mapping_rule, inplace=True)
    df = delete_apparently_useless_columns(df)
    df = delete_apparently_wrong_rows(df)

    if total_order_data:
        df.to_csv(os.path.join(os.getcwd(), 'order_data.csv'), index=False, encoding='utf-8-sig')  # good for japanese
    else:
        df.to_csv(os.path.join(os.getcwd(), 'fraud_order_data.csv'), index=False, encoding='utf-8-sig')
    return df


def change_date_to_datetime_type(total_order_data=True):
    if total_order_data:
        df = pd.read_csv(os.path.join(os.getcwd(), 'order_data.csv'))
    else:
        df = pd.read_csv(os.path.join(os.getcwd(), 'fraud_order_data.csv'))

    df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d %H:%M:%S')
    df['payment_date'] = pd.to_datetime(df['payment_date'], format='%Y-%m-%d %H:%M:%S')
    df['shipping_date'] = pd.to_datetime(df['shipping_date'], format='%Y-%m-%d %H:%M:%S')
    df['shipping_mail_sent_date'] = pd.to_datetime(df['shipping_mail_sent_date'], format='%Y-%m-%d %H:%M:%S')

    return df


def clean_extracted_csv(total_order_data=True):
    """
    changed columns include: status, Grade, shipping_prefecture, Domain, payment_method, canceller,
                             payment_status.

    Does not depend on any function itself.
    """
    if total_order_data:
        df = pd.read_csv(os.path.join(os.getcwd(), 'order_data.csv'))
    else:
        df = pd.read_csv(os.path.join(os.getcwd(), 'fraud_order_data.csv'))

    # ------------------- status -------------------
    # change name of status
    df['status'] = df['status'].replace({'発送済み': 'good',
                                         'キャンセル受付完了 / 返金完了': 'normal',
                                         'システムキャンセル': 'less_normal',
                                         'キャンセル受付': 'less_normal_2',
                                         'キャンセル処理中': 'processing'})

    # ------------------- order_date -------------------
    # change the 5 digit number to a datetime
    def date_to_string(digit_date):
        new_form = []
        for d in digit_date:
            try:
                x = datetime.date(1899, 12, 30) + datetime.timedelta(days=d)
                new_form.append(x.strftime('%Y-%m-%d %H:%M:%S'))
            except:
                new_form.append(d)
        return new_form

    if not total_order_data:
        # convert dates in a pandas dataframe column to strings
        df['order_date'] = date_to_string(df['order_date'])
        df['payment_date'] = date_to_string(df['payment_date'])
        df['shipping_date'] = date_to_string(df['shipping_date'])

    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['payment_date'] = pd.to_datetime(df['payment_date'], errors='coerce')
    df['shipping_date'] = pd.to_datetime(df['shipping_date'], errors='coerce')

    # ------------------- Grade ---------------------
    # change name of Grade
    df['Grade'] = df['Grade'].replace({'Aグレード': 'A',
                                       'Bグレード': 'B',
                                       'Cグレード': 'C'})
    # drop rows that doesn't have Grade of A, B, C
    df = df[df['Grade'].isin(['A', 'B', 'C'])]

    # ------------------- shipping_prefecture ---------------------
    # classify shipping_prefecture into 4 groups
    df['shipping_prefecture'] = df['shipping_prefecture'].map(lambda x: 'big_city' if x in ['東京都',
                                                                                            '神奈川県',
                                                                                            '大阪府',
                                                                                            '埼玉県'] else 'small_city')

    # ------------------- Domain ---------------------
    # judge it is normal is gmail, icloud in it
    df['Domain'] = df['Domain'].map(lambda x: x if x in ['gmail.com', 'icloud.com', 'yahoo.co.jp'] else 'other')
    df = df[df['Domain'].isin(['gmail.com', 'icloud.com', 'yahoo.co.jp', 'other'])]

    # ------------------- payment_method ---------------------
    # change name of payment_method
    df['payment_method'] = df['payment_method'].replace({'クレジットカード決済': 'credit_card',
                                                         'コンビニ決済': 'convenience_store',
                                                         'あと払い（ペイディ）': 'payday',
                                                         'ATM決済': 'atm'})
    df = df[df['payment_method'].isin(['credit_card', 'convenience_store', 'payday', 'atm'])]

    # ------------------- canceller --------------------------
    # change name of canceller
    df['canceller'] = df['canceller'].replace({'システムキャンセル': 'system canceller',
                                               'BackMarketJP': 'BackMarketJP',
                                               'カスタマー': 'customer',
                                               'Likewize Japan': 'Likewize Japan'})
    # make others as small_canceller
    df['canceller'] = df['canceller'].map(lambda x: 'small_canceller' if x not in ['system canceller',
                                                                                   'BackMarketJP',
                                                                                   'customer',
                                                                                   'Likewize Japan'] else x)
    df = df[df['canceller'].isin(['system canceller', 'BackMarketJP', 'customer', 'small_canceller', 'Likewize Japan'])]

    # ------------------- payment_status --------------------------
    df['payment_status'] = df['payment_status'].replace({'売上': 'good',
                                                         '申込': 'normal',
                                                         '取消': 'cancel',
                                                         '新規決済': 'idk'})

    # ------------------- order_date & payment_date --------------------------
    if total_order_data:
        df['order_date_weekday'] = df['order_date'].dt.weekday
        df['order_date_hour'] = df['order_date'].dt.hour
        df['payment_date_weekday'] = df['payment_date'].dt.weekday
        df['payment_date_hour'] = df['payment_date'].dt.hour

        df['order_payment_date_diff'] = df['payment_date'] - df['order_date']
        df['order_payment_date_diff'] = df['order_payment_date_diff'].dt.total_seconds() / 3600

    if total_order_data:
        df.to_csv('order_data.csv', index=False)
    else:
        df.to_csv('fraud_order_data.csv', index=False)
    return df


def change_to_one_hot(columns):
    pass


def change_product_name_for_more_info(total_order_data=True):
    # at least extract iphone/ipad, which mode, disk size
    pass


def add_columne_for_dates():
    pass


def main():
    pass


if __name__ == '__main__':
    change_col_names_and_delete_some(df=df_order_data, total_order_data=True)
    change_col_names_and_delete_some(df=df_fraud_order_data, total_order_data=False)
