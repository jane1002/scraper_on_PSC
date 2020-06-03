from os.path import join, basename, dirname

import scrapy
import urllib.parse
import csv
from scrapy import Selector

from electric_scraping.items import TxDocketLevelItem, TxItemLevelItem, TxDownloadItem


class TxSpider(scrapy.Spider):
    name = "tx"
    baseUrl = 'http://interchange.puc.texas.gov'

    def start_requests(self):
        params = {
            'UtilityType': 'E',
            'ControlNumber': '',
            'ItemMatch': 1,
            'ItemNumber': '',
            'UtilityName': '',
            'FilingParty': '',
            'DocumentType': 'ALL',
            'DateFiledFrom': '2020-05-01',
            'DateFiledTo': '2020-05-25',
            'Description': '',
            'FilingDescription': ''
        }
        # baseURL = 'http://interchange.puc.texas.gov/Search/Search?'
        url = f'{self.baseUrl}/Search/Search?{urllib.parse.urlencode(params)}'
        # url = 'http://interchange.puc.texas.gov/Search/Filings?ControlNumber=18661'

        request = scrapy.Request(url, callback=self.parse)

        yield request

    def parse(self, response):
        '''
        parse dockets table
        :param response:
        :return:
        '''
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        table_rows = response.xpath('//tr').getall()

        # remove table header
        del table_rows[0]

        docket_links = {}

        docket_item = TxDocketLevelItem()

        table = []
        for r in table_rows:
            sel = Selector(text=r)
            row = []
            # col1: Control
            docket_num = sel.xpath('//tr/td[1]/strong/a/text()').get()
            docket_link = sel.xpath('//tr/td[1]/strong/a/@href').get()
            docket_link = f'{self.baseUrl}{docket_link}'
            docket_links[docket_num] = docket_link

            # col2: Filings
            filings = sel.xpath('//tr/td[2]/text()').get()
            filings = str(filings).strip()

            # col3: Utility
            utility = sel.xpath('//tr/td[3]/text()').get()
            if utility:
                utility = str(utility).strip()

            # col4: Desc
            description = sel.xpath('//tr/td[4]/text()').get()
            if description:
                description = str(description).strip()

            row.append(docket_num)
            row.append(docket_link)
            row.append(filings)
            row.append(utility)
            row.append(description)
            table.append(row)

            docket_item['docket_num'] = docket_num
            docket_item['docket_link'] = docket_link
            docket_item['filings'] = filings
            docket_item['utility'] = utility
            docket_item['description'] = description

            yield docket_item
            # with open('tx_docket_result.csv', 'w') as f:
            #     writer = csv.writer(f)
            #     writer.writerows(table)
            if docket_link:
                request = scrapy.Request(docket_link, callback=self.parse_docket)

                yield request

        # next_link = response.xpath('/a[@rel="next"]').get()
        # if next_link:
        #     request = scrapy.Request(docket_link, callback=self.parse)
        #     yield request

        # with open('tx_docket_result01.csv', 'w') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(table)

    def parse_docket(self, response):
        '''
        docket level info includes: case style(description), document table
        :param response:
        :return:
        '''
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        table_rows = response.xpath('//tr').getall()
        del table_rows[0]

        item = TxItemLevelItem()

        for r in table_rows:
            sel = Selector(text=r)
            # col1: Item
            item_num = sel.xpath('//tr/td[1]/strong/a/text()').get()
            item_link = sel.xpath('//tr/td[1]/strong/a/@href').get()
            item_link = f'{self.baseUrl}{item_link}'

            # col2: File stamp
            file_stamp = sel.xpath('//tr/td[2]/text()').get()
            file_stamp = str(file_stamp).strip()

            # col3: Party
            party = sel.xpath('//tr/td[3]/text()').get()
            if party:
                party = str(party).strip()

            # col4: Desc
            file_description = sel.xpath('//tr/td[4]/text()').get()
            if file_description:
                file_description = str(file_description).strip()

            item['item_num'] = item_num
            item['item_link'] = item_link
            item['file_stamp'] = file_stamp
            item['party'] = party
            item['file_description'] = file_description

            yield item

            if item_link:
                request = scrapy.Request(item_link, callback=self.parse_item)
                yield request

        # next_link = response.xpath('/a/[@rel = next]').get()
        # if next_link:
        #     request = scrapy.Request(item_link, callback=self.parse_docket)
        #     yield request

    def parse_item(self, response):
        """
        download pdfs
        :param response:
        :return:
        """
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        table_rows = response.xpath('//tr').getall()
        del table_rows[0]

        for row in table_rows:
            sel = Selector(text=row)
            download_item = TxDownloadItem()

            item_download_name = sel.xpath('//td/strong/a/text()').get()
            if item_download_name:
                item_download_link = sel.xpath('//td/strong/a/@href').get()
                download_item['file_urls'] = [item_download_link]
                yield download_item
