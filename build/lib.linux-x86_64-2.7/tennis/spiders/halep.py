# -*- coding: utf-8 -*-
import scrapy


class HalepSpider(scrapy.Spider):
    name = "halep"
    allowed_domains = ["http://gametime.i2.ca"]
    start_urls = ['http://gametime.i2.ca/bel/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'davidjagoe', 'password': 'quizzy'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        yield {'ok': 'yes'}
        # return response.body
