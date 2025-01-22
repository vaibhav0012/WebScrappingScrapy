import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.in"]
    start_urls = ["https://www.audible.in/search"]

    def start_requests(self):
        # Editing the default headers (user-agent)
        yield scrapy.Request(url='https://www.audible.in/search/', callback=self.parse,
                       headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})

    def parse(self, response):
        product_container = response.xpath('//div[@class="adbl-impression-container "]//li[contains(@class, "productListItem")]')

        for product in product_container:
            book_title = product.xpath('.//li[contains(@class, "bc-heading")]/a/text()').get()
            book_author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            book_length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()

            yield{
                'title': book_title,
                'author':book_author,
                'length':book_length,
                'User-Agent':response.request.headers['User-Agent'],
            }
        

        pagination = response.xpath('//ul[contains(@class , "pagingElements")]')
        next_page_url = pagination.xpath('.//span[contains(@class , "nextButton")]/a/@href').get()
        button_disabled = pagination.xpath('.//span[contains(@class , "nextButton")]/a/@aria-disabled').get()

        # Going to the "next_page_url" link
        if next_page_url and button_disabled==None:
            yield response.follow(url=next_page_url, callback=self.parse,
                                  headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})
