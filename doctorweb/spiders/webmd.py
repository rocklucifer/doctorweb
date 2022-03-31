import scrapy
from doctorweb.items import DoctorwebItem

class WebmdSpider(scrapy.Spider):
    name = 'webmd'
    page_number = 2
    # allowed_domains = ['www.doctor.webmd.com']
    start_urls = ['https://doctor.webmd.com/find-a-doctor/specialty/general-dentistry/alabama/athens']
    def parse(self, response):
        data = response.xpath('//*[@class = "card-content"]')
        for item in data:
            Name = item.xpath('.//h2/text()').extract_first()
            Specialist = item.xpath('.//p[@class="prov-specialty"]/text()').extract_first()
            name_url = item.xpath('.//a/@href').extract_first()
            yield scrapy.Request(name_url, callback=self.parse_next,
                                meta = {'Name': Name,
                                'Specialist': Specialist,
                                'name_url': name_url})
        next_page_url = 'https://doctor.webmd.com/find-a-doctor/specialty/general-dentistry/alabama/athens?pagenumber=' + str(WebmdSpider.page_number)
        if WebmdSpider.page_number<=2:
            WebmdSpider.page_number += 1
            absolute = response.urljoin(next_page_url)
            yield scrapy.Request(absolute, callback=self.parse)
    def parse_next(self, response):
        print('parse_nextparse_next')
        Name= response.meta['Name']
        Specialist= response.meta['Specialist']
        name_url= response.meta['name_url']
        phone_number = response.xpath('//button/span/text()')[2].extract()
        # yield{
        #    'Name':Name,
        #    'Specialist':Specialist,
        #    'name_url': name_url,
        #    'phone_number': phone_number
        # }
        item = DoctorwebItem()
        item['name'] = Name
        item['specialty'] = Specialist
        return item
