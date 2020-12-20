from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import plot

client = MongoClient('mongodb://54.254.190.113:27017/')

app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/city/<city>')
def map_selected(city):
    data = getPM25ByCity(city)
    if not data:
        return render_template('showMessage.html')
    plot.toBarplot(data,city)
    plot.toHeatplot(data,city)
    return render_template('map_selected.html', city=city)


@app.route('/api/<city>/<year>/<month>', methods=['GET', 'POST'])
def pm25OneMonth(city, year, month):
    return jsonify(getPM25ByCityEachMount(city,year,mounth))


@app.route('/api/<city>/<year>', methods=['GET', 'POST'])
def pm25Year(city, year):
    return jsonify(getPM25ByCityEachYear(city,year))


@app.route('/api/<city>', methods=['GET', 'POST'])
def pm25City(city):
    return jsonify(getPM25ByCity(city))

def getPM25ByCity(city):
    data = []
    for x in client['cs457'][city].find({'date': {"$regex": "/*"}}):
        data.append({'date': x['date'], 'pm25': x[' pm25']})
    return data


def getPM25ByCityEachYear(city,year):
    data = []
    for x in client['cs457'][city].find({'date': {"$regex": year+"/*"}}):
        data.append({'date': x['date'], 'pm25': x[' pm25']})
    return data


def getPM25ByCityEachMonth(city,year,mounth):
    data = []
    for x in client['cs457'][city].find({'date': {"$regex": year+"/"+month+"/*"}}):
        data.append({'date': x['date'], 'pm25': x[' pm25']})
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
