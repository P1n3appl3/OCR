from collections import Counter

def load(fileName):
	f=open(fileName)
	lines = [[int(i) for i in l.rstrip('\n').replace(" ", "").split(",")] for l in f]
	f.close()
	return lines

def euclideanDistance(a, b):
	return sum([(a[i]-b[i])**2 for i in range(len(a))])**.5

def getNeighbors(dataSet, instance, k):
	return sorted([(euclideanDistance(instance,i),i[-1]) for i in dataSet])[:k]
	 
def predictLabel(dataSet, instance, k):
	return Counter([i[-1] for i in getNeighbors(dataSet,instance,k)]).most_common()[0][0]

#def everything(dataSet, instance, k):
	#return Counter([i[-1] for i in sorted([(sum([(instance[n]-j[n])**2 for n in range(len(instance))])**.5,j[-1]) for j in dataSet])[:k].most_common()[0][0]
