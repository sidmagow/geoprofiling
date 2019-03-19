#!flask/bin/python

import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans as km
import gmplot as gm
import geocoder

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

mapno=0

@app.route('/')
def output():
	# serve index template
	return render_template('IntegratedProject.html', name='Joe')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json()
	
	print(data)

	result=[]

	dataframe=pd.read_csv("TrainingData.csv")

	loaded_model = pickle.load(open('model.sav', 'rb'))
	prediction=loaded_model.predict(dataframe)
	g = geocoder.bing("Delhi, India", key='Av3MzjFGfdPT198iOOm1o5cUm9SohZKyKX_4ioh0IPW8xj4Uut_HOFxz2hbOAKyV')
	gmap1 = gm.GoogleMapPlotter(g.lat, g.lng, 12)

	color_red_lat=[]
	color_red_lon=[]
	color_yellow_lat=[]
	color_yellow_lon=[]
	color_green_lat=[]
	color_green_lon=[]

	for item in data:
		lat=float(item['lat'])
		lng=float(item['lon'])
		color_predict={}

		#Have to remove loop

		center_count=[]

		for i in range(18):
			center_count.append(list(prediction).count(i))

		max_value=max(center_count)
		min_value=min(center_count)
		avg_value=(max_value+min_value)/3
		range1=int(min_value+avg_value)
		range2=int(max_value-avg_value)

		'''df=pd.DataFrame({'Latitude':list(lat)})
		df=pd.DataFrame({'Longitude':list(lng)})'''
		lst=[{'Latitude':lat, 'Longitude':lng}]
		df=pd.DataFrame(lst)

		point=loaded_model.predict(df)


		if center_count[point[0]] in range(min_value, range1):
			# gmap1.scatter(list(lat), list(lng), 'green', size = 50, marker = False)
			color_green_lat.append(lat)
			color_green_lon.append(lng)
			color_predict['color']='green'
			result.append(color_predict)
		elif center_count[point[0]] in range(range2, max_value+1):
			# gmap1.scatter(list(lat), list(lng), 'red', size = 50, marker = False)
			color_red_lat.append(lat)
			color_red_lon.append(lng)
			color_predict['color']='red'
			result.append(color_predict)
		else:
			# gmap1.scatter(list(lat), list(lng), 'yellow', size = 50, marker = False)
			color_yellow_lat.append(lat)
			color_yellow_lon.append(lng)
			color_predict['color']='yellow'
			result.append(color_predict)

	print(result)
	if len(color_green_lat) > 0:
		gmap1.scatter(color_green_lat, color_green_lon, 'green', size=70, marker=False)
	if len(color_red_lat) > 0:
		gmap1.scatter(color_red_lat, color_red_lon, 'red', size=70, marker=False)
	if len(color_yellow_lat) > 0:
		gmap1.scatter(color_yellow_lat, color_yellow_lon, 'yellow', size=70, marker=False)
	global mapno
	gmap1.draw("pointsonrouteoutput"+str(mapno)+".html")
	mapno=mapno+1
	return json.dumps(result)

if __name__ == '__main__':
	# run!
	app.run()