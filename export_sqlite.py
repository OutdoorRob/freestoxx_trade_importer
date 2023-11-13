# coding: utf-8

import datetime
import sqlite3


def adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()

def adapt_time_iso(val):
    """Adapt datetime.time to timezone-naive ISO 8601 time."""
    return val.isoformat()

sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_adapter(datetime.time, adapt_time_iso)


def trades_to_database(cursor, trades):
    # db_trades = cursor.execute("SELECT TradeID, CloseDate FROM Trades WHERE CloseDate is NULL").fetchall()

    cursor.execute("DELETE FROM Trades WHERE CloseDate is NULL")
    cursor.connection.commit()
    
    for trade in trades:
        __close_date = None
        __close_time = None
        if trade.close_datetime is not None:
            __close_date = trade.close_datetime.date()
            __close_time = trade.close_datetime.time()
        
        try:
            cursor.execute("""
                INSERT INTO Trades (TradeID, Symbol, Direction,
                                    OpenDate, OpenTime, AverageOpenPrice,
                                    CloseDate, CloseTime, AverageClosePrice,
                                    Result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                    (trade.id, trade.symbol, "LONG" if trade.is_long else "SHORT",
                     trade.open_datetime.date(), trade.open_datetime.time(), trade.average_open_price,
                     __close_date, __close_time, trade.average_close_price,
                     trade.result))
            # print("new trade imported: " + str(trade.id) + " " + str(trade.symbol) + " " + "LONG" if trade.is_long else "SHORT" + " " + str(trade.open_datetime.date()) + "\n")
        except sqlite3.IntegrityError as ex:
            # print(ex)
            None


def read_trades_with_headers(cursor):
    try:
        cursor.execute("SELECT * FROM Trades")
        # https://stackoverflow.com/questions/65934371/return-data-from-sqlite-with-headers-python3
        headers = list(map(lambda attr : attr[0], cursor.description))
        results = [{header:row[i] for i, header in enumerate(headers)} for row in cursor]
    except sqlite3.IntegrityError as ex:
        print(ex)
    return results