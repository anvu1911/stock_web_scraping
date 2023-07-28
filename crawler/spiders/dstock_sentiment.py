"""
dstock.vndirect crawler.
"""
import scrapy

TICKER_LIST = ['ACB', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR', 'HDB', 'HPG', 'KDH', 'MBB', 'MSN', 'MWG', 'NVL',
               'PDR', 'PLX', 'PNJ', 'POW', 'SAB', 'SSI', 'STB', 'TCB', 'TPB', 'VCB', 'VHM', 'VIC', 'VJC', 'VNM',
               'VPB', 'VRE']


def get_urls():
    """Get urls for 30 tickers of VN30.
    """
    urls = list()
    for ticker in TICKER_LIST:
        urls.append("https://dstock.vndirect.com.vn/tong-quan/" +
                    ticker + "/quan-diem-cac-cong-ty-ck-popup")

    print(len(urls))
    return urls


class VnexpressSpider(scrapy.Spider):
    name = 'dstock'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data/dstock.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDENT': 4,
    }

    start_urls = get_urls()

    def start_requests(self):
        # url = "https://dstock.vndirect.com.vn/tong-quan/ACB/quan-diem-cac-cong-ty-ck-popup"
        for url in self.start_urls:
            yield scrapy.Request(url, meta={'playwright': True})

    def parse(self, response):
        sentiment = list()
        ticker = response.css(
            '.modal-heading__text').xpath('text()')[1].get()[-3:]
        for table in response.css('.modal-table'):
            for row in table.xpath('table/tbody/tr'):
                item = {}
                item['date'] = row.xpath('td')[0].xpath('text()').get()
                item['ticker'] = row.xpath('td')[1].xpath('text()').get()
                item['action'] = row.xpath('td')[2].xpath('text()').get()
                item['est_price'] = row.xpath('td')[3].xpath('text()').get()
                # print(f'{date}\t{ticker}\t{action}\t{est_price}')
                sentiment.append(
                    (item['date'], item['ticker'], item['action'], item['est_price']))
        yield {
            ticker: sentiment,
        }

        # print(table.xpath(
        #     'table/tbody/tr')[0].xpath('td')[0].xpath('text()').get())
        # yield {
        #     'date': table.xpath('table/tbody/td[has-class("td-label--small")]/text()').get()
        # }

        # table = response.css('.business-plan-inner').css('.modal-table').xpath('./tbody').getall()
        # table = response.css('.business-plan-inner').css('.modal-table')
        # print(len(table))
        # table = response.css('div.modal-table')
        # print(type(table.xpath('//table/thead/tr/th')[3]))
        # print(table.xpath('//table/tbody/tr').get())
        # print(table.xpath('//table/thead/tr/th[1]/text()').get())
        # print(table.xpath('//table/thead/tr/th[2]/text()').get())
        # print(table.xpath('//table/thead/tr/th[3]/text()').get())
        # print(table.xpath('//table/thead/tr/th[4]/text()').get())
        # print(response.css('div.modal-table').getall())
        # print(response.xpath('//div[has-class("modal-table")]').getall())
        # for article in response.xpath('//article'):
        #     yield {
        #         'category': category,
        #         'url': article.xpath('div/a/@href').get(),
        #         'title': article.xpath('div/a/@title').get(),
        #         'text': article.xpath('p/a/text()').get()
        #     }
