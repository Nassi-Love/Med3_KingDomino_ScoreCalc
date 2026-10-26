import numpy as np
import cv2
import glob

#cv2.namedWindow("Matched", cv2.WINDOW_NORMAL)

#Since this is cropped, its easy to split it into 25 parts.
#Planning to connect them to neighbors with matching terrain, then checking to see how many, if any, has a crown.
#I could do the opposite, but then i'd have to remember which one has already been checked bleh. I guess I have to do it anyway but the above feels easier.
boards = [cv2.imread(i) for i in sorted(glob.glob("data/cropped/*.jpg"), key=len)]
#board = cv2.imread("data/cropped/2.jpg")
#board = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
num = 1

#Need to do histogram stuff so its easier to compare differences regardless of lighting!

#Detect mines by detecting amount of "black" and "yellow" so it doesnt mistake with forest?

'''m_low = np.array([0, 0, 0])
m_high = np.array([170, 255, 30])

g_low = np.array([35, 165, 85])
g_high = np.array([55, 255, 255])

f_low = np.array([20, 0, 10])
f_high = np.array([80, 255, 80])

s_low = np.array([20, 210, 160])
s_high = np.array([30, 255, 210])

d_low = np.array([15, 10, 50])
d_high = np.array([30, 255, 155])

w_low = np.array([100, 230, 100])
w_high = np.array([110, 255, 210])

t_low = np.array([15, 115, 120])
t_high = np.array([21, 220, 185])'''

mine = grass = forest = sand = desert = water = table = na = crown = [].append([])

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
count = 0
diff = []
def mask(img, low, high, x, y):
    mask = cv2.inRange(img, low, high)
    if np.sum(mask) > 900000:
        return True

clahe = cv2.createCLAHE(1.0, (5, 5))
for b in boards:
    board = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
    #board[:,:,2] = cv2.equalizeHist(board[:,:,2])
    board[:,:,2] = clahe.apply(board[:,:,2])
    show = False
    count = 0
    colors = []
    diff = []
    diff2 = []
    '''if num == 47:
        show = True'''
    for y in range(5):
        colors.append([])
        for x in range(5):
                p = b[y * 100: (y + 1) * 100, x * 100: (x + 1) * 100]
                part = board[y * 100 + 5: (y + 1) * 100 - 5, x * 100 + 5: (x + 1) * 100 - 5]

                H = np.bincount(np.array(part[:,:,0]).ravel())
                check = np.where(part[:,:,0].ravel() == np.argmax(H))[0]
                S = np.bincount(np.array([part[:,:,1].ravel()[i] for i in check]))
                V = np.bincount(np.array([part[:,:,2].ravel()[i] for i in check]))

                '''if show:
                    np.set_printoptions(threshold=np.inf)
                    #print(part[:,:,1])
                    show = False
                    print(np.where(part[:,:,0].ravel() == np.argmax(H))[0])
                    print(np.array([part[:,:,1].ravel()[i] for i in np.where(part[:,:,0].ravel() == np.argmax(H))[0]]))'''

                #H = int((np.argmax(H) + np.argmax(np.setdiff1d(H, np.argmax(H)))) / 2)
                diff.append([np.argmax(H), np.argmax(S), np.argmax(V)])
                diff2.append([np.argmax(np.setdiff1d(H, diff[count][0])), np.argmax(np.setdiff1d(S, diff[count][1])), np.argmax(np.setdiff1d(V, diff[count][2]))])

                cv2.rectangle(part, (45, 45), (55, 55), np.array(diff[count]).tolist(), 40)
                #cv2.rectangle(part, (0, 0), (100, 100), np.array(diff[count]).tolist(), 10)

                text = ""
                color = [255, 255, 255]

                cv2.putText(p, str(np.array(diff[count]).tolist()), (2, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 3)
                cv2.putText(p, str(np.array(diff[count]).tolist()), (2, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.putText(p, str(np.array(diff2[count]).tolist()), (2, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 3)
                cv2.putText(p, str(np.array(diff2[count]).tolist()), (2, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

                #Important! brackets = (errors)
                #Order: Grass = Sand = Water, Forest (grass), Desert (players, forest, sand), Table (desert), mines (players, forests)
                if mask(part, g_low, g_high, x, y):
                    if grass is None:
                        grass = p
                    else:
                        grass = cv2.hconcat([grass, p])
                    text = "grass"
                    color = [0, 255, 0]
                elif mask(part, s_low, s_high, x, y):
                    if sand is None:
                        sand = p
                    else:
                        sand = cv2.hconcat([sand, p])
                    text = "sand"
                    color = [0, 150, 255]
                elif mask(part, w_low, w_high, x, y):
                    if water is None:
                        water = p
                    else:
                        water = cv2.hconcat([water, p])
                        text = "water"
                        color = [255, 0, 0]
                elif mask(part, f_low, f_high, x, y):
                    if forest is None:
                        forest = p
                    else:
                        forest = cv2.hconcat([forest, p])
                    text = "forest"
                    color = [0, 130, 0]
                elif mask(part, d_low, d_high, x, y):
                    if desert is None:
                        desert = p
                    else:
                        desert = cv2.hconcat([desert, p])
                    text = "desert"
                    color = [170, 160, 125]
                elif mask(part, m_low, m_high, x, y):
                    if mine is None:
                        mine = p
                    else:
                        mine = cv2.hconcat([mine, p])
                    text = "mine"
                    color = [0, 0, 0]
                elif mask(part, t_low, t_high, x, y):
                    if table is None:
                        table = p
                    else:
                        table = cv2.hconcat([table, p])
                    text = "Table"
                    color = [0, 0, 255]
                else:
                    if na is None:
                        na = p
                    else:
                        na = cv2.hconcat([na, p])
                    text = "N/A"
                    color = [255, 255, 255]
                colors[y].append(color)

                '''if x > 0 and colors[y][x] == colors[y][x-1]:
                    cv2.line(b, (50 + x * 100, 50 + y * 100), (-50 + x * 100, 50 + y * 100), colors[y][x], 3)
                if y > 0 and colors[y][x] == colors[y-1][x]:
                    cv2.line(b, (50 + x * 100, 50 + y * 100), (50 + x * 100, -50 + y * 100), colors[y][x], 3)'''

                cv2.putText(b, text, (5 + x * 100, 25 + y * 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

                '''cv2.putText(b, str(np.array(diff[count]).tolist()), (2 + x * 100, 40 + y * 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 3)
                cv2.putText(b, str(np.array(diff[count]).tolist()), (2 + x * 100, 40 + y * 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.putText(b, str(np.array([np.argmax(np.setdiff1d(H, diff[count][0])), np.argmax(np.setdiff1d(S, diff[count][1])), np.argmax(np.setdiff1d(V, diff[count][2]))])), (2 + x * 100, 60 + y * 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 3)
                cv2.putText(b, str(np.array([np.argmax(np.setdiff1d(H, diff[count][0])), np.argmax(np.setdiff1d(S, diff[count][1])), np.argmax(np.setdiff1d(V, diff[count][2]))])), (2 + x * 100, 60 + y * 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)'''

                count += 1
    if show:
        cv2.imshow("Matched", b)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    num += 1
'''all = mine
all = cv2.vconcat([all, grass])
all = cv2.vconcat([all, forest])
all = cv2.vconcat([all, sand])
all = cv2.vconcat([all, desert])
all = cv2.vconcat([all, water])
all = cv2.vconcat([all, table])
all = cv2.vconcat([all, na])'''
'''cv2.imshow("Mines", mine)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("Grasslands", grass)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("Forests", forest)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("Sands", sand)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("Deserts", desert)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("Water", water)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("Table", table)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("N/A", na)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

#DEBUG to check which blocks are considered what. Might split into different folders and have each be individual images.
cv2.imwrite("results/Mines.jpg", mine)
cv2.imwrite("results/Grasslands.jpg", grass)
cv2.imwrite("results/Forests.jpg", forest)
cv2.imwrite("results/Sands.jpg", sand)
cv2.imwrite("results/Deserts.jpg", desert)
cv2.imwrite("results/Water.jpg", water)
cv2.imwrite("results/Table.jpg", table)
cv2.imwrite("results/NA.jpg", na)
# Just testing, not final, need to check for the actual crowns and buildings.
cv2.imwrite("results/Crowns.jpg", crown)

#Board 1
#Mine:   N/A
#Grass:  35-45 / 210-255 / 140-160
#Sand:   26 (try 20-30) / 245-250 (try 240-250) / 199 (try 190-210)
#Desert: 23 (try 20-30) / 255 (try 240-255) / 135-140 (try 130-145)
#Water:  105-107 (try 100-110) / 240-255 (try 230-255) / 155-185 (try 150-190)

#Board 2
#Mine:   20-30 (try 10-40) / 0 or 255 (try 10-245) / less than 20 (try 30)
#Grass:  40-50 (try 70-90) / 220-230 (try 210-240) / 140-150 (try 130-160)
#Sand:   26  (try 25 - 28) / 245-255 (try 240-255) / 175-195 (try 170-200)
#Desert: 23-36 (try 20-40) / 46 - 255 (try 40-255) / 110-135 (try 100-140)
#Water:  N/A