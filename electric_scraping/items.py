# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ElectricScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FlElectricScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    docket_num = scrapy.Field()
    # docket_info_link = scrapy.Field()
    date_docketed = scrapy.Field()
    CASR_approved = scrapy.Field()
    docket_title = scrapy.Field()
    # docket_link = scrapy.Field()


# tx site


class TxDocketLevelItem(scrapy.Item):
    docket_num = scrapy.Field()
    # docket_link = scrapy.Field()
    filings = scrapy.Field()
    utility = scrapy.Field()
    description = scrapy.Field()


class TxItemLevelItem(scrapy.Item):
    item_num = scrapy.Field()
    item_link = scrapy.Field()
    file_stamp = scrapy.Field()
    party = scrapy.Field()
    file_description = scrapy.Field()


class TxDownloadItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()


class CADocketLevelItem(scrapy.Item):
    docket_num = scrapy.Field()
    filed_by = scrapy.Field()
    industry = scrapy.Field()
    filling_date = scrapy.Field()
    category = scrapy.Field()
    current_status = scrapy.Field()
    description = scrapy.Field()
    staff = scrapy.Field()
