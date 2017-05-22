import scrapy
import re

class Textileitem(scrapy.Item):
    Comp_Name = scrapy.Field()
    Comp_Type = scrapy.Field()
    About_Comp = scrapy.Field()
    Products = scrapy.Field()
    Address = scrapy.Field()
    Mobile = scrapy.Field()
    Phone = scrapy.Field()
    Fax = scrapy.Field()
    Contact_Name = scrapy.Field()
    Email = scrapy.Field()
    Contact_Url = scrapy.Field()
    Landing_Url = scrapy.Field()

class Textileinfomedia (scrapy.Spider):
    name = "textileinfomedia_spider"
    allowed_domains = ['https://www.textileinfomedia.com']
    start_urls = ['https://www.textileinfomedia.com/textile-industry']

    def parse(self, response):
        href_links = response.xpath('//div[@class="main-cat"]//ul//li//a/@href').extract()

        for href in href_links:
            url = 'https://www.textileinfomedia.com/' + href
            yield scrapy.Request(url=url, dont_filter=True, callback=self._parse_links)

    def _parse_links(self, response):
        self.href_urls = response.xpath('//div[@class="panel-body"]//h3[@class="sec_titl"]//a/@href').extract()

        for href in self.href_urls:
            self.comp_type = response.url.replace('.htm', '').replace('https://www.textileinfomedia.com/', '')
            url = 'https://www.textileinfomedia.com/' + href
            yield scrapy.Request(url=url, dont_filter=True,  callback=self._parse_data)

    def _parse_data(self, response):
        item = Textileitem()
        full_url = response.url
        if "/company-info/" in full_url:
            infos = response.xpath('//div[@class="agen_info2"]//div[@class="panel-body"]/p[@class="sec_desc"]/text()').extract()

            item['Comp_Name'] = response.xpath('//div[@class="agen_info2"]//div[@class="panel-body"]//div[@class="col-md-9"]//h3[@class="sec_titl"]/text()').extract()[0].replace('\r\n', '').replace('  ', '')
            item['Comp_Type'] = response.xpath('//div[@class="agen_info2"]//div[@class="panel-body"]//p[@class="sec_desc"]/text()').extract()[0].replace('\r\n', '').replace('  ', '')
            item['About_Comp'] = response.xpath('//div[@class="agen_info2"]//div[@class="panel-body"]//p[@class="sec_desc"]/text()').extract()[1].replace('\r\n', '').replace('  ', '')
            products = response.xpath('//div[@class="agen_info2"]//div[@class="panel-body"]//div[@class="col-md-4"]//p[@class="sec_desc"]/text()').extract()
            item['Products'] = []
            for product in products:
                item['Products'].append(product.replace('\r\n', '').replace('  ', ''))
            item['Address'] = response.xpath('//div[@class="agen_info2"]//div[@class="panel-body"]/p[@class="sec_desc"]/text()').extract()[2].replace('\r\n', '').replace('  ', '')
            item['Mobile'] = response.xpath('//div[@class="agen_info2"]//div[@class="panel-body"]/p[@class="sec_desc"]/text()').extract()[3].replace('\r\n', '').replace('  ', '')

            for info in infos:
                if "Phone :" in info:
                    item['Phone'] = info.replace('\r\n', '').replace('  ', '').replace('Phone :', '')
                    break
                else:
                    item['Phone'] = ''

            for info in infos:
                if "Fax Number :" in info:
                    item['Fax'] = info.replace('\r\n', '').replace('  ', '').replace('Fax Number :', '')
                    break
                else:
                    item['Fax'] = ''

            for info in infos:
                if "Contact Person:" in info:
                    item['Contact_Name'] = info.replace('\r\n', '').replace('  ', '').replace('Contact Person:', '')
                    break
                else:
                    item['Contact_Name'] = ''

            item['Email'] = response.xpath('//div[@class="agen_info2"]//div[@class="panel-body"]//p[@class="sec_desc"]//a/@href').extract()
            item['Landing_Url'] = response.url
            yield item
        else:
            item['Comp_Name'] = response.xpath('//h2[@class="my_title"]/text()').extract()[0]
            item['Comp_Type'] = self.comp_type

            if response.xpath('//div[@class="container"]//div[@class="col-md-8"]//p/text()').extract()[0] != "":
                item['About_Comp'] = response.xpath('//div[@class="container"]//div[@class="col-md-8"]//p/text()').extract()[0]
            else:
                item['About_Comp'] = response.xpath('//div[@class="container"]//div[@class="col-md-8"]//p/text()').extract()[1]

            products = response.xpath('//div[@class="container"]//div[@class="col-md-8"]/p/text()').extract()
            item['Products'] = []

            for idx, product in enumerate(products):
                if idx != 0:
                    item['Products'].append(product)
            item['Address'] = response.xpath('//div[@class="srch_frm"]/p/text()').extract()[0]
            item['Mobile'] = response.xpath('//div[@class="srch_frm"]/p/text()').extract()[2]
            item['Phone'] = response.xpath('//div[@class="srch_frm"]/p/text()').extract()[2]
            item['Email'] = response.xpath('//div[@class="srch_frm"]/p/text()').extract()[3]
            item['Landing_Url'] = response.url
            yield item