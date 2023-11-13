# coding: utf-8

import sqlite3
import sys

import user_config
import trading
import freestoxx_html
import export_sqlite
import export_csv


def main():
    print("Freestoxx trade importer version 0.0.1\n")
    print("starting import...\n")

    if len(sys.argv) > 1:
        user_config_file = sys.argv[1]
    else:
        user_config_file = 'user_config.json'

    user_cfg = user_config.user_config(user_config_file)

    transactions = freestoxx_html.import_transactions(user_cfg.account_statement_path)
    transactions.reverse()

    open_trades = []
    closed_trades = []

    for transaction in transactions:
        open_trade = list(filter(lambda trade: trade.symbol == transaction.symbol, open_trades))
        if len(open_trade) == 0:
            open_trades.append(trading.Trade(transaction))
        else:
            if open_trade[0].transaction_add(transaction) == False:     # trade closed
                closed_trades.append(open_trade[0])
                open_trades.remove(open_trade[0])


    # write closed trades to database
    db_conn = sqlite3.connect(user_cfg.database_path)
    db_cursor = db_conn.cursor()

    export_sqlite.trades_to_database(db_cursor, closed_trades)
    export_sqlite.trades_to_database(db_cursor, open_trades)

    # convert database to csv
    export_csv.write_to_csv(user_cfg.csv_path, export_sqlite.read_trades_with_headers(db_cursor))

    db_conn.commit()
    db_conn.close()

    print("\nimport done\n")


if __name__ == "__main__":
    main()
