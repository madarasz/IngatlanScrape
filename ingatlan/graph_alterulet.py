import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from models import db_connect, create_table, IngatlanDB, ArDB

from plotly.offline import iplot, init_notebook_mode
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os
import numpy as np
import re

engine = db_connect()
conn = engine.connect()

s = select([IngatlanDB.id, IngatlanDB.alapterulet, IngatlanDB.szobak_egesz, IngatlanDB.szobak_fel, IngatlanDB.cim, ArDB.ar]).where(IngatlanDB.id == ArDB.ingatlan_id).where(IngatlanDB.ingatlan_tipus == u'lakás').where(IngatlanDB.cim.like("%13. kerület%")).where(IngatlanDB.epites_tipus == u'tégla').where(ArDB.ar < 50000000).where(IngatlanDB.alapterulet < 100)
result = conn.execute(s).fetchall()
terulet = []
ar = []
szobak = []
hover_text = []
hol = []

alkeruletek = []
alkerulet_mapping = {}
for row in result:
    alkerulet = re.search(r'(?:\()(.*)(?:\))', row['cim']).group()
    if (alkerulet not in alkeruletek):
        alkeruletek.append(alkerulet)
for index, alkerulet in enumerate(alkeruletek):
    alkerulet_mapping[alkerulet] = index / (len(alkeruletek)-1)


for row in result:
    terulet.append(row['alapterulet'])
    ar.append(row['ar'])
    alkerulet = re.search(r'(?:\()(.*)(?:\))', row['cim']).group()
    hol.append(alkerulet_mapping[alkerulet])
    szobak.append(10+5*(row['szobak_egesz']+row['szobak_fel']*0.5))
    hover_text.append(alkerulet + " - Terulet: " + str(row['alapterulet']) + " - Tipus: " + " - Ar: " + str(row['ar']/1000000) + "M Ft - id: " + str(row['id'])) 

data = go.Scatter( 
    x=terulet,
    y=ar,
    mode='markers',
    text=hover_text,
    hoverinfo='text',
    marker={'size': szobak,
            'color': hol,
            'opacity': 0.6,
            'colorscale': 'Viridis'
            }
)
layout = go.Layout(
    title='XIII.ker tegla lakasok, 50M alatt'
)
fig = go.Figure(data=[data], layout=layout)
py.plot(fig)