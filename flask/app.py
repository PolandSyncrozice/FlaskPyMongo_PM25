from flask import Flask, render_template, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://54.254.190.113:27017/')

app = Flask(__name__,static_url_path='', static_folder='static',template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def map_selected(name):
    return render_template('map_selected.html',name=name)

@app.route('/api/<city>/<year>/<month>',methods=['GET', 'POST'])
def pm25(city,year,month):
    a = []
    for x in client.cs457.Bangkok.find({'date':{ "$regex": year+"/"+month+"/*" } }):
        a.append({'date':x['date'],'pm25':x[' pm25']})
    # gen_pic(a)
    return jsonify(a)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
