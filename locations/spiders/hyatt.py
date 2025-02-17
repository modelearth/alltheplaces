import json
import scrapy
import logging

from locations.items import GeojsonPointItem


class HyattSpider(scrapy.Spider):

    name = "hyatt"
    item_attributes = { 'brand': "Hyatt", 'brand_wikidata': "Q1425063" }
    allowed_domains = ["hyatt.com"]
    download_delay = 1.5  # delay required to avoid getting temporarily blocked from hyatt.com (403s)

    base_url = 'https://www.hyatt.com/explore-hotels/partial?regionGroup={region}&categories=&brands='

    regions = (
        '1-NorthAmerica',
        '2-CaribbeanAndLatinAmerica',
        '3-Europe',
        '4-AfricaAndMiddleEast',
        '5-Asia',
        '6-Australia'
    )

    def start_requests(self):
        for region in self.regions:
            yield scrapy.Request(url=self.base_url.format(region=region))

    def parse_hotel(self, response):
        data = json.loads(response.xpath('//script[contains(text(), "streetAddress")]/text()').extract_first())

        properties = {
            'ref': "_".join(response.url.split('/')[-3:]),
            'name': data["name"],
            'addr_full': data["address"]["streetAddress"],
            'city': data["address"]["addressLocality"],
            'state': data["address"]["addressRegion"],
            'postcode': data["address"]["postalCode"],
            'country': data["address"]["addressCountry"],
            'phone': data.get("telephone", None),
            'lat': float(data["geo"]["latitude"]),
            'lon': float(data["geo"]["longitude"]),
            'website': response.url,
        }

        yield GeojsonPointItem(**properties)

    def parse(self, response):
        urls = response.xpath('//li[contains(@class, "property")]/a/@href').extract()

        for url in urls:
            yield scrapy.Request(response.urljoin(url), headers={'Referer': None}, callback=self.parse_hotel)
