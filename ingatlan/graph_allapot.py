from sqlalchemy.sql import select
from models import db_connect, IngatlanDB, ArDB
from scipy import stats
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import re

# query database
engine = db_connect()
conn = engine.connect()
s = select([IngatlanDB.id, IngatlanDB.alapterulet, IngatlanDB.szobak_egesz, IngatlanDB.szobak_fel, IngatlanDB.cim, IngatlanDB.ingatlan_allapota, ArDB.ar])
s = s.where(IngatlanDB.id == ArDB.ingatlan_id)
s = s.where(IngatlanDB.ingatlan_tipus == u'lakás').where(IngatlanDB.cim.like("%Újlipótváros%")).where(IngatlanDB.epites_tipus == u'tégla')
s = s.where(ArDB.ar < 50000000).where(IngatlanDB.alapterulet < 100)
result = conn.execute(s).fetchall()

# data init
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

# prepare data
for row in result:
    terulet.append(row['alapterulet'])
    ar.append(row['ar'])
    alkerulet = re.search(r'(?:\()(.*)(?:\))', row['cim']).group()
    colors.append(category_mapping[row['ingatlan_allapota']])
    szobak.append(10+5*(row['szobak_egesz']+row['szobak_fel']*0.5))
    hover_text.append("{} - Terulet: {} - Allapot: {} - Ar: {}M Ft - id: {}".format(alkerulet, row['alapterulet'], row['ingatlan_allapota'], row['ar']/1000000, row['id'])) 

# calculate regression
slope, intercept, r_value, p_value, std_err = stats.linregress(terulet,ar)
line = slope * np.asarray(terulet) + intercept

# make graph
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
regression = go.Scatter(
    x=terulet,
    y=line,
    mode='lines',
    line={'color':'blue', 'width':3}
)
layout = go.Layout(
    title='XIII.ker Ujlipotvaros tegla lakasok, 50M alatt',
    hovermode='closest',
    showlegend=False
)
fig = go.Figure(data=[data, regression], layout=layout)
py.plot(fig)