from flask import Flask, make_response, render_template, request, jsonify
from flask_cors import CORS
import glob, sqlite3, pandas as pd

from searcher import querier, cubicalo, get_candy
from publish_candidatos import pc

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))

app = Flask(__name__, static_folder='static')
cors = CORS(app)
################################
@app.route('/ver_menciones/<query>/<ancho>', methods=['GET','POST'])
def verlas(query, ancho):

    ANCHO = int(ancho)
    data, nMatches = querier(query, ANCHO)

    return render_template('ver_menciones.html', data=data, 
                            nMatches=nMatches, 
                            mencion=query)

@app.route('/ver_menciones_ori/<query>/<ancho>', methods=['GET','POST'])
def verlas_ori(query, ancho):

    ANCHO = int(ancho)
    data, nMatches = querier(query, ANCHO, tipo='ori')   # fix: merged

    return render_template('ver_menciones.html', data=data, 
                            nMatches = nMatches, mencion=query)

@app.route('/cubo_menciones/<tipo>', methods=['GET','POST'])
def cubitos(tipo):
    data = cubicalo(tipo)

    return render_template('cubo_menciones.html', data=data)

@app.route('/')
def hello():
    return render_template('entering.html')

    return render_template('equipo.html')

@app.route('/candidatos')
def candidatos():
    #cdata = get_candy()
    cdata = pc()
    return render_template('candidatos.html', cdata=cdata)

@app.route('/distritos')
def distritos():
    plots = sorted(glob.glob('static/heatmap_listas_DD*.png'))
    print('PLOTS:', plots)
    return render_template('distritos.html', plots=plots)

@app.route('/listas')
def listas():
    plots = sorted(glob.glob('static/heatmap_lista_*.png'))
    print('PLOTS:', plots)
    return render_template('listas.html', plots=plots)

@app.route('/menciones', methods=['GET','POST'])
def menciones():
    #men = pd.read_csv('keywords.txt', names=['Tema'])
    #men['Tema']=men.Tema.apply(lambda t: t.split('\t')[1])
    men = sql('SELECT * FROM menciones_todos ORDER BY nMenciones DESC')
    #menO = sql('SELECT * FROM menciones_ori ORDER BY nMenciones DESC')
    menO = sql('SELECT * FROM menciones_originarios ORDER BY nMenciones DESC')
    #wot
    #men['Tema'] = men.Tema.apply(lambda t: 'clima' if 'clim' in t else 'medioambiente' if 'medio' in t else t)
    men = men.groupby('concepto').sum().reset_index()
    menO = menO.groupby('concepto').sum().reset_index()
    men['PorcMencionan'] = men.PorcMencionan.apply(lambda x: round(x,1))
    menO['PorcMencionan'] = menO.PorcMencionan.apply(lambda x: round(x,1))
    #URL = 'http://greenpeace.quant.cl:8081/ver_menciones/%s/50' 
    URL = 'http://greenpeace-monitor.herokuapp.com/ver_menciones/%s/50' 
    URLO = 'http://greenpeace-monitor.herokuapp.com/ver_menciones_ori/%s/50' 
    men['link'] = ['<A HREF="%s">click</A>' %(URL %tema) 
                    for tema in men['concepto']]
    menO['link'] = ['<A HREF="%s">click</A>' %(URLO %tema) 
                    for tema in men['concepto']]

    data = men.to_html(index=False, escape=False, classes='mystyle')
    dataO = menO.to_html(index=False, escape=False, classes='mystyle')

    return render_template('menciones_all.html', data=data,dataO=dataO)

if __name__ == '__main__':
    app.run(port=8081, debug=True, host='0.0.0.0')
    print(app.static_folder)
