# -*- coding: utf-8 -*-
import scrapy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, func
from models import IngatlanDB, ArDB, db_connect, create_table
import logging
import re

class FindsoldingatlanSpider(scrapy.Spider):
    name = 'findSoldIngatlan'
    allowed_domains = ['ingatlan.com']
    handle_httpstatus_list = [301, 404]
    max_days = 3 # set max days here

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

        #make a list of not up-to-date prices
        datediff = (func.datediff(func.now(), func.max(ArDB.frissitve))).label('datediff')
        s = self.Session().query(ArDB.ingatlan_id).group_by(ArDB.ingatlan_id).having(datediff > self.max_days).having(func.max(ArDB.ar) > 0).all()
        self.start_urls = ['https://ingatlan.com/a/b/c/d/'+str(r) for r, in s]
        logging.info("Looking for prices older than {} days, found {} entries!".format(self.max_days, len(self.start_urls)))

    def parse(self, response):
        id = re.search(r'[0-9]+$', response.request.url).group()
        removed_ingatlan = response.xpath("//div[@class='errorpage__title' and contains(.,'A keresett hirdet')]").extract_first()
        if (removed_ingatlan is not None):
            ar = ArDB()
            ar.ingatlan_id = id
            ar.ar = 0
            session = self.Session()
            try:
                session.add(ar)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            logging.warning('Probably sold: {}'.format(id))
        else:
            logging.info('Ingatlan still up!')
        pass
