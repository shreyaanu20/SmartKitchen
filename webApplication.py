import requests
import json
from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
import requests
from time import time
from random import random
from flask import Flask, render_template, make_response
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    
    r=requests.get("https://node-red-kgycv-2020-08-26.eu-gb.mybluemix.net/data")
    dat=r.json()
    print(dat)
    jar=dat['jarPer']
    cylinder=dat['gasWeight']
    data = [time() * 1000, jar,cylinder]
   
    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

if __name__ == "__main__":
    app.run(debug=True)
