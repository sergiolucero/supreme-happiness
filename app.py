from flask import Flask, make_response, render_template, request, jsonify
from flask_cors import CORS
import glob, sqlite3, pandas as pd

from searcher import querier, cubicalo

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))

app = Flask(__name__, static_folder='static')
cors = CORS(app)
################################
@app.route('/ver_menciones/<query>/<ancho>', methods=['GET','POST'])
def verlas(query):

    ANCHO = int(ancho)
    data = querier(query)   # fix: merged

    return render_template('ver_menciones.html', data=data, mencion=query, ancho=ANCHO)

@app.route('/cubo_menciones/<tipo>', methods=['GET','POST'])
def cubitos(tipo):
    data = cubicalo(tipo)

    return render_template('cubo_menciones.html', data=data)

@app.route('/')
def hello():

    return render_template('entering.html')

@app.route('/listas')
def listas():
    plots = glob.glob('static/images/lista*.png')
    print('PLOTS:', plots)
    return render_template('listas.html', plots=plots)

@app.route('/menciones', methods=['GET','POST'])
def hello_world():
    #men = pd.read_csv('keywords.txt', names=['Tema'])
    #men['Tema']=men.Tema.apply(lambda t: t.split('\t')[1])
    men = sql('SELECT * FROM menciones ORDER BY nMenciones DESC')
    men['link'] = ['<A HREF="%s">click</A>' %link for link in men['link']]

    data = men.to_html(index=False, escape=False, classes='mystyle')

    return render_template('menciones.html', data=data)

if __name__ == '__main__':
    app.run(port=8081, debug=True, host='0.0.0.0')
    print(app.static_folder)
