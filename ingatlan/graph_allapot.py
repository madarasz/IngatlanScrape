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

s = select([IngatlanDB.id, IngatlanDB.alapterulet, IngatlanDB.szobak_egesz, IngatlanDB.szobak_fel, IngatlanDB.cim, IngatlanDB.ingatlan_allapota, ArDB.ar])
s = s.where(IngatlanDB.id == ArDB.ingatlan_id)
s = s.where(IngatlanDB.ingatlan_tipus == u'lakás').where(IngatlanDB.cim.like("%Újlipótváros%")).where(IngatlanDB.epites_tipus == u'tégla')
s = s.where(ArDB.ar < 50000000).where(IngatlanDB.alapterulet < 100)
result = conn.execute(s).fetchall()
terulet = []
ar = []
szobak = []
hover_text = []
colors = []
category_mapping = {
    u'befejezetlen': 6,
    u'felújítandó': 5,
    u'közepes állapotú': 4,
    u'jó állapotú': 3,
    u'felújított': 2,
    u'újszerű': 1,
    u'új építésű': 0,
    None: 3
}

for row in result:
    terulet.append(row['alapterulet'])
    ar.append(row['ar'])
    alkerulet = re.search(r'(?:\()(.*)(?:\))', row['cim']).group()
    colors.append(category_mapping[row['ingatlan_allapota']])
    szobak.append(10+5*(row['szobak_egesz']+row['szobak_fel']*0.5))
    hover_text.append(alkerulet + " - Terulet: " + str(row['alapterulet']) + " - Allapot: " + str(row['ingatlan_allapota']) + " - Ar: " + str(row['ar']/1000000) + "M Ft - id: " + str(row['id'])) 

data = go.Scatter( 
    x=terulet,
    y=ar,
    mode='markers',
    text=hover_text,
    hoverinfo='text',
    marker={'size': szobak,
            'color': colors,
            'opacity': 0.6,
            'colorscale': 'Jet'
            }
)
layout = go.Layout(
    title='XIII.ker Ujlipotvaros tegla lakasok, 50M alatt'
)
fig = go.Figure(data=[data], layout=layout)
py.plot(fig)