import numpy as np
import cv2
import glob

#cv2.namedWindow("Matched", cv2.WINDOW_NORMAL)

'''Since this is cropped, its easy to split it into 25 parts.
Planning to connect them to neighbors with matching terrain, then checking to see how many, if any, has a crown.
I could do the opposite, but then i'd have to remember which one has already been checked bleh. I guess I have to do it anyway but the above feels easier.'''
boards = [cv2.imread(i) for i in sorted(glob.glob("data/cropped/*.jpg"), key=len)]
num = 1

p = cv2.SimpleBlobDetector_Params()
p.filterByCircularity = True
p.minArea = 125
p.maxArea = 400
p.minCircularity = 0.1
p.maxCircularity = 0.8
p.minConvexity = 0.1
blob = cv2.SimpleBlobDetector_create(p)

#Need to do histogram stuff so its easier to compare differences regardless of lighting!
#Detect mines by detecting amount of "black" and "yellow" so it doesnt mistake with forest?

mine = grass = forest = sand = desert = water = table = na = cForest = cWater = cSand = cMine = [].append([])
count = 0
diff = []

m_low = np.array([0, 0, 0])
m_high = np.array([35, 255, 30])

#Missing one grass thats 62, really need to do histogram sigh

m_low = np.array([0, 0, 0])
m_high = np.array([35, 255, 30])

#Missing one grass thats 62, really need to do histogram sigh
g_low = np.array([35, 160, 100])
g_high = np.array([55, 255, 255])

f_low = np.array([35, 50, 10])
f_high = np.array([80, 255, 109])

s_low = np.array([20, 220, 160])
s_high = np.array([30, 255, 225])

d_low = np.array([15, 10, 50])
d_high = np.array([30, 255, 155])

w_low = np.array([100, 230, 100])
w_high = np.array([110, 255, 215])

t_low = np.array([15, 115, 120])
t_high = np.array([21, 230, 185])

'''#Mine:   10-40 / 0-10 AND 245-255 / 0-30
#Grass:  35-50 / 210-255 / 130-160
#Forest: 35-60 / 50-255 / 20-70
#Sand:   20-30 / 240-255 / 170-200
#Desert: 20-40 / 40-255 / 100-150
#Water:  100-110 / 230-255 / 150-190'''

'''#Mine:   0-15 / 10-20 / 10-20
#Grass:  15-30 / 140-170 / 85-140
#Forest: 0-35 / 15-65 / 10-55
#Sand:   0-10 / 150-175 / 170-200
#Desert: 0-100 / 95-125 / 110-140
#Water:  170-185 / 80-95 / 0-15'''

def checkNeighborsDB(colors, x, y): #debug
    if colors is None:
        return
    curCol = colors[y][x]
    left = up = [0, 0, 0]
    if x > 0:
        nextCol = colors[y][x-1]
        left = abs(np.subtract(curCol, nextCol))
        #left = np.sum(abs(np.subtract(curCol, nextCol)))

    if y > 0:
        nextCol = colors[y-1][x]
        up = abs(np.subtract(curCol, nextCol))
        #up = np.sum(abs(np.subtract(curCol, nextCol)))
    return [left, up]

def checkNeighbors(self, other):
    return np.sum(abs(np.subtract(self, other)))

def kMeans(img, draw = None, colors = 1):
    if draw is None:
        draw = img
    px = np.float32(np.array(img).reshape(-1, 3))
    c = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, label, palette = cv2.kmeans(px, colors, None, c, 10, cv2.KMEANS_RANDOM_CENTERS)
    palette = [int(i) for i in palette[0]]
    cv2.rectangle(draw, (45 + x * 100, 45 + y * 100), (55 + x * 100, 55 + y * 100), palette, 50)
    draw = cv2.GaussianBlur(draw, (5, 5), 0)
    #cv2.circle(img, (50 + x * 100, 50 + y * 100), 1, palette, 75)
    return label, palette

def mask(img, low, high, lim):
    mask = cv2.inRange(img, low, high)
    if np.sum(mask) > lim:
        return True

#[204, 99, 76] [192, 29, 95] [172, 12, 95]
masked = []

def blobDetect(img):
    return
    #cv2.floodFill(img, None, (50, 50), 255)
    #cv2.rectangle(img, (47, 47), (52, 52), (255, 255, 255), 40)
    #cv2.rectangle(img, (0, 0), (100, 100), (255, 255, 255), 1)

    '''bp = img
    blobs = blob.detect(bp)'''

    bp = img[0:40, 0:100]
    blobs = blob.detect(bp)
    if blobs == ():
        bp = img[50:100, 0:100]
        blobs = blob.detect(bp)
    if blobs == ():
        bp = img[0:100, 0:40]
        blobs = blob.detect(bp)
    if blobs == ():
        bp = img[0:50, 50:100]
        blobs = blob.detect(bp)
    blobs = blob.detect(bp)
    if blobs != ():
        out = cv2.drawKeypoints(bp, blobs, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow("Matched", out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def maskCrown(mask, img):
    #mask = cv2.dilate(mask, (3, 3))
    masked = cv2.bitwise_and(img, img, mask = mask)
    masked = cv2.hconcat([masked, b])
    cv2.imshow("Matched", masked)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    blobDetect(mask)

clahe = cv2.createCLAHE(1.0, (5, 5))

'''for b in boards:
    b[:,:,0] = cv2.equalizeHist(b[:,:,0])
    b[:,:,1] = cv2.equalizeHist(b[:,:,1])
    b[:,:,2] = cv2.equalizeHist(b[:,:,2])
    b[:,:,0] = clahe.apply(b[:,:,0])
    b[:,:,1] = clahe.apply(b[:,:,1])
    b[:,:,2] = clahe.apply(b[:,:,2])
    m = cv2.inRange(b, np.array([200, 100, 0]), np.array([255, 255, 255]))
    cv2.floodFill(m, None, (0, 0), 255)
    cv2.imshow("Matched", m)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''

#Grass and desert can have 2, mines can have 3

#Yellow
ye_low = np.array([170, 0, 0])
ye_high = np.array([255, 255, 255])

#Yellow 2

y2_low = np.array([0, 0, 10])
y2_high = np.array([70, 255, 255])

#Yellow 3
y3_low = np.array([70, 0, 100])
ye3_low = np.array([70, 0, 85])
y3_high = np.array([255, 255, 250])

#Light Green
lg_low = np.array([0, 0, 0])
lg_high = np.array([150, 255, 100])

def wMask(img, low, high, lim):
    i = np.copy(img)
    i[:,:,0] = clahe.apply(i[:,:,0])
    i[:,:,1] = clahe.apply(i[:,:,1])
    i[:,:,2] = clahe.apply(i[:,:,2])
    i = cv2.inRange(i, low, high)
    cv2.rectangle(i, (0, 0), (100, 100), (255, 255, 255), 1)
    cv2.floodFill(i, None, (0, 0), 0)
    i = i[20:80, 20:80]
    if np.sum(i) > lim:
        return True

def fMask(img, low, high):
    i = np.copy(img)
    i[:,:,0] = clahe.apply(i[:,:,0])
    i[:,:,1] = clahe.apply(i[:,:,1])
    i[:,:,2] = clahe.apply(i[:,:,2])
    i[:,:,2] = clahe.apply(i[:,:,1])

    i = cv2.medianBlur(i, 5)
    i = cv2.inRange(i, low, high)

    cv2.rectangle(i, (0, 0), (100, 100), (255, 255, 255), 2)
    cv2.floodFill(i, None, (0, 0), 0)
    cv2.floodFill(i, None, (0, 99), 0)
    cv2.rectangle(i, (0, 0), (100, 100), (255, 255, 255), 1)
    cv2.floodFill(i, None, (0, 0), 0)
    cv2.rectangle(i, (0, 0), (100, 100), (0, 0, 0), 25)
    i = cv2.medianBlur(i, 3)

    i = i[10: 90, 10: 90]
    if np.sum(i) > 100000:
        return True

#region test crown detection
'''wa = cv2.imread("results/Mines.jpg")
#i = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
#wa = cv2.cvtColor(wa[:,:,1], cv2.COLOR_GRAY2RGB)
wa[:,:,0] = clahe.apply(wa[:,:,0])
wa[:,:,1] = clahe.apply(wa[:,:,1])
wa[:,:,2] = clahe.apply(wa[:,:,2])
wa[:,:,2] = clahe.apply(wa[:,:,0])
ma = cv2.inRange(wa, (90, 0, 100), (255, 255, 255))
ma = cv2.medianBlur(ma, 3)
#cv2.rectangle(ma, (0, 0), (37900, 100), (255, 255, 255), 2)
#cv2.floodFill(ma, None, (0, 0), 0)
#cv2.imshow("Matched", wa)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

n = 0
for i in range(int(wa.shape[1]/100)):
    was = wa[0: 100, i * 100: (i + 1) * 100]
    mas = ma[0: 100, i * 100: (i + 1) * 100]
    cv2.rectangle(mas, (0, 0), (100, 100), (255, 255, 255), 1)
    cv2.floodFill(mas, None, (0, 0), 0)
    cv2.rectangle(mas, (35, 35), (70, 70), (0, 0, 0), -1)
    was = cv2.hconcat([was, cv2.cvtColor(mas, cv2.COLOR_GRAY2BGR)])
    mas = cv2.medianBlur(mas, 3)
    if cMine is None:
        cMine = mas
    else:
        cMine = cv2.hconcat([cMine, mas])
    mas = mas[10: 90, 10: 90]
    #cv2.rectangle(mas, (0, 0), (60, 60), (0, 0, 0), 1)
    #cv2.floodFill(mas, None, (0, 0), 0)
    if np.sum(mas) > 130000: #500000
        cv2.rectangle(wa, (i * 100, 0), (i * 100 + 100, 100), (0, 0, 255), 2)
        #cv2.imshow("Matched", mas)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        n += 1

print(n)
cv2.imwrite("results/MineRes.jpg", cv2.vconcat([wa, cv2.cvtColor(cMine, cv2.COLOR_GRAY2BGR)]))

raise SystemExit(0)'''
#endregion

for b in boards:
#if True:
    #b = cv2.imread("data/cropped/8.jpg")
    o = b
    board = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
    board[:,:,2] = clahe.apply(board[:,:,2])
    show = False
    count = 0
    connect = []
    colors = []
    diff = []
    pt = []
    '''if num == 47:
        show = True'''
    for y in range(5):
        colors.append([])
        for x in range(5):
                p = o[y * 100: (y + 1) * 100, x * 100: (x + 1) * 100]
                part = board[y * 100 + 5: (y + 1) * 100 - 5, x * 100 + 5: (x + 1) * 100 - 5]

                H = np.bincount(np.array(part[:,:,0]).ravel())
                check = np.where(part[:,:,0].ravel() == np.argmax(H))[0]
                S = np.bincount(np.array([part[:,:,1].ravel()[i] for i in check]))
                V = np.bincount(np.array([part[:,:,2].ravel()[i] for i in check]))
                diff.append([np.argmax(H), np.argmax(S), np.argmax(V)])

                cv2.rectangle(part, (45, 45), (55, 55), np.array(diff[count]).tolist(), 40)

                text = "Meow"
                color = [255, 255, 255]

                #Important! brackets = (errors)
                #Order: Grass = Sand = Water, Forest (grass), Desert (players, forest, sand), Table (desert), mines (players, forests)
                if mask(part, g_low, g_high, 900000):
                    if grass is None:
                        grass = p
                    else:
                        grass = cv2.hconcat([grass, p])
                    text = "grass"
                    color = [0, 255, 0, 255]
                elif mask(part, s_low, s_high, 900000):
                    color = [0, 150, 255, 255]
                    if wMask(p, ye3_low, y3_high, 60000):
                        pt.append([x * 100 + 50, y * 100 + 50])
                        if cSand is None:
                            cSand = p
                        else:
                            cSand = cv2.hconcat([cSand, p])
                    elif sand is None:
                        sand = p
                    else:
                        sand = cv2.hconcat([sand, p])
                    text = "sand"
                elif mask(part, w_low, w_high, 900000):
                    color = [255, 0, 0, 255]
                    if wMask(p, y2_low, y2_high, 200000):
                        pt.append([x * 100 + 50, y * 100 + 50])
                        if cWater is None:
                            cWater = p
                        else:
                            cWater = cv2.hconcat([cWater, p])
                    elif water is None:
                        water = p
                    else:
                        water = cv2.hconcat([water, p])
                    text = "water"
                elif mask(part, f_low, f_high, 900000):
                    color = [0, 130, 0, 255]
                    if fMask(p, y3_low, y3_high):
                        pt.append([x * 100 + 50, y * 100 + 50])
                        if cForest is None:
                            cForest = p
                        else:
                            cForest = cv2.hconcat([cForest, p])
                    elif forest is None:
                        forest = p
                    else:
                        forest = cv2.hconcat([forest, p])
                    text = "forest"
                elif mask(part, d_low, d_high, 900000):
                    if desert is None:
                        desert = p
                    else:
                        desert = cv2.hconcat([desert, p])
                    text = "desert"
                    color = [170, 160, 125, 255]
                elif mask(part, m_low, m_high, 900000):
                    if mine is None:
                        mine = p
                    else:
                        mine = cv2.hconcat([mine, p])
                    text = "mine"
                    color = [0, 0, 0]
                elif mask(part, t_low, t_high, 900000):
                    if table is None:
                        table = p
                    else:
                        table = cv2.hconcat([table, p])
                    text = "Table"
                    color = [0, 0, 255, 255]
                else:
                    if na is None:
                        na = p
                    else:
                        na = cv2.hconcat([na, p])
                    text = "N/A"
                    color = [255, 255, 255, 255]
                colors[y].append(color)

                if x > 0 and colors[y][x][:3] == colors[y][x-1][:3]:
                    if any(([x * 100 - 50, y * 100 + 50]) in i for i in connect) == False:
                        connect.append([[x * 100 - 50, y * 100 + 50]])
                    for i in connect:
                        if (([x * 100 - 50, y * 100 + 50]) in i) == True and (([x * 100 + 50, y * 100 + 50]) in i) == False:
                            i.append([x * 100 + 50, y * 100 + 50])
                    cv2.line(b, (50 + x * 100, 50 + y * 100), (-50 + x * 100, 50 + y * 100), colors[y][x], 3)

                if y > 0 and colors[y][x][:3] == colors[y-1][x][:3]:
                    if any(([x * 100 + 50, y * 100 - 50]) in i for i in connect) == False:
                        connect.append([[x * 100 + 50, y * 100 - 50]])
                    for i in connect:
                        if (([x * 100 + 50, y * 100 - 50]) in i) == True and (([x * 100 + 50, y * 100 + 50]) in i) == False:
                            i.append([x * 100 + 50, y * 100 + 50])
                    cv2.line(b, (50 + x * 100, 50 + y * 100), (50 + x * 100, -50 + y * 100), colors[y][x], 3)

                #cv2.putText(b, text, (5 + x * 100, 25 + y * 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

                count += 1
    for i in range(len(connect)-1):
        if len(connect)-1 < i: break
        for j in range(len(connect)-1):
            if j == i: continue
            if any([k in connect[i] for k in connect[j]]):
                [connect[i].append(k) for k in connect[j] if k not in connect[i]]
                connect.remove(connect[j])
                break

    print(connect)
    for i in connect:
        points = np.sum([i.count(p) for p in pt])
        print(points)
        for p in pt:
            if points == 0 or p not in i: continue
            cv2.putText(b, f"Points: {np.sum(points) * len(i)}", (p[0] - 45, p[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            points = 0

    show = True
    if show:
        cv2.imshow("Matched", b)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    num += 1

#DEBUG to check which blocks are considered what. Might split into different folders and have each be individual images.
cv2.imwrite("results/WaterRes.jpg", cWater)
cv2.imwrite("results/Water.jpg", water)
cv2.imwrite("results/Forests.jpg", forest)
cv2.imwrite("results/ForestRes.jpg", cForest)
cv2.imwrite("results/Sands.jpg", sand)
cv2.imwrite("results/SandRes.jpg", cSand)
cv2.imwrite("results/Mines.jpg", mine)
cv2.imwrite("results/Grasslands.jpg", grass)
cv2.imwrite("results/Deserts.jpg", desert)
cv2.imwrite("results/Table.jpg", table)
cv2.imwrite("results/NA.jpg", na)
'''cv2.imwrite("results/Mines.jpg", mine)
cv2.imwrite("results/Grasslands.jpg", grass)
cv2.imwrite("results/Deserts.jpg", desert)
cv2.imwrite("results/Table.jpg", table)
cv2.imwrite("results/NA.jpg", na)'''
# Just testing, not final, need to check for the actual crowns and buildings.
#cv2.imwrite("results/Crowns.jpg", crown)