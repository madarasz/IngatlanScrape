import datetime
from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)
from sqlalchemy.dialects.mysql import INTEGER

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class IngatlanDB(DeclarativeBase):
    __tablename__ = "ingatlan"

    id = Column('id', INTEGER(unsigned=True), primary_key=True)
    frissitve = Column('frissitve', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)

    # text
    cim = Column('cim', Text(length=60))
    hirdetes_tipus = Column('hirdetes_tipus', Text(length=10))
    epites_tipus = Column('epites_tipus', Text(length=10))
    ingatlan_tipus = Column('ingatlan_tipus', Text(length=10))
    energia_tanusitvany = Column('energia_tanusitvany', Text(length=10), nullable=True)
    ingatlan_allapota = Column('ingatlan_allapota', Text(length=30), nullable=True)
    epites_eve = Column('epites_eve', Text(length=30), nullable=True)
    komfort = Column('komfort', Text(length=30), nullable=True)
    futes = Column('futes', Text(length=30), nullable=True)
    furdo_es_wc = Column('furdo_es_wc', Text(length=30), nullable=True)
    tajolas = Column('tajolas', Text(length=30), nullable=True)
    kilatas = Column('kilatas', Text(length=30), nullable=True)
    parkolas = Column('parkolas', Text(length=30), nullable=True)
    tetoter = Column('tetoter', Text(length=30), nullable=True)
    parkolohely_ara = Column('parkolohely_ara', Text(length=30), nullable=True)

    # integer
    alapterulet = Column('alapterulet', INTEGER(unsigned=True))
    telekterulet = Column('telekterulet', INTEGER(unsigned=True))
    szobak_egesz = Column('szobak_egesz', INTEGER(unsigned=True))
    szobak_fel = Column('szobak_fel', INTEGER(unsigned=True))
    epulet_szintjei = Column('epulet_szintjei', INTEGER(unsigned=True), nullable=True)
    rezsikoltseg = Column('rezsikoltseg', INTEGER(unsigned=True), nullable=True)
    erkely = Column('erkely', INTEGER(unsigned=True), nullable=True)
    
    # float
    emelet = Column('emelet', Float(), nullable=True)
    
    # boolean
    lift = Column('lift', Boolean(), nullable=True)
    belmagassag = Column('belmagassag', Boolean(), nullable=True)
    legkondicionalo = Column('legkondicionalo', Boolean(), nullable=True)
    akadalymentesitett = Column('akadalymentesitett', Boolean(), nullable=True)
    kertkapcsolatos = Column('kertkapcsolatos', Boolean(), nullable=True)
    panelprogram = Column('panelprogram', Boolean(), nullable=True)
    pince = Column('pince', Boolean(), nullable=True)
    magan_hirdetes = Column('magan_hirdetes', Boolean(), nullable=True)

class ArDB(DeclarativeBase):
    __tablename__ = "ar"

    id = Column('id', INTEGER(unsigned=True), primary_key=True)
    frissitve = Column('frissitve', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    ingatlan_id = Column('ingatlan_id', INTEGER(unsigned=True))
    ar = Column('ar', INTEGER(unsigned=True))
    