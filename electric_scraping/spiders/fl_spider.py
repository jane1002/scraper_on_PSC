import scrapy
import csv
from scrapy import Selector, FormRequest

from electric_scraping.items import FlElectricScrapingItem


class FlSpider(scrapy.Spider):
    name = "fl"
    baseUrl = 'http://www.psc.state.fl.us/ClerkOffice'

    # 1. search  OPEN Electric Dockets
    # url = 'http://www.psc.state.fl.us/ClerkOffice/DocketList?docketType=E'

    # 2. view OPEN dockets in one month,
    # need to add an additional filter in parse, suffix -EC,EG,EI,EU to get electric dockets
    # url = 'http://www.psc.state.fl.us/ClerkOffice/DocketList?docketType=O'

    # 3. search dockets by date,
    # need to add an additional filter in parse, suffix -EC,EG,EI,EU to get electric dockets
    # can't tell the docket is open or not ???
    # FormRequest

    def start_requests(self):
        url = f'{self.baseUrl}/Docket'

        frmdata = {
            'radioValue': 'Date',
            'fromDate': '05/01/2020',
            'toDate': '05/25/2020',
            'command': 'Search'
        }
        yield FormRequest(url, callback=self.parse, formdata=frmdata)

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        table_rows = response.xpath('//tbody/tr').getall()
        table = []

        for r in table_rows:
            sel = Selector(text=r)
            row = []

            item = FlElectricScrapingItem()

            # col1: docket number + suffix
            docket_num = sel.xpath('//tr/td[1]/a/text()').get()
            electric_suffix = ('EC', 'EG', 'EI', 'EU')

            if str(docket_num).endswith(electric_suffix):
                docket_info_link = sel.xpath('//tr/td[1]/a/@href').get()
                docket_info_link = f'{self.baseUrl}/{docket_info_link}'

                # col2: Data Docketed
                date_docketed = sel.xpath('//tr/td[2]/text()').get()
                if date_docketed:
                    date_docketed = str(date_docketed).strip()

                # col3: CASR Approved
                CASR_approved = sel.xpath('//tr/td[3]/text()').get()
                if CASR_approved:
                    CASR_approved = str(CASR_approved).strip()

                # col4: Docket Title
                docket_title = sel.xpath('//tr/td[4]/text()').get()
                if docket_title:
                    docket_title = str(docket_title).strip()

                # col5: docket link
                docket_link = sel.xpath('//tr/td[5]/a/@href').get()
                if docket_link:
                    docket_link = f'{self.baseUrl}/{docket_link}'

                item['docket_num'] = docket_num
                item['docket_info_link'] = docket_info_link
                item['date_docketed'] = date_docketed
                item['CASR_approved'] = CASR_approved
                item['docket_title'] = docket_title
                item['docket_link'] = docket_link
                # print("*******", item['docket_num'], item['docket_info_link'])

                yield item

#         row.append(docket_num)
#         row.append(docket_info_link)
#         row.append(date_docketed)
#         row.append(CASR_approved)
#         row.append(docket_title)
#         row.append(docket_link)
#         table.append(row)
#
# with open('fl_docket_result.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerows(table)
#     f.close()
