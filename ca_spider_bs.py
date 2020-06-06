import csv
import time
from urllib.parse import urljoin

from selenium import webdriver
import json
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CaSpider(object):

    def __init__(self):
        print('init')
        self.url = 'https://apps.cpuc.ca.gov/apex/f?p=401'
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options,
                                       executable_path='/Users/y0f00pb/Downloads/chromedriver')
        # self.driver = webdriver.Chrome(executable_path='/Users/y0f00pb/Downloads/chromedriver')
        self.file = open('ca_docket_result_bs2.csv', 'w')
        self.fieldnames = ["docket_num", "filed_by", "industry", "filling_date", "category",
                           "current_status", "description", "staff"]

        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()
        # self.writer = csv.writer(self.file)

    def test(self):
        # self.driver.implicitly_wait(2)
        print('start running...')
        self.driver.get(self.url)
        print('get search page...')

        # search by proceeding number
        # self.driver.find_element_by_id('P1_PROCEEDING_NUM').send_keys('R')
        # search by date range
        self.driver.find_element_by_id('P1_FILED_DATE_L').send_keys('06/01/2019')
        self.driver.find_element_by_id('P1_FILED_DATE_H').send_keys('06/01/2020')

        # search by description
        # self.driver.find_element_by_id('P1_DESCRIPTION').send_keys('')
        self.driver.find_element_by_id('P1_SEARCH').click()

        page = 1
        # while True:

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        links = soup.find_all(attrs={'headers': "PROCEEDING_STATUS_DESC"})
        flag = 1
        for link in links:
            link = link.find('a').get('href')
            link = urljoin('https://apps.cpuc.ca.gov/apex/', link)
            print(link)
            # get into docket info page:
            self.driver.get(link)
            print('[get docket info page]...')
            time.sleep(2)

            docket_info_page_soup = BeautifulSoup(self.driver.page_source, 'lxml')
            docket_num = docket_info_page_soup.find('div', class_='rc-content-main').find('h1').get_text()
            docket_num = str(docket_num).split('-')[0]
            industry = docket_info_page_soup.find('span', id='P56_INDUSTRY').get_text()
            filed_by = docket_info_page_soup.find('span', id='P56_FILED_BY').get_text()
            filling_date = docket_info_page_soup.find('span', id='P56_FILING_DATE').get_text()
            category = docket_info_page_soup.find('span', id='P56_CATEGORY').get_text()
            current_status = docket_info_page_soup.find('span', id='P56_STATUS').get_text()
            description = docket_info_page_soup.find('span', id='P56_DESCRIPTION').get_text()
            staff = docket_info_page_soup.find('span', id='P56_STAFF').get_text()
            data = {'docket_num': docket_num, 'industry': industry, 'filed_by': filed_by,
                    'filling_date': filling_date, 'category': category, 'current_status': current_status,
                    'description': description, 'staff': staff}

            self.writer.writerow(data)
            print(docket_num, ',', industry, ',', filed_by, ',', filling_date, ',', category,',', current_status,',',
                      description, ',', staff)
                # flag += 1
            # for next page
            try:
                print('[in try catch block]')
                print('start next page click')
                # self.driver.back()
                # self.driver.find_element_by_xpath('//*[@id="R119088863007793168210"]/div[2]/div/div[2]/table[1]/tbody/tr/td[1]/input[1]').click()
                self.driver.find_elements_by_class_name('t14Button')[2].click()
                time.sleep(1)

                if page == 1:
                    print("[page == 1]", page)
                    # print("[page 1 current page source]", self.driver.page_source)
                    self.driver.find_element_by_xpath(
                        '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a/img['
                        '@title="Next"]')

                    self.driver.find_element_by_xpath(
                        '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a').click()
                    time.sleep(20)

                elif page > 1:
                    print("[page > 1]", page)
                    self.driver.find_element_by_xpath(
                        '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a/img['
                        '@title="Next"]')
                    self.driver.find_element_by_xpath(
                        '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a').click()
                    time.sleep(20)
                    for i in range(1, page):
                        print('[in range]', i)
                        self.driver.find_element_by_xpath(
                            '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a[2]/img['
                            '@title="Next"]')
                        self.driver.find_element_by_xpath(
                            '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a[2]').click()
                        time.sleep(20)

                page += 1

            except NoSuchElementException as e:
                print('[no next page, exit..]')
                # start_flag = False
                break

        print(['end'])
        self.driver.quit()


# soup.find('span', id='')
if __name__ == '__main__':
    c = CaSpider()
    c.test()
