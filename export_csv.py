# coding: utf-8


import csv
import sqlite3


def write_to_csv(csv_file, data):
    with open(csv_file, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, data[0].keys(), dialect='excel', delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(data)