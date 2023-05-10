from ..itemsloaders import ChocolateProductLoader
from ..items import ChocolateItem
import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        items = response.css("product-item")

        for item in items:
            chocolate = ChocolateProductLoader(item=ChocolateItem(), selector=item)
            chocolate.add_css("nombre", "a.product-item-meta__title::text")
            chocolate.add_css("precio", "span.price")
            chocolate.add_css("url", "div.product-item-meta a::attr(href)")
            yield chocolate.load_item()

        next_page = response.css("[rel='next'] ::attr(href)").get()
        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page
            yield scrapy.Request(url=next_page_url, callback=self.parse)
