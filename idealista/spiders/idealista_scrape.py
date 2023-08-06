import scrapy


class IdealistaScrapeSpider(scrapy.Spider):
    name = 'idealista_scrape'
    allowed_domains = ['idealista.com']
    start_urls = ['https://www.idealista.com/venta-viviendas/salamanca-salamanca/']
    page_number = 2

    def parse(self, response):
        for houses in response.css('.item-info-container'):
            yield {
                'title' : houses.css('a.item-link::text').get(),
                'price' : houses.css('span.item-price.h2-simulated::text').get(),
                'rooms' : houses.css('span.item-detail:nth-child(1)::text').get(),
                'mtts' : houses.css('span.item-detail:nth-child(2)::text').get(),
                'floor' : houses.css('span.item-detail:nth-child(3)::text').get() ,
                'link' : houses.css('a.item-link::attr(href)').get(),
                'description' : houses.css('.ellipsis::text').get(),
            }

        next_page = 'https://www.idealista.com/venta-viviendas/salamanca-salamanca/pagina-' + str(IdealistaScrapeSpider.page_number) + '.htm'
        if IdealistaScrapeSpider.page_number < 200:
            IdealistaScrapeSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)