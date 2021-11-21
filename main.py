from flask import Flask,render_template
from map import create

##creating a flask app and naming it "app"
app = Flask(__name__)

@app.route('/')
def home():
    create()
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    return 'Pinging Model Application!'

if __name__ == '__main__':
    app.run(debug=True)