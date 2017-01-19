import knn
import pygame
import sys
import time

trainingSet = knn.load("../data/optdigitsTrain.csv")
testSet = knn.load("../data/optdigitsTest.csv")
avg = knn.load("../data/averages.csv")


def runKNNTest():
    correct = 0.
    percentage = 0
    for i in range(len(testSet)):
        if i * 100 / len(testSet) > percentage:
            percentage = i * 100 / len(testSet)
            print '{0}\r'.format("Progress: " + str(percentage) + "%"),
        prediction = knn.predictLabel(trainingSet, testSet[i][:-1], 1)
        correct += prediction == testSet[i][-1]
    print str(correct * 100 / len(testSet)) + "% correct"


def convertImageToData(n):
    results = []
    for x in range(8):
        for y in range(8):
            results.append(0)
            for i in range(4):
                results[-1] += n[y * 4 + i][x * 4:x * 4 + 4].count(1)
    return results

    def calculateAverages():
        n = [[0 for j in range(64)]for i in range(10)]
        total = [0 for i in range(10)]
        for i in trainingSet + testSet:
            for j in range(64):
                n[i[-1]][j] += i[j]
            total[i[-1]] += 1
        for i in range(10):
            n[i] = [int(round(float(n[i][a]) / total[i])) for a in range(64)] + [i]
        return n

    def vectorToBitmap(n):
        pass


def main():
    pygame.init()
    white = 255, 255, 255
    black = 0, 0, 0
    red = 255, 0, 0
    green = 0, 255, 0
    board = [[0 for i in range(32)] for j in range(32)]
    heatmap = convertImageToData(board)
    averageHeatmap = convertImageToData(board)
    closestHeatmap = convertImageToData(board)
    screenSize = 10
    screen = pygame.display.set_mode((screenSize * 96, screenSize * 64))
    currentTime = 0.
    accumulator = 0.
    fps = .5
    strokes = [[]]
    adjustedStrokes = [[]]
    pixelated = pygame.Surface((32 * screenSize, 32 * screenSize))
    penDown = False
    prediction = 0
    minY = maxY = minX = maxX = 0

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if not penDown:
                        strokes.append([])
                        penDown = True
                    p = pygame.mouse.get_pos()
                    strokes[-1].append((max(min(p[0], screenSize * 32), 0), max(min(p[1], screenSize * 32), 0)))
                    minY = min([min(i, key=lambda n:n[1]) for i in strokes if len(i) > 0], key=lambda n: n[1])[1]
                    maxY = max([max(i, key=lambda n:n[1]) for i in strokes if len(i) > 0], key=lambda n: n[1])[1]
                    minX = min([min(i, key=lambda n:n[0]) for i in strokes if len(i) > 0], key=lambda n: n[0])[0]
                    maxX = max([max(i, key=lambda n:n[0]) for i in strokes if len(i) > 0], key=lambda n: n[0])[0]
                    totalSize = (maxX - minX + 1, maxY - minY + 1)
                    center = ((minX + maxX) / 2, (minY + maxY) / 2)
                    origin = (minX, minY)
                    zoom = max(totalSize)
                    adjustedStrokes = [[((i[0] - center[0]) * 32 * screenSize / zoom + 16 * screenSize, (i[1] - center[1]) * 32 * screenSize / zoom + 16 * screenSize) for i in j] for j in strokes]
                else:
                    penDown = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print knn.predictLabel(trainingSet + testSet, heatmap, 1)
                    minY = maxY = minX = maxX = 0
                    strokes = [[]]
                    adjustedStrokes = [[]]
                    board = [[0 for i in range(32)] for j in range(32)]
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    # record correct key and save to current set
                    print "test"

        accumulator += time.clock() - currentTime
        currentTime = time.clock()
        while accumulator > fps:
            accumulator -= fps
            board = [[0 for i in range(32)] for j in range(32)]
            for i in range(32):
                for j in range(32):
                    if 1 in [pixelated.get_at((screenSize * j + n, screenSize * i + m)) != white for n in range(screenSize) for m in range(screenSize)]:
                        for y in range(-1, 2):
                            for x in range(-1, 2):
                                if x == 0 or y == 0:
                                    board[max(min(j + x, 31), 0)][max(min(i + y, 31), 0)] = 1
            heatmap = convertImageToData(board)
            if not pygame.mouse.get_pressed()[0]:
                prediction = knn.getNeighborData(trainingSet + testSet, heatmap)
                closestHeatmap = prediction
                averageHeatmap = avg[prediction[-1]]

        screen.fill((100, 100, 100))

        # vectorized
        pygame.draw.rect(screen, white, (0, 0, screenSize * 96, screenSize * 64))
        if maxX != 0 or maxY != 0:
            pygame.draw.line(screen, green, (minX, minY), (minX, maxY))
            pygame.draw.line(screen, green, (maxX, minY), (maxX, maxY))
            pygame.draw.line(screen, green, (minX, maxY), (maxX, maxY))
            pygame.draw.line(screen, green, (minX, minY), (maxX, minY))
        for i in strokes:
            for j in i:
                screen.set_at(j, red)

        # vectorized, normalized, and scaled
        pygame.draw.rect(pixelated, white, (0, 0, screenSize * 32, screenSize * 32))
        for i in adjustedStrokes:
            if len(i) > 1:
                pygame.draw.aalines(pixelated, black, 0, i, 1)
        screen.blit(pixelated, (32 * screenSize, 0))

        # 32x32 pixelated
        for j in range(32):
            for i in range(32):
                pygame.draw.rect(screen, black if board[i][j] else white, (64 * screenSize + i * screenSize, j * screenSize, screenSize, screenSize))

        # 8x8 gradient
        for i in range(64):
            c = 255 - heatmap[i] * (255 / 16)
            pygame.draw.rect(screen, (c, c, c), ((i % 8) * screenSize * 4, 32 * screenSize + (i / 8) * screenSize * 4, screenSize * 4, screenSize * 4))

        # closest 8x8
        for i in range(64):
            c = 255 - closestHeatmap[i] * (255 / 16)
            pygame.draw.rect(screen, (c, c, c), (32 * screenSize + (i % 8) * screenSize * 4, 32 * screenSize + (i / 8) * screenSize * 4, screenSize * 4, screenSize * 4))

        # average 8x8
        for i in range(64):
            c = 255 - averageHeatmap[i] * (255 / 16)
            pygame.draw.rect(screen, (c, c, c), (32 * screenSize + (i % 8) * screenSize * 4, 64 * screenSize + (i / 8) * screenSize * 4, screenSize * 4, screenSize * 4))

        # finalCharacter font draw/print

        pygame.draw.line(screen, red, (32 * screenSize, 0), (32 * screenSize, 64 * screenSize))
        pygame.draw.line(screen, red, (64 * screenSize, 0), (64 * screenSize, 64 * screenSize))
        pygame.draw.line(screen, red, (0, 32 * screenSize), (96 * screenSize, 32 * screenSize))

        pygame.display.flip()

# runKNNTest()
main()

# vector input or image      raw input scaled      32x32
# 8x8                        closest               average or example raw

# pull in the vector dataset from UCI once it can translate

# local set builds over time with option to correct wrong answers
# press digit to correct or verify it and add current to database
