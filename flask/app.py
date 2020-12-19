from flask import Flask, render_template

app = Flask(__name__,static_url_path='', static_folder='static',template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def map_selected(name):
    return render_template('map_selected.html',name=name)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
