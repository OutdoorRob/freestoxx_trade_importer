# coding: utf-8

class Transaction:
    @property
    def id(self):
        return self.__id
    @property
    def time(self):
        return self.__time
    @property
    def symbol(self):
        return self.__symbol
    @property
    def is_long(self):
        return self.__is_long
    @property
    def size(self):
        return self.__size
    @property
    def price(self):
        return self.__price
    @property
    def order_id(self):
        return self.__order_id

    def __set_is_long(self, is_long):
        self.__is_long = True if (is_long == "BUY") else False

    def __set_size(self, size):
        self.__size = float(size)
        if (self.__is_long == False):
            self.__size *= -1

    def __init__(self, symbol, is_long, size, price, time, id, order_id):
        self.__symbol = symbol
        self.__set_is_long(is_long)
        self.__set_size(size)
        self.__price = float(price)
        self.__time = time                      # datetime convert an diese Stelle verschieben
        self.__id = int(id)
        self.__order_id = int(order_id)


class Trade:
    @property
    def id(self):
        return self.__id
    @property
    def symbol(self):
        return self.__symbol
    @property
    def is_long(self):
        return self.__is_long
    @property
    def open_datetime(self):
        return self.__open_datetime
    @property
    def close_datetime(self):
        return self.__close_datetime
    @property
    def average_open_price(self):
        return self.__average_open_price
    @property
    def average_close_price(self):
        return self.__average_close_price
    @property
    def result(self):
        return self.__result

    # public TimeSpan Duration { get; private set; }

    def __init__(self, transaction):
        self.__transactions = []
        self.__size = 0
        self.__result = None
        self.__average_open_price = None
        self.__average_close_price = None
        self.__id = transaction.id
        self.__symbol = transaction.symbol
        self.__is_long = transaction.is_long
        self.__open_datetime = transaction.time
        self.__close_datetime = None
        self.transaction_add(transaction)

    # returns true: trade still open (more transactions can be added)
    # returns false: this transaction closed the trade (no more transactions can be added to this trade, you have to open a new one)
    def transaction_add(self, transaction):
        if self.__close_datetime == None:
            self.__transactions.append(transaction)
            self.__size += transaction.size
            # check if this transaction closes the trade
            if self.__size == 0:
                self.__close_datetime = transaction.time
                self.__on_close()
                return False
            else:
                return True
        else:
            raise AttributeError ('trade has already been closed')
    
    def __on_close(self):
        __buy_price = 0
        __buy_size = 0
        __sell_price = 0
        __sell_size = 0
        self.__result = 0
        for t in self.__transactions:
            self.__result -= t.size * t.price
            if t.is_long == True:
                __buy_price += t.price * t.size
                __buy_size += t.size
            else:
                __sell_price += t.price * t.size
                __sell_size += t.size
        __buy_price /= __buy_size
        __sell_price /= __sell_size
        if self.__is_long == True:
            self.__average_open_price = __buy_price
            self.__average_close_price = __sell_price
        else:
            self.__average_open_price = __sell_price
            self.__average_close_price = __buy_price
