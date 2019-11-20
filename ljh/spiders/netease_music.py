# -*- coding: utf-8 -*-
import scrapy


class NeteaseMusicSpider(scrapy.Spider):
    name = 'netease_music'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/playlist?id=3051693042']

    def parse(self, response):
        tr_list = response.css('table.m-table')
        print(tr_list.getall())
