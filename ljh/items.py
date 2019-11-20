# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LjhItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanItem(scrapy.Item):
    picture = scrapy.Field()
    main_page = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    star = scrapy.Field()
    quote = scrapy.Field()


class FilmItem(scrapy.Item):
    # print(title, year, directors, writers, actors, types, region, release_date, size, star, star_percent, sep='\n')
    film_id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    actors = scrapy.Field()
    types = scrapy.Field()
    region = scrapy.Field()
    release_date = scrapy.Field()
    size = scrapy.Field()
    star = scrapy.Field()
    star_percent = scrapy.Field()
    comment_num = scrapy.Field()
    src = scrapy.Field()


class CelebrityItem(scrapy.Item):
    celebrity_id = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    constellation = scrapy.Field()
    birthday = scrapy.Field()
    date_of_death = scrapy.Field()
    birthplace = scrapy.Field()
    job = scrapy.Field()
    other_foreign_names = scrapy.Field()
    other_chinese_names = scrapy.Field()
    families = scrapy.Field()
    human_src = scrapy.Field()


class DirectorItem(scrapy.Item):
    film_id = scrapy.Field()
    celebrity_id = scrapy.Field()


class WriterItem(scrapy.Item):
    film_id = scrapy.Field()
    celebrity_id = scrapy.Field()


class ActorItem(scrapy.Item):
    film_id = scrapy.Field()
    celebrity_id = scrapy.Field()
