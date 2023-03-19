import flask

app = flask.Flask(__name__)


@app.route('/test', methods=['GET'])
def Hello_World():
    return "Hello World"


app.run(port=5000, host='0.0.0.0')
