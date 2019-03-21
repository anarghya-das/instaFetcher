
from flask import Flask, render_template, send_file, request
import private

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetch", methods=['POST'])
def get_data():
    data = request.get_json()
    print(data)
    return private.downloadWithLink(data['link'])


@app.route("/download/<file>")
def send(file):
    return send_file("all/"+file)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
