import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def linkTextExtractor(aText):
    # example of how a raw link looks like
    # '\r\n\t\t\t\t\t  Fitness Equipment on EMI  \r\n\t\t\t\t\t'
    remove = ['\n', '\t', '\r']
    
    for r in remove:
        if r == '\n':
            aText = aText.replace(r, '. ')
            continue
        aText = aText.replace(r, ' ')

    aText = ''.join([i if ord(i) < 128 else ' ' for i in aText])

    aText = aText.strip(' ')
    aText = aText.strip('.')
    aText = aText.strip(' ')
    aText = aText.strip('.')

    return aText

def stringCheck(string):
    return len(string.replace(' ', '').replace('.', '')) > 0


class PASpiderSpider(CrawlSpider):
    name = 'p_a_spider'
    # allowed_domains = ['bajajfinserv.in']
    # start_urls = ['http://bajajfinserv.in/']

    allowed_domains = ['bajajfinserv.in']
    start_urls = ['https://www.bajajfinserv.in/']

    rules = (
        Rule(LinkExtractor(deny=([r'(.*)(\/hindi\/)(.*)', r'(.*)(\/tamil\/)(.*)'])), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        
        print(response)

        p_items = response.xpath('//p/text()').getall()

        a_items = response.xpath('//a/text()').getall()

        p_obs = [
                {idx: linkTextExtractor(p_items[idx])}
                    for idx in range(len(p_items)) 
                        if stringCheck(linkTextExtractor(p_items[idx]))
        ]

        a_obs = [
                {idx: linkTextExtractor(a_items[idx])} 
                    for idx in range(len(a_items)) 
                        if stringCheck(linkTextExtractor(a_items[idx]))
        ]

        yield {
            'url' : {
                'url'  : response.url,
                'paras': p_obs,
                'links': a_obs
            }
        }
        