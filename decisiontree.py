import random

import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

decision = {'Defuse': 0, 'Move away': 1}
variables = ['Percent of mines', 'Time to explosion', 'Range of explosion']

class DecisionTree:
	def __init__(self):
		self.data = pandas.read_csv("decisiontree.csv", sep=';')
		#print(self.data)
		self.data['What to do'] = self.data['What to do'].map(decision)
		self.treevariables = self.data[variables]
		self.treeresault = self.data['What to do']
		self.decisiontree = DecisionTreeClassifier(random_state=0)
		self.decisiontree = self.decisiontree.fit(self.treevariables.values, self.treeresault.values)

	def make_decision(self, minespercent, exptime, exprange):
		wtd = self.decisiontree.predict([[minespercent, exptime, exprange]])
		#print("zmienne:", minespercent, exptime, exprange)
		#print("wdt:", wtd)
		if wtd == [0]:
			return "Defuse"
		if wtd == [1]:
			return "Move away"


