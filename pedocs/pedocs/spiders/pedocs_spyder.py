# -*- coding: utf-8 -*-
# File: xxx.py

# Copyright 2022 Dr. Janis Meyer. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import scrapy


class AnnReportLinkSpider(scrapy.Spider):
    name = "pedocs"
    start_urls = ['https://www.pedocs.de/zeitschriften.php?zst=6989']
    custom_settings = {
        'FEEDS': { '/home/janis/Tests/scrapy/data.csv': { 'format': 'csv',}}
        }

    def parse(self, response):
        for rel_link in response.css('ul.browsingliste a::attr(href)'):
            absolute_link = response.urljoin(rel_link.get())
            current_response = response.follow(absolute_link, callback=self.parse_per_year_page)
            yield current_response

    def parse_per_year_page(self,  response):
        for rel_link in response.css('ul.browsingliste a::attr(href)'):
            absolute_link = response.urljoin(rel_link.get())

            abs_str=str(absolute_link)
            if "lucene_ergebnis" in abs_str:
                current_response = response.follow(absolute_link, callback=self.parse_per_journal)
                yield current_response

    def parse_per_journal(self, response):
        for rel_link in response.css('span.book-list-item a::attr(href)').getall():
            if "frontdoor" in rel_link:
                absolute_link = response.urljoin(rel_link)
                current_response = response.follow(absolute_link, callback=self.parse_article_meta_data)
                yield current_response

    def parse_article_meta_data(self, response):

        # determine scope
        headline = response.css('table.a5-table-responsive tr td[itemprop="headline"] span.contentLine::text').get()
        author = response.css('table.a5-table-responsive tr a[itemprop="author"] span.contentLine::text').get()
        reference = response.css('table.a5-table-responsive tr td[itemprop="isPartOf"] span.contentLine::text').get()
        year_published = response.css('table.a5-table-responsive tr td[itemprop="datePublished"]::text').get()
        download_link = response.css('table.a5-table-responsive tr a.a5-book-list-item-fulltext::attr(href)').get()
        yield {"headline": headline,
               "author": author,
               "reference": reference,
               "year_published": year_published,
               "file_urls": [download_link]}
