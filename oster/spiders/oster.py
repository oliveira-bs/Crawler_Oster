import json
import locale
import re
from datetime import datetime

import requests
from oster.custom_settings.oster_settings import settings
from scrapy.http import Request
from scrapy.spiders import SitemapSpider

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


class OsterSpider(SitemapSpider):
    name = 'oster_crawler'
    allowed_domains = ['www.oster.com.br']
    sitemap_urls = ['https://www.oster.com.br/sitemap/sitemap.xml']
    sitemap_rules = [('', 'parse_listpage')]

    sitemap_follow = [
        r'[\d\w:/.](category-)[\d\w:/.]'
    ]

    other_urls: list[str] = []

    custom_settings = settings()

    def parse_listpage(self, response):
        urlspage_jscript = []

        var_pagecount = response.xpath(
            '//*/div/script[contains(@type,"text/javascript")]/text()'
        ).getall()
        for text in var_pagecount:
            char_identif = "var pagecount"
            prefix_identif = ").load('"
            sufix_identif = "' + pageclickednumber"
            if char_identif in text:
                url_standard_jscript = text.split(
                    prefix_identif)[-1].split(sufix_identif)[0]
                url_standard_jscript = url_standard_jscript.strip()
                url_standard_jscript = re.sub(
                    "(PS=\\d+)", "PS=50", url_standard_jscript)

                page = 1

                while True:
                    page_jscript = "".join(
                        ("https://", self.allowed_domains[0],
                         url_standard_jscript, str(page)))

                    page += 1

                    payload = {}
                    headers = {}

                    request_nextpage = requests.get(
                        url=page_jscript, headers=headers, data=payload)
                    size_nextpage = len(request_nextpage.text)

                    if size_nextpage < 10:
                        break
                    urlspage_jscript.append(page_jscript)

                for url_jscript in urlspage_jscript:
                    yield Request(url=url_jscript, callback=self.parse)

    def parse(self, response):
        url_products = response.xpath(
            '//*[contains(@class,"shelf-product")]/*/h3/a/@href').getall()
        for url in url_products:
            yield Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        json_addData = response.xpath('//*/script/text()').getall()
        for text in json_addData:
            prefix_identif = "vtex.events.addData("
            sufix_identif = ");"
            if prefix_identif in text:
                data_json = text.split(
                    prefix_identif)[-1].split(sufix_identif)[0]
                data_json = data_json.strip()
                data_json = json.loads(data_json)

        pageUrl = data_json["pageUrl"]

        if "404" in pageUrl:
            raise '=== Produto Esgotado ==='

        for text in json_addData:
            prefix_identif_2 = "skuJson_0 ="
            sufix_identif_2 = ";CATALOG_SDK"
            if prefix_identif_2 in text:
                data_json_2 = text.split(
                    prefix_identif_2)[-1].split(sufix_identif_2)[0]
                data_json_2 = data_json_2.strip()
                data_json_2 = json.loads(data_json_2)

        price = data_json["productPriceTo"]
        try:
            price = locale.atof(price)
        except ValueError:
            pass
        name = data_json_2["name"]
        try:
            gtin = data_json["productEans"]
        except None:
            gtin = None
        sku = [key for key, value in data_json["skuStocks"].items()]

        currency = data_json_2["skus"][0]["taxFormated"].split()[0]
        seller = data_json_2["skus"][0]["seller"]
        category = data_json["productCategoryName"]
        image = data_json_2["skus"][0]["image"]
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield {
            "gtin": gtin,
            "name": name,
            "currency": currency,
            "price": price,
            "category": category,
            "sku": sku,
            "seller": seller,
            "pageUrl": pageUrl,
            "image": image,
            "created_at": created_at,
        }
