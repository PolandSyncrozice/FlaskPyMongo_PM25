from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import plot

client = MongoClient('mongodb://54.254.190.113:27017/')

app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/city/<name>')
def map_selected(name):
    return render_template('map_selected.html', name=name)


@app.route('/api/<city>/<year>/<month>', methods=['GET', 'POST'])
def pm25OneMonth(city, year, month):
    a = []
    for x in client['cs457'][city].find({'date': {"$regex": year+"/"+month+"/*"}}):
        a.append({'date': x['date'], 'pm25': x[' pm25']})
    return jsonify(a)


@app.route('/api/<city>/<year>', methods=['GET', 'POST'])
def pm25Year(city, year):
    a = []
    for x in client['cs457'][city].find({'date': {"$regex": year+"/*"}}):
        a.append({'date': x['date'], 'pm25': x[' pm25']})
    return jsonify(a)


@app.route('/api/<city>', methods=['GET', 'POST'])
def pm25City(city):
    a = []
    for x in client['cs457'][city].find({'date': {"$regex": "/*"}}):
        a.append({'date': x['date'], 'pm25': x[' pm25']})
    plot.toBarplot(a,city)
    plot.toHeatplot(a,city)
    return jsonify(a)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
