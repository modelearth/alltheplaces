# -*- coding: utf-8 -*-
import json

import scrapy

from locations.items import GeojsonPointItem


class United_surgical_partners_internationalSpider(scrapy.Spider):
    name = "united_surgical_partners_international"
    item_attributes = {'brand': 'United Surgical Partners International'}
    allowed_domains = ["uspi.com"]
    start_urls = [
        'https://webwidgets.q4api.com/v1/fusion?sql=SELECT%20*%20FROM%201MgAq-T0B9gtHKnM0RbfBi8xeJRwmCQftIEvcNdY0Olw&key=AIzaSyBjtj8mMa96IpYNmDjwH-EbmMT3RpeU6ao',
    ]

    def parse(self, response):
        data = json.loads(response.body_as_unicode())["rows"]

        for i, item in enumerate(data):
            if len(item) == 12:
                website = item[11]
            else:
                website = 'na'
            properties = {
                'name': item[0],
                'addr_full': item[3] + " " + item[4],
                'city': item[5],
                'state': item[6],
                'postcode': item[7],
                'phone': item[10],
                'ref': item[0] + ", " + item[5] + ", " + item[6],
                'website': website,
                'lat': item[8],
                'lon': item[9],
            }
            yield GeojsonPointItem(**properties)