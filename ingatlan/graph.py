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

engine = db_connect()
conn = engine.connect()

s = select([IngatlanDB.id, IngatlanDB.alapterulet, IngatlanDB.epites_tipus, IngatlanDB.szobak_egesz, IngatlanDB.szobak_fel, ArDB.ar]).where(IngatlanDB.id == ArDB.ingatlan_id).where(IngatlanDB.ingatlan_tipus == u'lakás')
result = conn.execute(s).fetchall()
terulet = []
ar = []
epites = []
szobak = []
hover_text = []
epites_mapping = {
    u'tégla': 0,
    u'csúszózsalus': 0.5,
    u'panel': 1,
}
for row in result:
    terulet.append(row['alapterulet'])
    ar.append(row['ar'])
    epites.append(epites_mapping[row['epites_tipus']])
    szobak.append(10+5*(row['szobak_egesz']+row['szobak_fel']*0.5))
    hover_text.append("Terulet: " + str(row['alapterulet']) + " - Tipus: " + row['epites_tipus'] + " - Ar: " + str(row['ar']/1000000) + "M Ft - id: " + str(row['id'])) 

fig = go.Figure()
fig.add_scatter(x=terulet,
                y=ar,
                mode='markers',
                text=hover_text,
                hoverinfo='text',
                marker={'size': szobak,
                        'color': epites,
                        'opacity': 0.6,
                        'colorscale': 'Viridis'
                       })
py.plot(fig)