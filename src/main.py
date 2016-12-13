from knn import load, predictLabel
import pygame
import sys

trainingSet = load("../data/optdigitsTrain.txt")

testSet = load("../data/optdigitsTest.txt")
def runKNNTest():
    correct = 0.
    percentage = 0
    for i in range(len(testSet)):
        if i*100/len(testSet)>percentage:
            percentage=i*100/len(testSet)
            print '{0}\r'.format("Progress: " + str(percentage)+"%"),
        prediction=predictLabel(trainingSet,testSet[i][:-1],1)
        correct+=prediction==testSet[i][-1]

    print str(correct*100/len(testSet)) + "% correct"

def convertImageToData(n):
    results = []
    for x in range(8):
        for y in range(8):
            results.append(0)
            for i in range(4):
                results[-1]+=n[y*4+i][x*4:x*4+4].count(1)
    return results

def main():
    white = 255,255,255
    black = 0,0,0
    pygame.init()
    board = [[0 for i in range(32)] for j in range(32)]
    screenSize = 10
    screen = pygame.display.set_mode((screenSize*32*2,screenSize*32))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print predictLabel(trainingSet,heatmap,1)                       
                    board = [[0 for i in range(32)] for j in range(32)]
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

        heatmap=convertImageToData(board)
        #heatmap=[0,0,1,10,16,7,0,0,0,1,14,14,12,16,4,0,0,6,16,2,1,16,4,0,0,6,16,11,13,16,2,0,0,0,11,12,16,11,0,0,0,0,0,3,16,5,0,0,0,0,0,11,14,0,0,0,0,0,0,13,11,0,0,0]

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()[0]/screenSize, pygame.mouse.get_pos()[1]/screenSize
            #board[pos[0]][pos[1]]=1
            for j in range(-1,2):
                for i in range(-1,2):
                    if i==0 or j==0:
                        board[max(min(pos[0]+i, 31),0)][max(min(pos[1]+j, 31),0)]=1

        screen.fill((100, 100, 100))
        for j in range(32):
            for i in range(32):
                pygame.draw.rect(screen,black if board[i][j] else white,(i*screenSize,j*screenSize,screenSize,screenSize))

        for i in range(64):
            c = 255-heatmap[i]*(255/16)
            pygame.draw.rect(screen,(c,c,c),(31*screenSize+screenSize+(i%8)*screenSize*4,(i/8)*screenSize*4,screenSize*4,screenSize*4))
        pygame.draw.line(screen,black,(32*screenSize,0),(32*screenSize,32*screenSize))

        pygame.display.flip()


#runKNNTest()
main()