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
    def direction(self):
        return self.__direction
    @property
    def size(self):
        return self.__size
    @property
    def size_by_direction(self):
        if self.__direction == "BUY":
            return self.__size
        else:
            return self.__size * -1
    @property
    def price(self):
        return self.__price
    @property
    def fk_order_id(self):
        return self.__fk_order_id
    @property
    def commisions_and_fees(self):
        return self.__commisions_and_fees
    @property
    def fk_trade_id(self):
        return self.__fk_trade_id
    @fk_trade_id.setter
    def fk_trade_id(self, value):
        self.__fk_trade_id = value

    # def __set_is_long(self, is_long):
    #     self.__is_long = True if (is_long == "BUY") else False

    # def __set_size(self, size):
    #     self.__size = float(size)
    #     if (self.__direction == "SELL"):
    #         self.__size *= -1

    def __init__(self, id, time, symbol, direction, size, price, fk_order_id, commisions_and_fees, __fk_trade_id = None):
        self.__symbol = symbol
        # self.__set_is_long(is_long)
        self.__direction = direction
        # self.__set_size(size)
        self.__size = float(size)
        self.__price = float(price)
        self.__time = time
        self.__id = int(id)
        self.__fk_order_id = int(fk_order_id)
        self.__commisions_and_fees = float(commisions_and_fees)
        self.__fk_trade_id = None


class Trade:
    @property
    def id(self):
        return self.__id
    @property
    def symbol(self):
        return self.__symbol
    @property
    def direction(self):
        return self.__direction
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
    
    def __set_direction(self, direction):
        self.__direction = "LONG" if (direction == "BUY") else "SHORT"

    # public TimeSpan Duration { get; private set; }

    def __init__(self, transaction):
        self.__transactions = []
        self.__size = 0
        self.__result = None
        self.__average_open_price = None
        self.__average_close_price = None
        self.__id = transaction.id
        self.__symbol = transaction.symbol
        self.__set_direction(transaction.direction)
        self.__open_datetime = transaction.time
        self.__close_datetime = None
        self.transaction_add(transaction)

    # returns true: trade still open (more transactions can be added)
    # returns false: this transaction closed the trade (no more transactions can be added to this trade, you have to open a new one)
    def transaction_add(self, transaction):
        if self.__close_datetime == None:
            self.__transactions.append(transaction)
            self.__size += transaction.size_by_direction
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
            t.fk_trade_id = self.__id
            self.__result -= t.size_by_direction * t.price
            if t.direction == "BUY":
                __buy_price += t.price * t.size_by_direction
                __buy_size += t.size_by_direction
            else:
                __sell_price += t.price * t.size_by_direction
                __sell_size += t.size_by_direction
        
        __buy_price /= __buy_size
        __sell_price /= __sell_size

        if self.__direction == "LONG":
            self.__average_open_price = __buy_price
            self.__average_close_price = __sell_price
        else:
            self.__average_open_price = __sell_price
            self.__average_close_price = __buy_price
