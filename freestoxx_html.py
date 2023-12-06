# coding: utf-8

import re
import datetime

from lxml import html

import trading

# imports all transactions from a Freestoxx HTML account statement
def import_transactions(html_file):
    transactions = []

    # transaction_table = html.fromstring(html_data).xpath('//div[@class="transactionsTable"]/table')
    transaction_table = html.parse(html_file).xpath('//div[@class="transactionsTable"]/table')
    
    # gets table headers as list of strings
    headers = transaction_table[0].xpath('.//thead/tr/th/text()')
    
    # gets transaction data as list of strings
    # writes each data record to the database
    for data_record in transaction_table[0].xpath('.//tbody/tr'):
        transaction = data_record.xpath('.//td/text()')
        transactions.append(trading.Transaction(transaction[headers.index('Transaction ID')], datetime_convert(transaction[headers.index('Transaction Time')]),
                                                transaction[headers.index('Symbol')], transaction[headers.index('Direction')],
                                                transaction[headers.index('Size')], transaction[headers.index('Price')],
                                                transaction[headers.index('Order ID')], transaction[headers.index('Commissions and Fees')]))
    transactions.reverse()
    return transactions


def datetime_convert(date_time):
    pattern = "(?P<day>\d+).(?P<month>\d+).(?P<year>\d+), (?P<hour>\d+):(?P<minute>\d+)"
    m = re.match(pattern, date_time)
    return datetime.datetime(int(m.group('year')) + 2000, int(m.group('month')), int(m.group('day')), int(m.group('hour')), int(m.group('minute')))
