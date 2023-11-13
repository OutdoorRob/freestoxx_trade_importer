# coding: utf-8

import json


class user_config:
    @property
    def account_statement_path(self):
        return self.__account_statement_path
    @property
    def database_path(self):
        return self.__database_path
    @property
    def csv_path(self):
        return self.__csv_path

    def __init__(self, user_config_path):
        self.__config = json.load(open(user_config_path))
        self.__account_statement_path = self.__config["account_statement"]["path"] + self.__config["account_statement"]["file"]
        self.__database_path = self.__config["database"]["path"] + self.__config["database"]["file"]
        self.__csv_path = self.__config["csv"]["path"] + self.__config["csv"]["file"]

