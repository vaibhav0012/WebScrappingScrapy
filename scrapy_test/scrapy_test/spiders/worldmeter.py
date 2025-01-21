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
            yield response.follow(url = country_link, callback = self.parse_country, meta={'country':country_name})

    def parse_country(self, response):
        # Getting country names and each row element inside the population table
        country = response.request.meta['country']
        rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")  # You can also use the whole class value  --> response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        # Looping through the rows list
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yearly_change_percentage = row.xpath(".//td[3]/text()").get()
            yearly_change = row.xpath(".//td[4]/text()").get()
            migrants_net = row.xpath(".//td[5]/text()").get()
            median_age = row.xpath(".//td[6]/text()").get()
            fertility_rate = row.xpath(".//td[7]/text()").get()
            density = row.xpath(".//td[8]/text()").get()
            urban_pop_percentage = row.xpath(".//td[9]/text()").get()
            urbal_population = row.xpath(".//td[10]/text()").get()
            country_share_of_pop = row.xpath(".//td[11]/text()").get()
            world_population = row.xpath(".//td[12]/text()").get()
            global_rank = row.xpath(".//td[13]/text()").get()



            # Return data extracted
            yield {
                'country':country,
                'year': year,
                'population':population,
                'yearly_change_percentage':yearly_change_percentage,
                'yearly_change':yearly_change,
                'migrants_net':migrants_net,
                'median_age':median_age,
                'fertility_rate':fertility_rate,
                'density':density,
                'urban_pop_percentage':urban_pop_percentage,
                'urbal_population':urbal_population,
                'country_share_of_pop':country_share_of_pop,
                'world_population':world_population,
                'global_rank':global_rank
            }

