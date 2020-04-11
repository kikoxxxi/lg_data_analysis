# -*- coding: utf-8 -*-

import csv
import urllib.parse


class Util(object):
    def url_encode(self, string):
        return urllib.parse.quote(string)

    def create_csv(self, path, head):
        with open('{}.csv'.format(path), "w+", encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(head)
            f.close()

    def append_csv(self, path, data):
        with open('{}.csv'.format(path), 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for d in data:
                writer.writerow(d)
            f.close()
