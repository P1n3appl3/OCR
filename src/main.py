from knn import load, predictLabel

trainingSet = load("../data/optdigitsTrain.txt")

testSet = load("../data/optdigitsTest.txt")

correct = 0.
percentage = 0
for i in range(len(testSet)):
	if i*100/len(testSet)>percentage:
		percentage=i*100/len(testSet)
		print str(percentage)+"% complete"
	prediction=predictLabel(trainingSet,testSet[i][:-1],1)
	correct+=prediction==testSet[i][-1]

print str(correct*100/len(testSet)) + "% correct"