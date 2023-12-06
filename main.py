# coding: utf-8
 
import sys

import user_config
import trading
import freestoxx_html
import export_sqlite
import export_csv


def main():
    print("Freestoxx trade importer version 0.2.0\n")

    if len(sys.argv) > 1:
        user_config_file = sys.argv[1]
    else:
        user_config_file = 'user_config.json'

    user_cfg = user_config.user_config(user_config_file)

    # import transactions from HTML and ...
    print("reading account statement...\n")
    transactions = freestoxx_html.import_transactions(user_cfg.account_statement_path)
    # write new ones to database
    # todo: Warnung wenn keine doppelte TransactionId gefunden wurde (=> mögliche Lücke in Kontoauszug)
    print("importing transactions...\n")
    export_sqlite.write_transactions(user_cfg.database_path, transactions)

    # read transactions that aren't matched to a trade (= newly imported ones)
    transactions = export_sqlite.read_unmatched_transactions(user_cfg.database_path)

    # 'build' trades
    # there can be only one open trade for each symbol
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

    # write trades to database
    print("\nimporting trades...\n")
    export_sqlite.write_trades(user_cfg.database_path, closed_trades)
    export_sqlite.write_trades(user_cfg.database_path, open_trades)
    
    # update transactions in database
    export_sqlite.update_transactions(user_cfg.database_path, transactions)

    # convert database to csv
    export_csv.write_to_csv(user_cfg.csv_path, export_sqlite.read_all_trades_with_headers(user_cfg.database_path))

    print("import done :-) \n")


if __name__ == "__main__":
    main()
