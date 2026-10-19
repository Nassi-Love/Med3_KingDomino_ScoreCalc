import numpy as np
import cv2
import glob

#Since this is cropped, its easy to split it into 25 parts.
#Planning to connect them to neighbors with matching terrain, then checking to see how many, if any, has a crown.
#I could do the opposite, but then i'd have to remember which one has already been checked bleh. I guess I have to do it anyway but the above feels easier.
boards = [cv2.imread(i) for i in sorted(glob.glob("data/cropped/*.jpg"), key=len)]
#board = cv2.imread("data/cropped/2.jpg")
#board = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
num = 1

#Need to do thresholding so its easier to compare differences regardless of lighting!

m_low = np.array([0, 0, 0])
m_high = np.array([255, 255, 30]) # 170 Hue instead if 255 too big

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
t_high = np.array([21, 220, 185])

'''t_low = np.array([18, 119, 121])
t_high = np.array([21, 219, 183])'''

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

cv2.namedWindow("Matched", cv2.WINDOW_NORMAL)

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
    if np.sum(mask) > 50:
        return True

for b in boards:
    board = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
    show = False
    count = 0
    colors = []
    diff = []
    for y in range(5):
        for x in range(5):
                p = b[y * 100: (y + 1) * 100, x * 100: (x + 1) * 100]
                part = board[y * 100: (y + 1) * 100, x * 100: (x + 1) * 100]

                H = np.bincount(np.array(part[:,:,0]).ravel())
                S = np.bincount(np.array(part[:,:,1]).ravel())
                V = np.bincount(np.array(part[:,:,2]).ravel())
                diff.append([np.argmax(H), np.argmax(S), np.argmax(V)])

                cv2.rectangle(part, (45, 45), (55, 55), np.array(diff[count]).tolist(), 200)

                text = ""
                color = [255, 255, 255]

                if mask(part, g_low, g_high, x, y):
                    text = "grass"
                elif mask(part, f_low, f_high, x, y):
                    text = "forest"
                elif mask(part, s_low, s_high, x, y):
                    text = "sand"
                elif mask(part, t_low, t_high, x, y):
                    text = "Table"
                    print(np.array(diff[count]).tolist())
                    color = [0, 0, 255]
                    show = True
                elif mask(part, d_low, d_high, x, y):
                    text = "desert"
                elif mask(part, w_low, w_high, x, y):
                    text = "water"
                elif mask(part, m_low, m_high, x, y):
                    text = "mine"
                else:
                    text = "N/A"
                    #show = True
                    #print(np.array(diff[count]).tolist())
                    '''cv2.imshow("Matched", p)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()'''
                count += 1

                cv2.putText(b, text, (10 + x * 100, 60 + y * 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

                '''board = cv2.cvtColor(board, cv2.COLOR_HSV2BGR_FULL)
                cv2.rectangle(board, (45 + x * 100, 45 + y * 100), (55 + x * 100, 55 + y * 100), color, 50)
                board = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)'''
    #board = cv2.cvtColor(board, cv2.COLOR_HSV2BGR_FULL)
    if show:
        cv2.imshow("Matched", b)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    '''if num <= 3:
        cv2.imshow("Matched", board)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''
    num += 1

'''cv2.imshow("Matched", board)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(repr(np.array(diff)).replace('\n', ''))'''

#HSV (0–179, 0-255, 0-255)

#Board 1
#Mine:   N/A
#Grass:  35-45 / 210-255 / 140-160
#Sand:   26 (try 20-30) / 245-250 (try 240-250) / 199 (try 190-210)
#Desert: 23 (try 20-30) / 255 (try 240-255) / 135-140 (try 130-145)
#Water:  105-107 (try 100-110) / 240-255 (try 230-255) / 155-185 (try 150-190)
[[ 43, 220, 160], [106, 255, 185], [ 48, 188,  23], [ 38, 255,  63], [ 38, 170,  62],
 [ 43, 220, 159], [ 51, 170,  62], [ 38, 170,  58], [ 37, 255,  60], [ 44, 220, 151],
 [ 41, 212, 154], [ 23, 255, 139], [ 32,  70, 140], [ 48, 255,  24], [ 41, 255, 148],
 [ 42, 225, 151], [ 23, 255, 136], [105, 255, 185], [ 37, 255, 148], [ 39, 255, 152],
 [ 55,  64,  27], [106, 255, 156], [107, 243, 174], [ 41, 255, 142], [ 26, 247, 199]]

#Board 2
#Mine:   20-30 (try 10-40) / 0 or 255 (try 10-245) / less than 20 (try 30)
#Grass:  40-50 (try 70-90) / 220-230 (try 210-240) / 140-150 (try 130-160)
#Sand:   26  (try 25 - 28) / 245-255 (try 240-255) / 175-195 (try 170-200)
#Desert: 23-36 (try 20-40) / 46 - 255 (try 40-255) / 110-135 (try 100-140)
#Water:  N/A
[[ 26, 255, 179], [ 26,  46, 117], [ 26, 255, 178], [ 24, 255,  15], [ 23, 102, 112],
 [ 30,   0,  19], [ 23, 255, 114], [ 26, 255, 183], [ 26, 255, 181], [ 51, 255,  42],
 [ 20,   0,  16], [ 23, 126, 125], [ 24,  51, 123], [ 26, 255, 186], [ 26, 255, 184],
 [ 20, 255,  18], [ 30, 255,  14], [ 42, 226, 150], [ 44, 226, 145], [ 26, 255, 187],
 [ 26, 248, 193], [ 26, 246, 193], [ 23, 255, 130], [ 26,  78, 134], [ 42, 221, 142]]

#Hue
[[ 52], [ 52], [ 52], [ 48], [ 46],
 [ 60], [ 46], [ 52], [ 52], [102],
 [ 40], [ 46], [ 58], [ 52], [ 52],
 [ 40], [ 60], [ 84], [ 88], [ 52],
 [ 52], [ 52], [ 46], [ 52], [ 84]]

[[ 20], [ 27], [ 23], [ 26], [ 35],
 [ 20], [  0], [ 23], [ 26], [ 25],
 [ 19], [ 20], [ 22], [  5], [255],
 [ 19], [  0], [ 40], [ 42], [ 27],
 [ 20], [ 26], [ 27], [ 25], [255]]

#Saturation
[[20], [27], [23], [26], [26],
 [20], [30], [23], [26], [25],
 [19], [ 0], [20], [ 7], [25],
 [19], [ 0], [40], [42], [26],
 [20], [26], [26], [24], [40]]

#Value
[[ 20], [ 26], [ 23], [255], [ 24],
 [ 20], [ 30], [ 23], [ 26], [255],
 [ 19], [ 24], [ 10], [ 23], [ 25],
 [ 19], [  0], [ 42], [ 38], [ 26],
 [ 21], [255], [ 25], [ 24], [ 41]]

#Wah
[[  0], [118], [  0], [ 14], [107],
 [ 19], [  0], [  0], [  0], [ 17],
 [ 16], [111], [116], [  0], [184],
 [ 16], [  0], [150], [145], [  0],
 [193], [193], [114], [130], [ 18]]

#RGB
[[ 92], [  0], [119], [ 10], [ 21],
 [103], [ 17], [103], [  0], [  5],
 [131], [ 14], [ 99], [ 55], [  0],
 [119], [ 14], [ 26], [ 95], [157],
 [ 17], [164], [169], [ 59], [  0]]

'''num = 1
for board in boards:
    colors = []
    diff = []
    board = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
    board = cv2.GaussianBlur(board, (5, 5), 0)
    for y in range(5):
        colors.append([])
        diff.append([])
        for x in range(5):
            part = board[y * 100: (y + 1) * 100, x * 100: (x + 1) * 100]
            #part = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)

            ''sides = [part[70:90, 40:60]] #[part[10:30, 40:60]]
            #np.append(sides, part[40:60, 10:30])
            #np.append(sides, part[70:90, 40:60])
            np.append(sides, part[40:60, 70:90])
            _, palette = kMeans(sides, part)
            _, palette = kMeans(part)
            _, palette = kMeans(part)''

            _, palette = kMeans(part)
            colors[y].append(palette)

            cv2.rectangle(board, (45 + x * 100, 45 + y * 100), (55 + x * 100, 55 + y * 100), palette, 50)
            #cv2.circle(board, (50 + x * 100, 50 + y * 100), 1, palette, 75)

            if x > 0 and checkNeighbors(colors[y][x], colors[y][x-1]) < 65:
                cv2.line(board, (50 + x * 100, 50 + y * 100), (-50 + x * 100, 50 + y * 100), (0, 0, 255), 3)
            if y > 0 and checkNeighbors(colors[y][x], colors[y-1][x]) < 65:
                cv2.line(board, (50 + x * 100, 50 + y * 100), (50 + x * 100, -50 + y * 100), (0, 0, 255), 3)

            diff[y].append(checkNeighborsDB(colors, x, y))
    if num <= 3:
        print(repr(np.array(diff)))
        num +=1

    if num <= 5:
        board = cv2.cvtColor(board, cv2.COLOR_HSV2BGR)
        cv2.imshow("Matched", board)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        num +=1'''

'''[[[[0, 0, 0], [0, 0, 0]], [[60, 47, 25], [0, 0, 0]], [[56, 79, 111], [0, 0, 0]], [[2, 9, 4], [0, 0, 0]], [[1, 7, 2], [0, 0, 0]]],
 [[[0, 0, 0], [2, 8, 1]], [[1, 41, 89], [57, 80, 115]], [[1, 7, 1], [2, 6, 3]], [[7, 8, 8], [7, 7, 9]], [[5, 51, 74], [3, 51, 81]]],
 [[[0, 0, 0], [3, 2, 1]], [[17, 67, 44], [21, 28, 46]], [[5, 22, 32], [15, 57, 77]], [[14, 62, 79], [6, 13, 10]], [[3, 48, 81], [2, 10, 3]]],
 [[[0, 0, 0], [2, 8, 1]], [[18, 73, 39], [1, 2, 4]], [[74, 93, 54], [70, 117, 26]], [[66, 36, 29], [10, 19, 76]], [[2, 24, 4], [5, 5, 9]]],
 [[[0, 0, 0], [6, 107, 82]], [[30, 93, 78], [54, 59, 35]], [[19, 19, 7], [1, 15, 26]], [[63, 12, 16], [2, 9, 13]], [[8, 45, 68], [8, 30, 59]]]]

[[[  0,   0], [132,   0], [246,   0], [ 15,   0], [ 10,   0]],
 [[  0,  11], [131, 252], [  9,  11], [ 23,  23], [130, 135]],
 [[  0,   6], [128,  95], [ 59, 149], [155,  29], [132,  15]],
 [[  0,  11], [130,   7], [221, 213], [131, 105], [ 30,  19]],
 [[  0, 195], [201, 148], [ 45,  42], [ 91,  24], [121,  97]]]

[[[[0, 0, 0], [0, 0, 0]], [[0, 163, 60], [0, 0, 0]], [[0, 159, 62], [0, 0, 0]], [[4, 108, 111], [0, 0, 0]], [[6, 5,37], [0, 0, 0]]],
 [[[0, 0, 0], [8, 143, 111]], [[8, 30, 26], [0, 50, 25]], [[0, 111, 91], [0, 2, 4]], [[0, 3, 3], [4, 113, 118]], [[19, 89, 122], [21, 29, 41]]],
 [[[0, 0, 0], [1, 2, 6]], [[9, 19, 35], [2, 9, 15]], [[0, 54, 20], [2, 174, 56]], [[2, 170, 52], [0, 7, 7]], [[1, 7, 10], [18, 89, 125]]],
 [[[0, 0, 0], [6, 7, 3]], [[10, 8, 9], [5, 4, 23]], [[14, 89, 69], [19, 139, 26]], [[1, 4, 7], [18, 35, 33]], [[19, 23, 23], [2, 19, 20]]],
 [[[0, 0, 0], [13, 132, 118]], [[1, 1, 3], [2, 123, 112]], [[4, 80, 81], [20, 46, 38]], [[3, 47, 0], [18, 89, 31]], [[16, 95, 30], [17, 17, 24]]]]

[[[  0,   0], [223,   0]  [221,   0], [223,   0], [ 48,   0]],
 [[  0, 262], [ 64,  75], [202,   6], [  6, 235], [230,  91]],
 [[  0,   9], [ 63,  26], [ 74, 232], [224,  14], [ 18, 232]],
 [[  0,  16], [ 27,  32], [172, 184], [ 12,  86], [ 65,  41]],
 [[  0, 263], [  5, 237], [165, 104], [ 50, 138], [141,  58]]]

#[left, up] BGR
[[[[0, 0, 0], [0, 0, 0]], [[139, 60, 94], [0, 0, 0]], [[153, 25, 38], [0, 0, 0]], [[2, 4, 1], [0, 0, 0]], [[1, 1, 0], [0, 0, 0]]],
 [[[0, 0, 0], [4, 1, 7]], [[9, 90, 52], [152, 29, 35]], [[1, 1, 2], [0, 3, 1]], [[9, 5, 15], [7, 6, 15]], [[4, 76, 37], [4, 81, 52]]],
 [[[0, 0, 0], [2, 1, 12]], [[22, 56, 2], [33, 33, 62]], [[24, 42, 31], [58, 74, 91]], [[61, 76, 93], [12, 7, 17]], [[2, 80, 56], [6, 3, 2]]],
 [[[0, 0, 0], [3, 0, 8]], [[28, 53, 11], [3, 3, 5]], [[103, 6, 95], [82, 45, 121]], [[125, 28, 97], [18, 59, 69]], [[14, 1, 12], [2, 20, 1]]],
 [[[0, 0, 0], [10, 83, 44]], [[83, 24, 1], [65, 6, 56]], [[12, 17, 31], [26, 17, 8]], [[105, 38, 72], [6, 7, 17]], [[22, 55, 95], [14, 47, 90]]]]

[[[[0, 0, 0], [0, 0, 0]], [[69, 43, 60], [0, 0, 0]], [[66, 46, 62], [0, 0, 0]], [[15, 99, 112], [0, 0, 0]], [[27, 36, 38], [0, 0, 0]]],
 [[[0, 0, 0], [22, 97, 112]], [[16, 25, 26], [31, 29, 26]], [[37, 77, 92], [2, 2, 4]], [[0, 3, 4], [17, 104, 120]], [[13, 100, 136], [31, 32, 54]]],
 [[[0, 0, 0], [3, 5, 7]], [[23, 34, 35], [10, 14, 16]], [[36, 17, 19], [83, 46, 57]], [[80, 41, 53], [3, 8, 8]], [[3, 12, 10], [13, 104, 138]]],
 [[[0, 0, 0], [0, 1, 2]], [[3, 8, 9], [20, 25, 24]], [[8, 83, 20], [64, 41, 23]], [[1, 8, 11], [17, 8, 87]], [[10, 1, 77], [10, 21, 20]]],
 [[[0, 0, 0], [22, 106, 119]], [[1, 5, 3], [24, 103, 113]], [[32, 76, 81], [16, 56, 12]], [[23, 10, 1], [38, 38, 24]], [[40, 37, 15], [8, 0, 68]]]]

[[[  0,   0], [290,   0], [214,   0], [  6,   0], [  3,   0]],
 [[  0,  12], [152, 214], [  5,   5], [ 28,  27], [115, 137]],
 [[  0,  14], [ 79, 127], [ 97, 223], [230,  35], [139,  13]],
 [[  0,  12], [ 91,  10], [204, 247], [247, 144], [ 27,  22]],
 [[  0, 137], [108, 128], [ 60,  50], [215,  28], [171, 150]]]

[[[  0,   0], [171,   0], [174,   0], [225,   0], [100,   0]],
 [[  0, 229], [ 66,  86], [205,   7], [  7, 239], [247, 116]],
 [[  0,  14], [ 92,  40], [ 72, 185], [173,  19], [ 25, 253]],
 [[  0,   4], [ 19,  69], [109, 126], [ 18, 111], [ 88,  50]],
 [[  0, 246], [  8, 239], [188,  82], [ 32, 100], [ 92,  76]]]

[[[35, 149, 103], [172, 90, 9], [21, 65, 47], [22, 61, 46], [20, 62, 46]],
 [[31, 151, 97], [22, 61, 44], [20, 62, 46], [28, 67, 61], [25, 143, 97]],
 [[33, 150, 108], [54, 94, 106], [78, 136, 137], [17, 60, 44], [19, 140, 101]],
 [[29, 150, 100], [56, 97, 111], [159, 91, 16], [35, 118, 112], [21, 120, 101]],
 [[39, 67, 56], [122, 91, 55], [134, 74, 24], [29, 112, 96], [7, 167, 190]]]

[[[3, 144, 168], [72, 102, 108], [6, 148, 170], [21, 49, 59], [48, 85, 96]],
 [[25, 48, 57], [41, 73, 82], [5, 150, 174], [4, 153, 177], [17, 53, 43]],
 [[28, 53, 63], [51, 87, 98], [87, 104, 117], [7, 145, 169], [4, 156, 180]],
 [[28, 54, 66], [31, 62, 74], [24, 144, 94], [24, 137, 83], [14, 136, 160]],
 [[6, 160, 184], [7, 164, 187], [39, 89, 106], [62, 98, 106], [22, 136, 92]]]'''