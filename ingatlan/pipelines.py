# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from models import IngatlanDB, ArDB, db_connect, create_table

class IngatlanPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        session = self.Session()
        ingatlan_ar = item.pop('ar')  # removing price from opject

        # save if ingatlan does not exists
        ingatlan_exists = session.query(exists().where(IngatlanDB.id==item['id'])).scalar()
        if (not ingatlan_exists):
            ingatlan = IngatlanDB(**item)
        
            try:
                session.add(ingatlan)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            logging.warning('ALREADY HAVING THAT ingatlan: '+ str(item['id']))
        
        ar = ArDB()
        ar.ar = ingatlan_ar
        ar.ingatlan_id = item['id']

        # save if ar does not exists
        ar_exists = session.query(exists().where(ArDB.ingatlan_id==item['id'] and ArDB.ar==ingatlan_ar)).scalar()
        if (not ar_exists):
            try:
                session.add(ar)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            logging.warning('ALREADY HAVING THAT PRICE: ' + str(ingatlan_ar))

        return item

