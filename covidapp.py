from flask import Flask, request, jsonify, render_template, flash
from cassandra.cluster import Cluster
import json
import requests
from random import randint
from datetime import datetime
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

cluster=Cluster(contact_points=['172.17.0.2'],port=9042)
session=cluster.connect()

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

class ReusableForm(Form):
    country = TextField('Country:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def startapp():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        country=request.form['country']
        covidurl = f'https://api.covid19api.com/live/country/{country}'
        resp = requests.get(covidurl)
        if resp.ok:
            response = resp.json()
            num=len(response)
            country = response[num-1]['Country']
            newconfirmed = response[num-1]['Confirmed']
            newdeaths = response[num-1]['Deaths']
            newrecovered = response[num-1]['Recovered']
            flash(f'Country: {country}\n NewConfirmed: {newconfirmed}\n NewDeaths: {newdeaths} \nNewRecovered: {newrecovered}')
            session.execute(f"INSERT INTO covid.stats(country,newconfirmed,newdeaths,newrecovered) VALUES('{country}',{newconfirmed},{newdeaths},{newrecovered});")
                
         else:
            print(resp.reason)    
    return render_template('index.html', form=form)
@app.route('/covid', methods=['GET'])
def profile():
        rows = session.execute( """SELECT * FROM covid.stats""")
        result = []
        for r in rows:
                result.append({"country":r.country, "newconfirmed":r.newconfirmed, "newdeaths":r.newdeaths, "newrecovered":r.newrecovered})
        return jsonify(result), 200
@app.route('/covid/external',methods=['GET'])
def external():
        covid19_url ='https://api.covid19api.com/summary'
        resp = requests.get(covid19_url)
        if resp.ok:
             covid19 = resp.json()
             return jsonify(resp.json())
        else:
             print(resp.reason)
@app.route('/covid', methods=['POST'])
def create():
        session.execute( """INSERT INTO covid.stats(country,newconfirmed,newdeaths,newrecovered) VALUES('{}',{},{},{})""".format(request.json['country'],int(request.json['newconfirmed']),int(request.json['newdeaths']),int(request.json['newrecovered'])))

        return jsonify({'message': 'created: /covid/{}'.format(request.json['country'])}), 201
@app.route('/covid', methods=['PUT'])
def update():
        session.execute("""UPDATE covid.stats SET newconfirmed= {}, newdeaths= {}, newrecovered= {} WHERE country= '{}'""".format(int(request.json['newconfirmed']),int(request.json['newdeaths']),int(request.json['newrecovered']),request.json['country']))
        return jsonify({'message': 'updated: /covid/{}'.format(request.json['country'])}), 200
@app.route('/covid', methods=['DELETE'])
def delete():
        session.execute("""DELETE FROM covid.stats WHERE country= '{}'""".format(request.json['country']))
        return jsonify({'message': 'deleted: /country/{}'.format(request.json['country'])}), 200

if __name__=='__main__':
#        app.run(host='0.0.0.0')
        app.run(host='0.0.0.0',port=443,ssl_context=('cert.pem', 'key.pem'))

