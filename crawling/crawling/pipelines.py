# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import datetime

import jdatetime
from django.db import IntegrityError


def month_name_to_number(param):
    month_dict = {
        "فروردین": 1,
        "اردیبهشت": 2,
        "خرداد": 3,
        "تیر": 4,
        "مرداد": 5,
        "شهریور": 6,
        "مهر": 7,
        "آبان": 8,
        "آذر": 9,
        "دی": 10,
        "بهمن": 11,
        "اسفند": 12,
    }
    return month_dict.get(param)


def clean_title(param):
    return param.strip()


def clean_category(param):
    if 'کوین' in param:
        if 'بیت' in param:
            return 'btc'
        elif 'آلت' or 'الت':
            return 'atc'
        else:
            return None
    elif 'اتریوم' in param:
        return 'eth'
    else:
        return None


def clean_description(param):
    return param[:150] + '...'


def clean_path(param):
    return param.split('/')[-2]


def reformat_date_time(param):
    if re.match(r'\d{4}-\d{1,2}-\d{1,2}', param):
        return datetime.datetime.strptime(param, '%Y-%m-%d').date()
    elif re.match(r'\d{1,2} .+ \d{4}', param):
        day = int(param.split(' ')[0])
        month = int(month_name_to_number(param.split(' ')[1]))
        year = int(param.split(' ')[2])
        return jdatetime.date(
            day=day, month=month, year=year
        ).togregorian()
    else:
        return None


class CcNewsCrawlingPipeline(object):
    duplicate_record_flag = False

    def process_item(self, item, spider):
        item['title'] = clean_title(item['title'])
        item['category'] = clean_category(item['category'])
        item['description'] = clean_description(item['description'])
        item['publish_date'] = reformat_date_time(item['publish_date'])
        item['path'] = clean_path(item['source'])

        try:
            item.save()
            return item
        except IntegrityError:
            self.duplicate_record_flag = True
            return None

    def open_spider(self, spider):
        spider.my_pipeline = self
