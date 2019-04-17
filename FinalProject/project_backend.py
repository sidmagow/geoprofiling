#!flask/bin/python

import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans as km
import gmplot as gm
import geocoder
import webbrowser

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

	time=data[len(data)-1]['lat']
	print(time)
	del data[len(data)-1]

	cluster_crimes=[]

	result=[]

	# dataframe=pd.read_csv("TrainingData.csv")
	# crimedataframe=pd.read_csv("CrimeTrainingData.csv")

	if time>=600 and time<=2000:
		dataframe=pd.read_csv("Day.csv")
		loaded_model = pickle.load(open('modelday.sav', 'rb'))
		crimedataframe=pd.read_csv("DayCrime.csv")
	else:
		dataframe=pd.read_csv("Night.csv")
		loaded_model = pickle.load(open('modelnight.sav', 'rb'))
		crimedataframe=pd.read_csv("NightCrime.csv")

	#loaded_model = pickle.load(open('model1.sav', 'rb'))
	prediction=loaded_model.predict(dataframe)
	g = geocoder.bing("Delhi, India", key='Av3MzjFGfdPT198iOOm1o5cUm9SohZKyKX_4ioh0IPW8xj4Uut_HOFxz2hbOAKyV')
	gmap1 = gm.GoogleMapPlotter(g.lat, g.lng, 12)

	df3=crimedataframe.copy()
	df3['cluster'] = loaded_model.labels_

	for i in range(18):
	    ind=df3[df3.cluster == i].index
	    c_murder=0
	    c_kidnap=0
	    c_sexual=0
	    c_robbery=0
	    c_drugs=0
	    for j in ind:
	        if crimedataframe['Crime'][j] == 'Murder':
	            c_murder=c_murder+1
	        elif crimedataframe['Crime'][j] == 'Robbery':
	            c_robbery=c_robbery+1
	        elif crimedataframe['Crime'][j] == 'Kidnapping':
	            c_kidnap=c_kidnap+1
	        elif crimedataframe['Crime'][j] == 'Sexual Offense':
	            c_sexual=c_sexual+1
	        else:
	            c_drugs=c_drugs+1
	    l1=[c_murder, c_robbery, c_kidnap, c_sexual, c_drugs]
	    l2=['Murder', 'Robbery', 'Kidnapping', 'Sexual Offense', 'Drugs']
	    cluster_crimes.append(l2[l1.index(max(l1))])

	print(cluster_crimes)

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
			color_green_lat.append(lat)
			color_green_lon.append(lng)
			color_predict['color']='green'
			color_predict['crime']=cluster_crimes[point[0]]
			result.append(color_predict)
		elif center_count[point[0]] in range(range2, max_value+1):
			color_red_lat.append(lat)
			color_red_lon.append(lng)
			color_predict['color']='red'
			color_predict['crime']=cluster_crimes[point[0]]
			result.append(color_predict)
		else:
			color_yellow_lat.append(lat)
			color_yellow_lon.append(lng)
			color_predict['color']='yellow'
			color_predict['crime']=cluster_crimes[point[0]]
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
	chrome_path="C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
	webbrowser.get(chrome_path).open_new_tab("pointsonrouteoutput"+str(mapno-1)+".html")
	return json.dumps(result)

if __name__ == '__main__':
	# run!
	app.run()