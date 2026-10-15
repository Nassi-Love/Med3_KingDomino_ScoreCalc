import numpy as np
import cv2
import glob

board = cv2.imread("data/cropped/1.jpg")
lined = np.copy(board)
dominos = [cv2.imread(i) for i in glob.glob("templates/crowned/*.png")]
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
parts = []
cv2.namedWindow("Matched", cv2.WINDOW_NORMAL)
for y in range(5):
    for x in range(5):
        part = board[y * 100: (y + 1) * 100, x * 100: (x + 1) * 100]
        cv2.imshow("Matched", part)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #parts.append(part)

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