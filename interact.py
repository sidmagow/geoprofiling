import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans as km

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='Joe')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply

	data = request.get_json()
	# print(data)
	result = ''
	dataframe=pd.read_csv("TrainingData1.csv")
	loaded_model = pickle.load(open('model1.sav','rb'))
	prediction=loaded_model.predict(dataframe)

	center_count=[]
	for i in range(18):
		center_count.append(list(prediction).count(i))


	#print(centers)
	max_value=max(center_count)
	min_value=min(center_count)
	avg_value=(max_value+min_value)/3
	range1=int(min_value+avg_value)
	range2=int(max_value-avg_value)


	lat_list=[]
	lon_list=[]
	for item in data:
		# loop over every row
		# lst=[{'Latitude':float(item['lat']), 'Longitude':float(item['lon'])}]
		lat_list.append(float(item['lat']))
		lon_list.append(float(item['lon']))

	df = pd.DataFrame({'Latitude':lat_list, 'Longitude':lon_list})

	#print(df)
	point= loaded_model.predict(df)

	# result="hello"
	for i in point:
		if center_count[point[i]] in range(min_value,range1):
			result+='green'
		elif center_count[point[i]] in range(range2,max_value+1):
			result+='red'
		else:
			result+='yellow'

	return result


if __name__ == "__main__":
  	app.run('127.0.0.1','5011',True)
