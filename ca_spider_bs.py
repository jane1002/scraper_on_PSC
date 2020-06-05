import csv
import time
from urllib.parse import urljoin

from selenium import webdriver
import json
from bs4 import BeautifulSoup
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
        self.file = open('ca_docket_result_bs.csv', 'w')
        self.fieldnames = ["docket_num", "filed_by", "industry", "filling_date", "category",
                           "current_status", "description", "staff"]

        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()
        # self.writer = csv.writer(self.file)

    def test(self):
        print('start running...')
        self.driver.get(self.url)
        print('get search page...')
        self.driver.find_element_by_id('P1_PROCEEDING_NUM').send_keys('R')
        self.driver.find_element_by_id('P1_SEARCH').click()
        page = 1
        start_flag = True

        while page == 1:
            self.driver.implicitly_wait(2)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            links = soup.find_all(attrs={'headers': "PROCEEDING_STATUS_DESC"})
            flag = 1

            # for link in links:
            #     link = link.find('a').get('href')
            #     link = urljoin('https://apps.cpuc.ca.gov/apex/', link)
            #     print(link)
            #     # get into docket info page:
            #     if flag == 1:
            #         self.driver.get(link)
            #         self.driver.implicitly_wait(3)
            #         print('[get docket info page]...')
            #
            #         docket_info_page_soup = BeautifulSoup(self.driver.page_source, 'lxml')
            #         docket_num = docket_info_page_soup.find('div', class_='rc-content-main').find('h1').get_text()
            #         docket_num = str(docket_num).split('-')[0]
            #         industry = docket_info_page_soup.find('span', id='P56_INDUSTRY').get_text()
            #         filed_by = docket_info_page_soup.find('span', id='P56_FILED_BY').get_text()
            #         filling_date = docket_info_page_soup.find('span', id='P56_FILING_DATE').get_text()
            #         category = docket_info_page_soup.find('span', id='P56_CATEGORY').get_text()
            #         current_status = docket_info_page_soup.find('span', id='P56_STATUS').get_text()
            #         description = docket_info_page_soup.find('span', id='P56_DESCRIPTION').get_text()
            #         staff = docket_info_page_soup.find('span', id='P56_STAFF').get_text()
            #         data = {'docket_num': docket_num, 'industry': industry, 'filed_by': filed_by,
            #                 'filling_date': filling_date, 'category': category, 'current_status': current_status,
            #                 'description': description, 'staff': staff}
            #
            #         # data = []
            #         # data.append(docket_num)
            #         # data.append(industry)
            #         # data.append(filed_by)
            #         # data.append(filling_date)
            #         # data.append(category)
            #         # data.append(current_status)
            #         # data.append(description)
            #         # data.append(staff)
            #         self.writer.writerow(data)
            #         print('...data...', docket_num, ',', industry, ',', filed_by, ',', filling_date, ',', category,',', current_status,',',
            #               description, ',', staff)
            #         flag += 1

            # for next page
            next_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a/img['
                           '@title="Next"]')))
            if next_button:
                print('start next page click')
                next2 = self.driver.find_element_by_xpath('//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a') \
                    .get_attribute('href')
                print(next2)
                # self.driver.implicitly_wait(2)
                if page == 1:
                    print("$$$$ page == 1")
                    # self.driver.find_element_by_xpath('//*[@id="R119089022893978248410"]/div/table[1]/tbody/tr/td/input').click()
                    # self.driver.find_element_by_xpath('//*[@id="119089023003070248410"]/tbody/tr[2]/td[1]/a').click()

                    # js = "gReport.navigate.paginate('documennt...')"
                    # self.driver.execute_script(js)

                    # self.driver.execute_script("arguments[0].click;", next2)

                    # action = webdriver.common.action_chains.ActionChains(self.driver)
                    # action.move_to_element_with_offset(next2, 0, 0)
                    # action.click()
                    # self.driver.find_element_by_xpath('//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a/img['
                    #                                   '@title="Next"]').click()
                    # WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    #     (By.XPATH, '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a'))).click()

                    # pages = self.driver.find_elements_by_css_selector('a[href^="javascript:gReport.navigate.paginate"]')
                    # for l in pages:
                    #     l.click()
                    #     print(l.tag_name)
                    #     print(self.driver.page_source)
                    #     break
                    self.driver.find_element_by_xpath('//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a').click()
                    time.sleep(40)
                    print(self.driver.page_source)

                elif page > 1:
                    self.driver.find_element_by_xpath(
                        '//*[@id="apexir_DATA_PANEL"]/table/tbody/tr[1]/td/span/a[2]').click()
                page += 1


# soup.find('span', id='')
if __name__ == '__main__':
    c = CaSpider()
    c.test()
