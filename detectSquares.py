import numpy as np
import cv2
import glob

'''board = cv2.imread("data/cropped/1.jpg")
lined = np.copy(board)
dominos = [cv2.imread(i) for i in glob.glob("templates/crowned/*.png")]'''
'''clean = [np.copy(i) for i in dominos]
dominos.extend([cv2.rotate(i, cv2.ROTATE_90_CLOCKWISE) for i in clean])
dominos.extend([cv2.rotate(i, cv2.ROTATE_180) for i in clean])
dominos.extend([cv2.rotate(i, cv2.ROTATE_90_COUNTERCLOCKWISE) for i in clean])
loc = []
for i in dominos:
    matching = cv2.matchTemplate(board, i, cv2.TM_CCOEFF_NORMED)
    if any(map(len, np.where(matching >= 0.7))):
        minV, maxV, minL, maxL = cv2.minMaxLoc(matching)
        sX, sY = maxL
        cv2.rectangle(lined, (sX, sY), (sX + i.shape[1], sY + i.shape[0]), (0, 0, 255), 3)
        loc.append([np.where(matching >= 0.7)])
print(loc)'''
#Since this is cropped, its easy to split it into 25 parts.
#Planning to connect them to neighbors with matching terrain, then checking to see how many, if any, has a crown.
#I could do the opposite, but then i'd have to remember which one has already been checked bleh. I guess I have to do it anyway but the above feels easier.
boards = [cv2.imread(i) for i in sorted(glob.glob("data/cropped/*.jpg"), key=len)]
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
        #print("blue:", abs(curCol[0]-nextCol[0]), "green:", abs(curCol[1]-nextCol[1]), "red:", abs(curCol[2]-nextCol[2]))
    if y > 0:
        nextCol = colors[y-1][x]
        up = abs(np.subtract(curCol, nextCol))
        #print("blue:", abs(curCol[0]-nextCol[0]), "green:", abs(curCol[1]-nextCol[1]), "red:", abs(curCol[2]-nextCol[2]))
    return [left, up]

def checkNeighbors(self, other):
    return np.sum(abs(np.subtract(self, other)))

def kMeans(img, draw = None, colors = 1):
    if draw is None:
        draw = img
    px = np.float32(np.array(img).reshape(-1, 3)) #numpy.reshape(), -1 means unknown. Unknown num arrays/pixels with 3 elements, BGR.
    c = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, label, palette = cv2.kmeans(px, colors, None, c, 10, cv2.KMEANS_RANDOM_CENTERS)
    palette = [int(i) for i in palette[0]]
    cv2.rectangle(draw, (45 + x * 100, 45 + y * 100), (55 + x * 100, 55 + y * 100), palette, 50)
    draw = cv2.GaussianBlur(draw, (5, 5), 0)
    #cv2.circle(img, (50 + x * 100, 50 + y * 100), 1, palette, 75)
    return label, palette

num = 1
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
            '''part = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
            sobelx = cv2.Sobel(part, cv2.CV_64F, 1, 0, ksize = 3)
            sobely = cv2.Sobel(part, cv2.CV_64F, 0, 1, ksize = 3)
            part = cv2.convertScaleAbs(cv2.magnitude(sobelx, sobely))
            sobelx = cv2.Sobel(bl, cv2.CV_64F, 1, 0, ksize = 3)
            sobely = cv2.Sobel(bl, cv2.CV_64F, 0, 1, ksize = 3)
            part = cv2.convertScaleAbs(cv2.magnitude(sobelx, sobely))'''
            '''sides = [part[10:30, 40:60]]
            np.append(sides, part[40:60, 10:30])
            np.append(sides, part[70:90, 40:60])
            np.append(sides, part[40:60, 70:90])'''
            #print(sides)

            '''sides = [part[70:90, 40:60]] #[part[10:30, 40:60]]
            #np.append(sides, part[40:60, 10:30])
            #np.append(sides, part[70:90, 40:60])
            np.append(sides, part[40:60, 70:90])
            _, palette = kMeans(sides, part)
            _, palette = kMeans(part)
            _, palette = kMeans(part)'''

            _, palette = kMeans(part)

            # Need to check hue next

            colors[y].append(palette)

            #cv2.rectangle(board, (45 + x * 100, 45 + y * 100), (55 + x * 100, 55 + y * 100), palette, 50)
            #cv2.circle(board, (50 + x * 100, 50 + y * 100), 1, palette, 75)

            if x > 0 and checkNeighbors(colors[y][x], colors[y][x-1]) < 65:
                cv2.line(board, (50 + x * 100, 50 + y * 100), (-50 + x * 100, 50 + y * 100), (0, 0, 255), 3)
            if y > 0 and checkNeighbors(colors[y][x], colors[y-1][x]) < 65:
                cv2.line(board, (50 + x * 100, 50 + y * 100), (50 + x * 100, -50 + y * 100), (0, 0, 255), 3)

            '''diff[y].append(checkNeighborsDB(colors, x, y))
    if num <= 3:
        print(repr(np.array(diff)))
        num +=1'''
    if num <= 5:
        board = cv2.cvtColor(board, cv2.COLOR_HSV2BGR)
        cv2.imshow("Matched", board)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        num +=1
    '''cv2.imwrite(f'colors/cropped/{num}.png', np.array(colors))
    num += 1'''
'''cv2.imwrite('cropped/colors.jpg', np.array(colors))
cv2.imshow("Matched", np.array(colors)/255)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

[[[[0, 0, 0], [0, 0, 0]], [[60, 47, 25], [0, 0, 0]], [[56, 79, 111], [0, 0, 0]], [[2, 9, 4], [0, 0, 0]], [[1, 7, 2], [0, 0, 0]]],
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
[[[[  0,   0,   0],
         [  0,   0,   0]],

        [[139,  60,  94],
         [  0,   0,   0]],

        [[153,  25,  38],
         [  0,   0,   0]],

        [[  2,   4,   1],
         [  0,   0,   0]],

        [[  1,   1,   0],
         [  0,   0,   0]]],


       [[[  0,   0,   0],
         [  4,   1,   7]],

        [[  9,  90,  52],
         [152,  29,  35]],

        [[  1,   1,   2],
         [  0,   3,   1]],

        [[  9,   5,  15],
         [  7,   6,  15]],

        [[  4,  76,  37],
         [  4,  81,  52]]],


       [[[  0,   0,   0],
         [  2,   1,  12]],

        [[ 22,  56,   2],
         [ 33,  33,  62]],

        [[ 24,  42,  31],
         [ 58,  74,  91]],

        [[ 61,  76,  93],
         [ 12,   7,  17]],

        [[  2,  80,  56],
         [  6,   3,   2]]],


       [[[  0,   0,   0],
         [  3,   0,   8]],

        [[ 28,  53,  11],
         [  3,   3,   5]],

        [[103,   6,  95],
         [ 82,  45, 121]],

        [[125,  28,  97],
         [ 18,  59,  69]],

        [[ 14,   1,  12],
         [  2,  20,   1]]],


       [[[  0,   0,   0],
         [ 10,  83,  44]],

        [[ 83,  24,   1],
         [ 65,   6,  56]],

        [[ 12,  17,  31],
         [ 26,  17,   8]],

        [[105,  38,  72],
         [  6,   7,  17]],

        [[ 22,  55,  95],
         [ 14,  47,  90]]]]

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
 [[6, 160, 184], [7, 164, 187], [39, 89, 106], [62, 98, 106], [22, 136, 92]]]
#Playing with the perspective data (not successful yet, bad idea to do it so early oop, but did find some lines... kinda... The goal was to figure out the perspective and size of each square)
'''board = cv2.imread("data/full/DSC_1281.JPG", cv2.IMREAD_GRAYSCALE)

#Find edges using Sobel
sobelx = cv2.Sobel(board, cv2.CV_64F, 1, 0, ksize = 3)
sobely = cv2.Sobel(board, cv2.CV_64F, 0, 1, ksize = 3)
mag = cv2.convertScaleAbs(cv2.magnitude(sobelx, sobely))

#Trying to despeckle the image
bilateral = cv2.bilateralFilter(mag, 25, 45, 45)

canny = cv2.Canny(bilateral, 30, 100)
contours, h = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(canny, contours, -1, (255, 0, 0), 3)

cv2.namedWindow("Matched", cv2.WINDOW_NORMAL)
cv2.imshow("Matched", canny)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

#Misc attempts
'''boards = glob.glob("data/cropped/*.JPG")
crown = cv2.imread("templates/crown.png")
board = cv2.GaussianBlur(mag, (3, 3), 0)
matched = cv2.matchTemplate(board, crown, cv2.TM_SQDIFF)'''

'''magP = np.copy(mag)
lines = cv2.HoughLines(mag, 1, np.pi / 180, 150, None, 0, 0)
if lines is not None:
    for i in range(0, len(lines)):
        pix = lines[i][0][0]
        rad = lines[i][0][1]
        a = math.cos(rad)
        b = math.sin(rad)
        x = a * pix
        y = b * pix
        pt1 = (int(x + 1000*(-b)), int(y + 1000*(a)))
        pt2 = (int(x + 1000*(-b)), int(y - 1000*(a)))

        cv2.line(mag, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
linesP = cv2.HoughLinesP(mag, 1, np.pi / 180, 50, None, 50, 10)
if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv2.line(magP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)'''

'''dominos = [cv2.imread(i, cv2.IMREAD_GRAYSCALE) for i in glob.glob("templates/*.png")]
loc = []
for i in dominos:
    w, h = i.shape[::-1]
    matching = cv2.matchTemplate(board, i, cv2.TM_CCOEFF_NORMED)
    resize = imutils.resize()
    if any(map(len, np.where(matching >= 0.70))):
        (sX, sY) = cv2.minMaxLoc(matching)[3:]
        cv2.rectangle(board, (sX, sY), (sX + i.shape[1], sY + i.shape[0]), (255, 0, 0), 3)
        loc.append([np.where(matching >= 0.70)])
print(loc)'''