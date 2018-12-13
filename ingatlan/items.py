# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IngatlanItem(scrapy.Item):
    id = scrapy.Field()
    ar = scrapy.Field()
    cim = scrapy.Field()
    hirdetes_tipus = scrapy.Field()
    epites_tipus = scrapy.Field()
    ingatlan_tipus = scrapy.Field()
    alapterulet = scrapy.Field()
    telekterulet = scrapy.Field()
    szobak_egesz = scrapy.Field()
    szobak_fel = scrapy.Field()
    ingatlan_allapota = scrapy.Field()
    epites_eve = scrapy.Field()
    komfort = scrapy.Field()
    energia_tanusitvany = scrapy.Field()
    emelet = scrapy.Field()
    epulet_szintjei = scrapy.Field()
    lift = scrapy.Field()
    belmagassag = scrapy.Field()
    futes = scrapy.Field()
    legkondicionalo = scrapy.Field()
    akadalymentesitett = scrapy.Field()
    furdo_es_wc = scrapy.Field()
    tajolas = scrapy.Field()
    kilatas = scrapy.Field()
    erkely = scrapy.Field()
    kertkapcsolatos = scrapy.Field()
    rezsikoltseg = scrapy.Field()
    parkolas = scrapy.Field()
    tetoter = scrapy.Field()
    panelprogram = scrapy.Field()
    parkolohely_ara = scrapy.Field()
    pince = scrapy.Field()
    magan_hirdetes = scrapy.Field()

