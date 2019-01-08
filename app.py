from flask import Flask
from flask import render_template


app = Flask(__name__, template_folder='templates', static_folder='static')
print(app.url_map)


@app.route('/')
def index():
    return render_template('index.html')
