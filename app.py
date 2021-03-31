from flask import Flask, make_response, render_template, request, jsonify
from flask_cors import CORS
import sqlite3, pandas as pd
sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))

app = Flask(__name__, static_folder='static')
cors = CORS(app)
################################
@app.route('/menciones', methods=['GET','POST'])
def hello_world():
    #men = pd.read_csv('keywords.txt', names=['Tema'])
    #men['Tema']=men.Tema.apply(lambda t: t.split('\t')[1])
    men = sql('SELECT * FROM menciones')
    return render_template('menciones.html', data=men.to_html(index=False))

if __name__ == '__main__':
    app.run(port=8081, debug=True, host='0.0.0.0')
    print(app.static_folder)
