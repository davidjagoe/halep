# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime


class HalepSpider(scrapy.Spider):
    name = "halep"
    allowed_domains = ["http://gametime.i2.ca", "gametime.i2.ca"]
    start_urls = ['http://gametime.i2.ca/bel/login.php']

    def _read_credentials(self):
        with open("/usr/local/halep/credentials") as f:
            line = f.readline()
        username, password = line.strip().split(",")
        return {'username': username, 'password': password}
    
    def parse(self, response):
        credentials = self._read_credentials()
        return scrapy.FormRequest.from_response(
            response,
            formdata=credentials,
            callback=self.after_login
        )

    def after_login(self, response):
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        filename = "/var/halep/{0}".format(timestamp)
        with  open(filename, "wb") as f:
            f.write(response.body)

