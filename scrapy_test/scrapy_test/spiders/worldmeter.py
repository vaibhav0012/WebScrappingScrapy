import scrapy


class WorldmeterSpider(scrapy.Spider):
    name = "worldmeter"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()
        # countries = response.xpath('//td/a/text()').getall()
        country_links = response.xpath('//td/a')
        
        for country in country_links:
            country_name = country.xpath('.//text()').get()
            country_link = country.xpath('.//@href').get()
            # absolute links
            # absolute_url = f'https://www.worldometers.info/{country_link}'
            # absolute_url = response.urljoin(country_link)
            # yield scrapy.Request(url=absolute_url)
            
            # relative links
            # yield response.follow(country_link)
            #yield{
            #    'country_name':country_name,
            #    'link':absolute_url
            #}
             
            # Fetch Multiple Links
            yield response.follow(url = country_link, callable = self.parse_country())

    def parse_country(self, response):
        response.xpath('(//table[@class = "table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        response.xpath("(//table[@contains(@class, 'table')])[1]/tbody/tr")
        pass
