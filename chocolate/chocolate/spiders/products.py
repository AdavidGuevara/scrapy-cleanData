from ..items import ChocolateItem
import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        items = response.css("product-item")

        product = ChocolateItem()
        for item in items:
            product["nombre"] = item.css("a.product-item-meta__title::text").get()
            product["precio"] = (
                item.css("span.price")
                .get()
                .replace('<span class="price">\n', "")
                .replace('              <span class="visually-hidden">Sale price', "")
                .replace("</span>", "")
                .replace('<span class="price price--highlight">\n', "")
                .replace("\n", "")
                .replace("From ", "")
            )
            product["url"] = item.css("div.product-item-meta a").attrib["href"]
            yield {"nombre": product["nombre"], "precio": product["precio"]}

        next_page = response.css("[rel='next'] ::attr(href)").get()
        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page
            yield scrapy.Request(url=next_page_url, callback=self.parse)
