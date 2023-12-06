# coding: utf-8

import datetime
import sqlite3
import trading


def adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()

def adapt_time_iso(val):
    """Adapt datetime.time to timezone-naive ISO 8601 time."""
    return val.isoformat()

sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_adapter(datetime.time, adapt_time_iso)


def write_transactions(database_path, transactions):
    db_cursor = __connect_to_database(database_path)

    for transaction in transactions:
        try:
            db_cursor.execute("""
                INSERT INTO Transactions (Id, Time,
                                          Symbol, Direction,
                                          Size, Price,
                                          FkOrderId, CommissionsAndFees)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                    (transaction.id, transaction.time,
                     transaction.symbol, transaction.direction,
                     transaction.size, transaction.price,
                     transaction.fk_order_id, transaction.commisions_and_fees))
            print(str(transaction.id) + "\t" + str(transaction.symbol) + "\t" + str(transaction.direction) + "\t" + str(transaction.time))
        except sqlite3.IntegrityError as ex:
            # print(ex)
            None

    db_cursor.connection.commit()
    __disconnect_from_database(db_cursor)


def update_transactions(database_path, transactions):
    db_cursor = __connect_to_database(database_path)

    for transaction in transactions:
        try:
            db_cursor.execute("""
                UPDATE Transactions
                SET FkTradeId = ?
                WHERE Id = ?;""",
                (transaction.fk_trade_id, transaction.id))
        except sqlite3.IntegrityError as ex:
            print(ex)
            None

    db_cursor.connection.commit()
    __disconnect_from_database(db_cursor)


def read_unmatched_transactions(database_path):
    db_cursor = __connect_to_database(database_path)

    # try:
    #     db_cursor.execute("SELECT * FROM Transactions WHERE FkTradeId is NULL")
    #     headers = list(map(lambda attr : attr[0], db_cursor.description))
    #     results = [{header:row[i] for i, header in enumerate(headers)} for row in db_cursor]
    # except sqlite3.IntegrityError as ex:
    #     print(ex)

    # __disconnect_from_database(db_cursor)

    # transactions = list()

    # for r in results:
    #     t = trading.Transaction(r['TransactionId'], r['TransactionTime'],
    #                             r['Symbol'], r['Symbol'],
    #                             r['Size'], r['Price'],
    #                             r['OrderID'], r['CommissionsAndFees'])
    #     transactions.append(t)

    try:
        rows = db_cursor.execute("""
            SELECT Id, Time, Symbol, Direction, Size, Price, FkOrderId, CommissionsAndFees
            FROM Transactions
            WHERE FkTradeId is NULL""").fetchall()
    except sqlite3.IntegrityError as ex:
        print(ex)

    __disconnect_from_database(db_cursor)

    unmatched_transactions = list()

    for row in rows:
        t = trading.Transaction(row[0], datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"), row[2], row[3], row[4], row[5], row[6], row[7])
        unmatched_transactions.append(t)

    return unmatched_transactions


def write_trades(database_path, trades):
    db_cursor = __connect_to_database(database_path)

    db_cursor.execute("DELETE FROM Trades WHERE CloseDate is NULL")
    db_cursor.connection.commit()
    
    for trade in trades:
        __close_date = None
        __close_time = None
        if trade.close_datetime is not None:
            __close_date = trade.close_datetime.date()
            __close_time = trade.close_datetime.time()
        
        try:
            db_cursor.execute("""
                INSERT INTO Trades (Id, Symbol, Direction,
                                    OpenDate, OpenTime, AverageOpenPrice,
                                    CloseDate, CloseTime, AverageClosePrice,
                                    Result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                    (trade.id, trade.symbol, trade.direction,
                     trade.open_datetime.date(), trade.open_datetime.time(), trade.average_open_price,
                     __close_date, __close_time, trade.average_close_price,
                     trade.result))
            # print("new trade imported: " + str(trade.id) + " " + str(trade.symbol) + " " + str(trade.direction) + " " + str(trade.open_datetime) + "\n")
        except sqlite3.IntegrityError as ex:
            # print(ex)
            None

    db_cursor.connection.commit()
    __disconnect_from_database(db_cursor)


def read_all_trades_with_headers(database_path):
    db_cursor = __connect_to_database(database_path)

    try:
        db_cursor.execute("SELECT * FROM Trades")
        # https://stackoverflow.com/questions/65934371/return-data-from-sqlite-with-headers-python3
        headers = list(map(lambda attr : attr[0], db_cursor.description))
        results = [{header:row[i] for i, header in enumerate(headers)} for row in db_cursor]
    except sqlite3.IntegrityError as ex:
        print(ex)

    __disconnect_from_database(db_cursor)

    return results


def __connect_to_database(database_path):
    return sqlite3.connect(database_path).cursor()


def __disconnect_from_database(db_cursor):
    db_cursor.connection.close()