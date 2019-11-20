# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ljh.items import *
import pymysql


class LjhPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='localhost', port=3306, user='root', password='740406', database='douban')
        self.add_film_sql = """
            INSERT INTO `t_film`(
                `film_id`,
                `title`,
                `year`,
                `types`,
                `region`,
                `release_date`,
                `size`,
                `star`,
                `star_percent`,
                `comment_num`,
                `src`
            ) 
            VALUES(
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
        """
        self.add_celebrity_sql = """
            INSERT INTO `t_celebrity` (
                `celebrity_id`,
                `name`,
                `gender`,
                `constellation`,
                `birthday`,
                `date_of_death`,
                `birthplace`,
                `job`,
                `other_foreign_names`,
                `other_chinese_names`,
                `families`,
                `human_src`
            ) 
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
             )
        """

        self.add_rel_fd_sql = """
            INSERT INTO t_film_director(film_id,celebrity_id)
            VALUES(
                %s,%s
            )
        """

        self.add_rel_fw_sql = """
            INSERT INTO t_film_writer(film_id,celebrity_id)
            VALUES(
                %s,%s
            )
        """

        self.add_rel_fa_sql = """
            INSERT INTO t_film_actor(film_id,celebrity_id)
            VALUES(
                %s,%s
            )
        """

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        if type(item) == FilmItem:
            cursor.execute(self.add_film_sql, [
                str(item['film_id']),
                str(item['title']),
                str(item['year']),
                # str(item['directors']),
                # str(item['writers']),
                # str(item['actors']),
                str(item['types']),
                str(item['region']),
                str(item['release_date']),
                str(item['size']),
                str(item['star']),
                str(item['star_percent']),
                str(item['comment_num']),
                str(item['src'])
            ])
        elif type(item) == CelebrityItem:
            cursor.execute(self.add_celebrity_sql, [
                str(item['celebrity_id']),
                str(item['name']),
                str(item['gender']),
                str(item['constellation']),
                str(item['birthday']),
                str(item['date_of_death']),
                str(item['birthplace']),
                str(item['job']),
                str(item['other_foreign_names']),
                str(item['other_chinese_names']),
                str(item['families']),
                str(item['human_src'])
            ])
        elif type(item) == DirectorItem:
            cursor.execute(self.add_rel_fd_sql, [str(item['film_id']), str(item['celebrity_id'])])
        elif type(item) == WriterItem:
            cursor.execute(self.add_rel_fw_sql, [str(item['film_id']), str(item['celebrity_id'])])
        elif type(item) == ActorItem:
            cursor.execute(self.add_rel_fa_sql, [str(item['film_id']), str(item['celebrity_id'])])
        else:
            pass
        self.db.commit()
        cursor.close()
        return item
