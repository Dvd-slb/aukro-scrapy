import re
import scrapy
from ..items import AukroItem


class AukroSpider(scrapy.Spider):
    name = 'aukro'
    pg_number = 2
    start_urls = [f'https://aukro.cz/uzivatel/paleto/nabidky?page=1&size=16&sort=endingTime_ASC&auction=true']

    def parse(self, response, **kwargs):
        next_page = f'https://aukro.cz/uzivatel/paleto/nabidky?page={self.pg_number}&size=16&sort=endingTime_ASC&auction=true'
        if self.pg_number < 5:
            self.pg_number += 1
            yield response.follow(next_page, callback=self.parse)
        stage = response.css("a.doNotTrackViewCount::attr(href)").getall()
        for box in stage[::2]:
            link = "https://aukro.cz"+box
            yield response.follow(link, callback=self.detail_parse)

    def detail_parse(self, response):
        items = AukroItem()
        max_bid = ""

        name = response.css(".md\:tw-mr-20::text").re(r"#\w+")[0]
        link = response.url
        category = response.css("tbody td::text").getall()[0] + " a " + response.css("tbody td::text").getall()[3]
        dead_line = response.css(".text-bold::text").get()
        max_bid_info = response.css(".tw-text-5xl::text").get()
        for x in max_bid_info:
            if x.isnumeric():
                max_bid += x
        max_bid = int(max_bid)
        total_price = int(response.css("tbody td::text").getall()[-1].replace(" ", ""))

        item_info = self.top_item_info(response)
        top_item_id = item_info[0]
        top_item_price = item_info[1]
        top_item_quantity = item_info[2]
        top_item_description = item_info[3]
        top_item_img = item_info[4]

        items["name"] = name
        items["link"] = link
        items["category"] = category
        items["dead_line"] = dead_line
        items["max_bid"] = max_bid
        items["total_price"] = total_price
        items["top_item_id"] = top_item_id
        items["top_item_price"] = top_item_price
        items["top_item_quantity"] = top_item_quantity
        items["top_item_description"] = top_item_description
        items["top_item_img"] = top_item_img

        yield items

    def top_item_info(self, response):
        most_price = response.css("div.plt-product-desc p::text").re(r"Původní cena:.*?K")
        price_list = []
        for x in most_price[:int(len(most_price)/2)]:
            price = ""
            numbers = re.findall(r"\d+", x)
            if len(numbers) > 1:
                for n in numbers:
                    price += n
            else:
                price = numbers[0]
            price_list.append(int(price))
        top_item_price = max(price_list)

        top_item_index = price_list.index(top_item_price)

        top_item_description = response.css("div.plt-product-desc p::text").re(r"Popis.*")[top_item_index]

        count = response.css("div.plt-product-desc p::text").re(r"Počet.*")[top_item_index]
        top_item_count = re.findall(r"\d+", count)
        top_item_count = int(top_item_count[0])

        id = response.css("div.plt-product-desc strong::text").getall()[top_item_index]
        top_item_id = re.findall(r":.*", id)[0].strip(": ")

        top_item_img = response.css("div.plt-product-img img::attr(src)").getall()[top_item_index]

        return top_item_id, top_item_price, top_item_count, top_item_description, top_item_img
