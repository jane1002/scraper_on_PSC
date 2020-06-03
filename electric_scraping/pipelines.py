# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json

# from scrapy.extensions.feedexport import BlockingFeedStorage
# from azure.storage.blob import BlockBlobService
import os

from scrapy.pipelines.files import FilesPipeline

from electric_scraping.items import TxItemLevelItem


class ElectricScrapingPipeline:
    def __init__(self):
        # self.file = open('fl_docket_result.json', 'w')
        self.file = open('fl_docket_result.csv', 'w')
        self.fieldnames = ["docket_num", "docket_info_link", "date_docketed", "CASR_approved",
                           "docket_title", "docket_link"]
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        # content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()


class TXDocketLevelPipeline:
    def __init__(self):
        # self.file = open('fl_docket_result.json', 'w')
        self.file = open('tx_docket_result.csv', 'w')
        self.fieldnames = ["docket_num", "docket_link", "filings", "utility",
                           "description"]
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        # content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()


class TXItemLevelPipeline:
    def __init__(self):
        # self.file = open('fl_docket_result.json', 'w')
        self.file = open('tx_item_result.csv', 'w')
        self.fieldnames = ["item_num", "item_link", "file_stamp", "party",
                           "file_description"]
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        if isinstance(item, TxItemLevelItem):
            self.writer.writerow(item)
            # content = json.dumps(dict(item), ensure_ascii=False) + "\n"
            # self.file.write(content)
            return item

    def close_spider(self, spider):
        self.file.close()


from os.path import basename, dirname, join
from urllib.parse import urlparse


class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        docket_num = basename(path).split('_')[0]
        # return join(basename(dirname(path)), basename(path))
        return join(docket_num, basename(path))

# class AzureBlobFeedStorage(BlockingFeedStorage):
#
#     def __init__(self, uri):
#
#         '''
#         Azure uses slashes '/' in their keys, which confuses the shit out of urlparse.
#         So, we just handle it ourselves here.
#         assuming format looks like this:
#
#         azure://account_name:password@container/filename.jsonl
#
#         azure://bobsaccount:1234567890abc1KUj0lK1gXHv4NHrCfKxfxHy3bwQJ+LqFHCay6r1S/Yhw2Ot4Tk6p1zF9IiMcPBo7o9poXZgA==@sites/filename.jsonl
#         '''
#
#         container = uri.split('@')[1].split('/')[0]
#         filename = '/'.join(uri.split('@')[1].split('/')[1::])
#         account_name, account_key = uri[8::].split('@')[0].split(':')
#
#         self.account_name = account_name
#         self.account_key = account_key
#         self.container = container
#         self.filename = filename
#         self.blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
#
#     def _store_in_thread(self, file):
#         file.seek(0)
#         self.blob_service.create_blob_from_stream( self.container, self.filename, file)
