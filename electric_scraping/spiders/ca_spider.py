import time

import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class CaSpider(scrapy.Spider):

    name = 'ca'

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/Users/y0f00pb/Downloads/chromedriver')

    def start_requests(self):
        url = 'https://apps.cpuc.ca.gov/apex/f?p=401'

        headers = {
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode' : 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1'
        }
        request = scrapy.Request(url, callback=self.parse, headers=headers)

        yield request

    def parse(self, response):
        self.driver.get(response.url)
        print(response.url)
        # print(self.driver.page_source)

        self.driver.find_element_by_id('P1_PROCEEDING_NUM').send_keys('R')
        self.driver.find_element_by_id('P1_SEARCH').click()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        time.sleep(1)
        self.driver.quit()
        sel = Selector(text=self.driver.page_source)
        sel.xpath('//table[@class="apexir_WORKSHEET_DATA"]').get()

        pass

