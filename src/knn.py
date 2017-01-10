from collections import Counter

def load(fileName):
	f=open(fileName)
	lines = [[int(i) for i in l.rstrip('\n').replace(" ", "").split(",")] for l in f]
	f.close()
	return lines

def euclideanDistance(a, b):
	return sum([(a[i]-b[i])**2 for i in range(len(a))])**.5

def getNeighborData(dataSet, instance):
	return sorted([(euclideanDistance(instance,i),i) for i in dataSet])[0][-1]

def getNeighbors(dataSet, instance, k):
	return sorted([(euclideanDistance(instance,i),i[-1]) for i in dataSet])[:k]

def predictLabel(dataSet, instance, k):
	return Counter([i[-1] for i in getNeighbors(dataSet,instance,k)]).most_common()[0][0]
