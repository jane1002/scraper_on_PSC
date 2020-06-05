import csv
import time
from urllib.parse import urljoin

import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from electric_scraping.items import CADocketLevelItem


class CaSpider(scrapy.Spider):
    name = 'ca'

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path='/Users/y0f00pb/Downloads/chromedriver')

    def start_requests(self):
        url = 'https://apps.cpuc.ca.gov/apex/f?p=401'

        headers = {
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1'
        }
        request = scrapy.Request(url, callback=self.parse, headers=headers)

        yield request

    def parse(self, response):
        self.driver.get(response.url)
        # print(response.url)
        # print(self.driver.page_source)

        self.driver.find_element_by_id('P1_PROCEEDING_NUM').send_keys('R')
        self.driver.find_element_by_id('P1_SEARCH').click()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        time.sleep(1)
        page = self.driver.page_source
        self.driver.quit()
        sel = Selector(text=page)
        table_rows = sel.xpath('//table[@class="apexir_WORKSHEET_DATA"]/tbody/tr').getall()
        del table_rows[0]

        for row in table_rows:
            sel_row = Selector(text=row)
            link = sel_row.xpath('//tr/td[1]/a/@href').get()
            link = urljoin('https://apps.cpuc.ca.gov/apex/', link)
            # print("sss", link)

            request = scrapy.Request(link, callback=self.parse_ca_docket)
            yield request

        # for next page
        # while True:
        #     if self.driver.page_source.find('shark-pager-disable-next') != -1:
        #         break
        #
        #     time.sleep(1)
        #     page = self.driver.page_source
        #     select = Selector(text=page)
        #     table = sel.xpath('//table[@class="apexir_WORKSHEET_DATA"]/tr/td').get()

        # pass

    def parse_ca_docket(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        industry = response.xpath('//span[@id="P56_INDUSTRY"]/text()').get()
        docket_num = response.xpath('//table/tbody/tr/td[1]/div[4]/div[2]/div/div[2]/h1/text()').get()
        filed_by = response.xpath('//span[@id="P56_FILED_BY"]/text()').get()
        filling_date = response.xpath('//span[@id="P56_FILING_DATE"]/text()').get()
        category = response.xpath('//span[@id="P56_CATEGORY"]/text()').get()
        current_status = response.xpath('//span[@id="P56_STATUS"]/text()').get()
        description = response.xpath('//span[@id="P56_DESCRIPTION"]/text()').get()
        staff = response.xpath('//span[@id="P56_STAFF"]/text()').get()

        docket_item = CADocketLevelItem()

        docket_item['docket_num'] = docket_num
        docket_item['industry'] = industry
        docket_item['filed_by'] = filed_by
        docket_item['filling_date'] = filling_date
        docket_item['category'] = category
        docket_item['current_status'] = current_status
        docket_item['description'] = description
        docket_item['staff'] = staff

        yield docket_item
