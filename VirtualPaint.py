import cv2
import numpy as np

cap1 = cv2.VideoCapture(0)
cap1.set(3, 640)     #width, 3 is the ID no. of the width
cap1.set(4, 480)     #height, 4 is the ID no. of the length
cap1.set(10, 150)    #brightness, 10 is the ID no. of the brightness

"""These are the hue, sat, and val minimum and maximum values of colors green and blue respectively, obtained
from the webCamColorDetection project"""
myColors = [[35, 69, 90, 66, 255, 255],
            [99, 111, 0, 114, 255, 255]]

myColorValues = [[0, 255, 0],
                 [255, 0, 0]]   #These are the RGB codes for the colors green and blue respectively

"""The myPoints array will consist of the points through which a 'for loop' will iterate when printing the circles on the canvas"""
myPoints = []  #These points will be appended in the form [x, y, colorId]

"""The initial image (frame from the webcam) is first converted to an HSV image. Then a 'for loop' is iterated in the myColors
array, and a mask is created for the colors present in myColors and the values returned by the getContours fxn are
stored in the variables x and y, now if x & y are zero, then that means that no object of color green or blue is present in the frame
and if x&y are not zero, then that means objects of the colors are present. So, in that case, the values of x, y, and count
will pe added to the newPoints array. Then the value of count will be incremented by one. And in the end, the newPoints array
will be returned by the fxn, which will be used later to append the myPoints[] array"""
def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   #The image passed in as an argument will first be converted to an HSV image
    count = 0   #This counter's value will later be used as the index value for the myColorValues array
    newPoints = []  #This empty array will be later filled with the x,y coordinates and the count value
                    # whenever the green or blue object is detected
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, count])
        count+=1
    return newPoints

"""This is the function that needs to be understood first. First, we get the contour points using the findContours() fxn,
Then for each contour point, we calculate the area, if it is more than 500, we calculate the perimeter, and pass it on
as the epsilon value in the approxPolyDP() fxn. The approxPolyDP fxn returns the coordinates of each of the corner
contour points of the shape in the form of a numpy array. This array is further passed on to the boundingRect() fxn
which returns the x, y , w, and h values of the bounding rectangle to be drawn. Then in the end, the coordinates of the
mid-point of the upper side of the bounding rectangle are returned. These values are then used in the findColor() fxn above"""
def getContours(img):       #This fxn draws the bounding rectangle on the shapes, and thus gives us the position of the object
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, w, y, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

"""This is the final fxn. It is called when the drawing part starts. Now that we have the positions of the markers/objects,
all we need to do is print the colors on the screen. That is accomplished by using the circle() fxn. For every point
in the array myPoints, we draw a filled circle of that particular color with the 1st element of the array as the x
coordinate of the circle's centre and the 2nd element as the y coordinate. And the 3rd element (that describes the
color of the required circle) is used to describe the color of the filled circle"""
def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap1.read()
    imgResult = img.copy()  #copy of the original image
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints)!=0:   #If newPoints is empty, then there is no object of the specified colors in the webcam's frame
        for newP in newPoints:
            myPoints.append(newP)   #If its not empty, then, it's values will be passed on to the myPoints array
    if len(myPoints)!=0:    #If myPoints is not empty, then the drawOnCanvas fxn will be called, thus printing the circles
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):       #adds delay and looks for key press 'q' to break the loop
        break