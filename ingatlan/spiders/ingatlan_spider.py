# coding=utf-8
import scrapy
import logging
import re
from items import IngatlanItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from models import IngatlanDB, ArDB, db_connect, create_table

class IngatlanSpider(scrapy.Spider):
    name = "ingatlan"
    start_urls = [
        'https://ingatlan.com/lista/elado+lakas+ujlipotvaros',
        'https://ingatlan.com/lista/elado+lakas+ujpest-kozpont',
        'https://ingatlan.com/szukites/elado+haz+xvi-ker',
        'https://ingatlan.com/szukites/elado+haz+xvii-ker',
        'https://ingatlan.com/szukites/elado+haz+xviii-ker',
        'https://ingatlan.com/szukites/elado+haz+xix-ker',
        'https://ingatlan.com/szukites/elado+haz+xx-ker',
        'https://ingatlan.com/szukites/elado+haz+gyomro',
        'https://ingatlan.com/szukites/elado+haz+csomor',
        'https://ingatlan.com/szukites/elado+haz+maglod',
        'https://ingatlan.com/szukites/elado+haz+nagytarcsa',
    ]

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
    def parse(self, response):
        session = self.Session()
        for hirdetes in response.css('div.listing__card'):
            # parsing
            parsed_short = {
                'ar': self.millions_to_int(hirdetes.css('div.price::text').re_first(r'[0-9.]+')),
                'id': hirdetes.css('a.listing__thumbnail::attr("href")').re_first(r'[0-9]+$')
            }
            # checking DB for latest price
            hirdetes_exists = session.query(exists().where(ArDB.ingatlan_id==parsed_short['id'])).scalar()
            try:
                ar_in_db = session.query(ArDB).filter(ArDB.ingatlan_id==parsed_short['id']).order_by(ArDB.frissitve.desc()).one().ar
            except:
                ar_in_db = 0

            # adding, updating in DB
            if (not hirdetes_exists):
                logging.info('ADDING NEW INGATLAN: '+str(parsed_short['id']))
                yield response.follow(hirdetes.css('a.listing__thumbnail::attr("href")').extract_first(), self.parse_details)    
            elif (ar_in_db != parsed_short['ar']):
                logging.info('HAVE THAT INGATLAN('+str(parsed_short['id'])+'), UPDATING PRICE TO: ' + str(parsed_short['ar']))
                ar = ArDB()
                ar.ar = parsed_short['ar']
                ar.ingatlan_id = parsed_short['id']
                try:
                    session.add(ar)
                    session.commit()
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
            else:
                logging.info('WE ALREADY HAVE THAT INGATLAN:'+str(parsed_short['id']))


        next_page = response.xpath("//a[contains(@class,'pagination__button') and contains(.,'vetkez')]/@href").extract_first()
        logging.info("NEXT PAGE:"+str(next_page))
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_details(self, response):
        parsed_data = {
            'id': re.search(r'[0-9]+$', response.request.url).group(),
            'ar': str(self.millions_to_int(response.css('div.parameter-price span.parameter-value::text').re_first(r'^([\d,]+)').replace(",", "."))),
            'cim': response.xpath('//meta[@property="og:title"]/@content').re_first(r'(?:-\s)([^#]*)'),
            'hirdetes_tipus': response.css('div.listing-subtype::text').re_first(r'^([\w\-]+)'),
            'epites_tipus': response.css('div.listing-subtype::text').re_first(r'^(?:\S+\s){1}(\S+)'),
            'ingatlan_tipus': response.css('div.listing-subtype::text').re_first(r'(?:\s)(\S+)$'),
            'alapterulet': response.css('div.parameter-area-size span.parameter-value::text').re_first(r'(\d*)'),
            'telekterulet': response.css('div.parameter-lot-size span.parameter-value::text').re_first(r'(\d*)'),
            'szobak_egesz': response.css('div.parameter-room span.parameter-value::text').re_first(r'^\s*(\d*)'),
            'szobak_fel': response.css('div.parameter-room span.parameter-value::text').re_first(r'(?:\+\s)(\d)(?:\sf)', default="0"),
            # adatlap
            'ingatlan_allapota': response.xpath('//div[@class="paramterers"]//td[contains(.,"Ingatlan")]/../td[2]/text()').extract_first(),
            'epites_eve': response.xpath('//div[@class="paramterers"]//td[contains(.,"ve") and contains(.,"s ")]/../td[2]/text()').re_first(r'([\d-]*)'),
            'komfort': response.xpath('//div[@class="paramterers"]//td[contains(.,"Komfort")]/../td[2]/text()').extract_first(),
            'energia_tanusitvany': response.xpath('//div[@class="paramterers"]//td[contains(.,"Energiatan")]/../td[2]/text()').extract_first(),
            'emelet': response.xpath('//div[@class="paramterers"]//td[contains(.,"Emelet")]/../td[2]/text()').extract_first(),
            'epulet_szintjei': response.xpath('//div[@class="paramterers"]//td[contains(.,"let szintjei")]/../td[2]/text()').extract_first(),
            'lift': response.xpath('//div[@class="paramterers"]//td[contains(.,"Lift")]/../td[2]/text()').extract_first(),
            'belmagassag': response.xpath('//div[@class="paramterers"]//td[contains(.,"Belmagass")]/../td[2]/text()').extract_first(),
            'futes': response.xpath('//div[@class="paramterers"]//td[contains(.,"F") and contains(.,"t")]/../td[2]/text()').extract_first(),
            'legkondicionalo': response.xpath('//div[@class="paramterers"]//td[contains(.,"gkondicion")]/../td[2]/text()').extract_first(),
            'rezsikoltseg': response.xpath('//div[@class="paramterers"]//td[contains(.,"Rezsik")]/../td[2]/text()').re_first(r'([\d ]*)'),
            'akadalymentesitett': response.xpath('//div[@class="paramterers"]//td[contains(.,"lymentes")]/../td[2]/text()').extract_first(),
            'furdo_es_wc': response.xpath('//div[@class="paramterers"]//td[contains(.," WC")]/../td[2]/text()').extract_first(),
            'tajolas': response.xpath('//div[@class="paramterers"]//td[contains(.," jol")]/../td[2]/text()').extract_first(),
            'kilatas': response.xpath('//div[@class="paramterers"]//td[contains(.," Kil")]/../td[2]/text()').extract_first(),
            'erkely': response.xpath('//div[@class="paramterers"]//td[contains(.," Erk")]/../td[2]/text()').re_first(r'([\d\.]*)'),
            'kertkapcsolatos': response.xpath('//div[@class="paramterers"]//td[contains(.," Kertkapcsolatos")]/../td[2]/text()').extract_first(),
            'parkolas': response.xpath('//div[@class="paramterers"]//td[contains(.," Parkol")]/../td[2]/text()').extract_first(),
            'tetoter': response.xpath('//div[@class="paramterers"]//td[contains(.," Tet")]/../td[2]/text()').extract_first(),
            'pince': response.xpath('//div[@class="paramterers"]//td[contains(.,"Pince")]/../td[2]/text()').extract_first(),
            'panelprogram': response.xpath('//div[@class="paramterers"]//td[contains(.," Panelprogram")]/../td[2]/text()').extract_first(),
            'parkolohely_ara': response.xpath('//div[@class="paramterers"]//td[contains(.,"hely ") and contains(.,"Park")]/../td[2]/text()').extract_first(),
            'magan_hirdetes': (response.css('div.agent-profile').extract_first() is None)
        }
        self.process_data(parsed_data)
        yield IngatlanItem(parsed_data)

    def process_data(self, target):
        for key, value in target.items():
            if (value == "nincs megadva"):
                target[key] = None
            elif (value is not None and isinstance(value, str) and value.replace(" ", "").isdigit()):
                target[key] = int(value.replace(" ", ""))
            elif (value == 'nem' or value == 'nincs' or value == u'3 m-nél alacsonyabb'):
                target[key] = False
            elif (value == 'igen' or value == 'van' or value == u'részt vett' or value == u'3 m vagy magasabb'):
                target[key] = True
            elif (value == u'szuterén'):
                target[key] = -1
            elif (value == u'földszint'):
                target[key] = 0
            elif (value == u'félemelet'):
                target[key] = 0.5
            elif (value == u'10 felett' or value == u'több mint 10'):
                target[key] = 11
            elif (value == u'földszintes'):
                target[key] = 1
    
    def millions_to_int(self, target):
        return int(round(float(target)*1000000, -3))
            