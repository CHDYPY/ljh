# -*- coding: utf-8 -*-
import json
import random
import time

import scrapy

from ljh.items import *


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    mapping = {'姓名': 'name', '性别': 'gender', '星座': 'constellation', '出生日期': 'birthday', '去世日期': 'date_of_death',
               '出生地': 'birthplace',
               '职业': 'job', '更多外文名': 'other_foreign_names', '更多中文名': 'other_chinese_names', '生卒日期': 'birthday',
               '家庭成员': 'families'}

    # start_urls = ['https://movie.douban.com/top250']
    # start_urls = ['https://movie.douban.com/subject/30304469/?tag=%E7%83%AD%E9%97%A8&from=gaia']

    def start_requests(self):
        # yield scrapy.Request(url='https://movie.douban.com/subject/1292052/', callback=self.parse_film_page)
        # yield scrapy.Request(url='https://movie.douban.com/top250', callback=self.parse)
        yield scrapy.Request(
            url='https://movie.douban.com/j/search_subjects?type=movie&tag=%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86&sort=recommend&page_limit=2000&page_start=0',
            callback=self.parse_json)

    def parse_json(self, response):
        res = json.loads(response.body_as_unicode())['subjects']
        for i in res:
            yield response.follow(i['url'], callback=self.parse_film_page)

    # def start_requests(self):
    #     # yield scrapy.Request(url='https://movie.douban.com/subject/1292052/', callback=self.parse_film_page)
    #     yield scrapy.Request(url='https://movie.douban.com/top250', callback=self.parse)
    #
    # def parse(self, response):
    #     res = response.css('ol.grid_view li div.item div.pic a::attr(href)').getall()
    #     for url in res:
    #         yield response.follow(url, callback=self.parse_film_page)
    #         # print(self.count, picture, main_page, title, description, star, quote)
    #     next = response.css('div.paginator span.next a::attr(href)').extract_first()
    #     if next is not None:
    #         yield response.follow(next, callback=self.parse)

    def parse_film_page(self, response):
        item = FilmItem()
        item['film_id'] = response.request.url.split('/')[4]
        item['title'] = response.css('#content > h1 > span:nth-child(1)::text').extract_first()
        item['year'] = response.css('#content > h1 > span.year::text').extract_first().replace('(', '').replace(')', '')
        item['directors'] = response.css('#info > span:nth-child(1) > span.attrs > a::text').getall()
        director_hrefs = response.css('#info > span:nth-child(1) > span.attrs > a::attr(href)').getall()
        item['writers'] = response.css('#info > span:nth-child(3) > span.attrs > a::text').getall()
        writer_hrefs = response.css('#info > span:nth-child(3) > span.attrs > a::attr(href)').getall()
        item['actors'] = response.css('#info > span.actor > span.attrs > a::text').getall()[:7]
        actor_hrefs = response.css('#info > span.actor > span.attrs > a::attr(href)').getall()[:7]
        item['types'] = response.css('#info > span[property="v:genre"]::text').getall()
        item['region'] = \
            response.css('#info').re(r'<span class="pl">制片国家/地区:</span>.*<br>')[0].split('</span>')[1].split('<br>')[0]
        item['release_date'] = response.css('#info > span[property="v:initialReleaseDate"]::text').extract_first()
        item['size'] = response.css('#info > span[property="v:runtime"]::attr(content)').extract_first()
        item['star'] = response.css(
            '#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong::text').extract_first()
        item['star_percent'] = response.css(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div > span.rating_per::text').getall()
        item['comment_num'] = response.css(
            '#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span::text').extract_first()
        item['src'] = response.css(
            '#mainpic > a > img::attr(src)').extract_first()
        # print(title, year, directors, writers, actors, types, region, release_date, size, star, star_percent, sep='\n')
        yield item
        for href in director_hrefs:
            d_item = DirectorItem()
            d_item['film_id'] = item['film_id']
            d_item['celebrity_id'] = href.split('/')[2]
            yield d_item
        for href in writer_hrefs:
            w_item = WriterItem()
            w_item['film_id'] = item['film_id']
            w_item['celebrity_id'] = href.split('/')[2]
            yield w_item
        for href in actor_hrefs:
            a_item = ActorItem()
            a_item['film_id'] = item['film_id']
            a_item['celebrity_id'] = href.split('/')[2]
            yield a_item
        for i in list(director_hrefs) + writer_hrefs + actor_hrefs:
            yield response.follow(i, callback=self.parse_celebrity_page)

    def parse_celebrity_page(self, response):
        name = response.css('#content > h1::text').extract_first()
        ul = response.css('#headline > div.info > ul > li::text').getall()
        info_names = ['姓名'] + response.css('#headline > div.info > ul > li > span::text').getall()
        del info_names[-1]
        info_list = [name]
        for s in ul:
            s = s.replace(':', '').strip()
            if len(s) > 0:
                info_list.append(s)
        # result = {k: v for k, v in zip(info_names, info_list)}
        # print(result)
        item = CelebrityItem()
        item['celebrity_id'] = response.request.url.split('/')[4]
        item['human_src'] = response.css('#headline > div.pic > a > img::attr(src)').extract_first()
        for k in self.mapping:
            item[self.mapping[k]] = ''
        for k, v in zip(info_names, info_list):
            if k == '生卒日期':
                birthday_and_date_of_death = v.split('至')
                item['birthday'] = birthday_and_date_of_death[0]
                item['date_of_death'] = birthday_and_date_of_death[1]
            else:
                item[self.mapping[k]] = v
        yield item
