import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.externals import joblib
from sklearn import model_selection

"""
Model
"""

def model_train():
	data = pd.read_csv('occurrences.csv')
	data=data.drop('date',axis=1)
	train_pr = ['barcelona','madrid','real','barça']
	prdata = data[train_pr]
	target = data.match

	predictor= LinearRegression(n_jobs=-1)
	predictor.fit(prdata,target)

	X_TEST=[[[20,10,5,4]],[[10,5,4,2]],[[5,3,2,1]],[[0,0,0,0]],[[100,100,100,100]]]

	print("Test Values= barcelona, madrid, real, barça")
	for element in X_TEST:
		outcome= predictor.predict(X=element)
		coefficients=predictor.coef_
		print("Test Values: {0}, Outcome: {1}, Coefficient: {2}".format(element,outcome, coefficients))

if __name__ == "__main__":
	model_train()