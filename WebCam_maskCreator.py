import cv2
import numpy as np

cap1 = cv2.VideoCapture(0)
cap1.set(3, 640)     #width, 3 is the ID no. of the width
cap1.set(4, 480)     #height, 4 is the ID no. of the length
cap1.set(10, 100)    #brightness, 10 is the ID no. of the brightness

def empty(a):
    pass

cv2.namedWindow("Trackbars")    #Creating a new window named "Trackbars"
cv2.resizeWindow("Trackbars", 640, 240)     #Resizing the "trackbars" window to a 640x240 window
cv2.createTrackbar("Hue min", "Trackbars", 0, 179, empty)   ##The arguments are (TrackBar_Name, Window_Name, minValue, maxValue, OnChangeFxn)
cv2.createTrackbar("Hue max", "Trackbars", 179, 179, empty)  #creating a trackbar with name "Hue max", minvalue 0, maxvalue 179, and an empty fxn
cv2.createTrackbar("Sat min", "Trackbars", 0, 255, empty)   #The OnChange fxn is called everytime the position of the trackbar is changed
cv2.createTrackbar("Sat max", "Trackbars", 255, 255, empty)
"""The min value of every trackbar is always zero, instead of zero, if you put some other number, then when the program starts running,
the initial position of the trackbar will be at that number"""
cv2.createTrackbar("Val min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val max", "Trackbars", 255, 255, empty)


while True:
    _, img = cap1.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    """The cv2.getTrackbarPos() fxn is used to assign the current trackbar position value to the variable"""
    h_min = cv2.getTrackbarPos("Hue min", "Trackbars")  #The arguments are(trackbar_name, window_name)
    h_max = cv2.getTrackbarPos("Hue max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val max", "Trackbars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    """Whenever we want to check the elements of a given array with the corresponding elements of the two
    arrays among which one array represents the upper bounds and the other array represents the lower bounds,
    we make use of a function called inRange() function in OpenCV and this inRange() function returns an array
    of elements equal to 255 if the elements of the given array lie between the two arrays representing the
    upper bounds and the lower bounds or the inRange() function returns an array of elements equal to 0 if the
    elements of the given array do not lie between the two arrays representing the upper bounds and the lower bounds."""
    mask = cv2.inRange(imgHSV, lower, upper)

    """Whenever we are dealing with images while solving computer vision problems, there arises a necessity to wither
    manipulate the given image or extract parts of the given image based on the requirement, in such cases we make
    use of bitwise operators in OpenCV and when the elements of the arrays corresponding to the given two images must
    be combined bit wise, then we make use of an operator in OpenCV called but wise and operator using which the arrays
    corresponding to the two images can be combined resulting in merging of the two images and bit wise operation on
    the two images returns an image with the merging done as per the specification."""
    result = cv2.bitwise_and(img, img, mask = mask)     #The arguments here are (src_img1, src_img2, mask)

    """We use both bitwise operations and masks to construct ROIs (Regions of interest) that are non-rectangular.
    This allows us to extract regions from images that are of completely arbitrary shape. Put simply; a mask allows us
    to focus only on the portions of the image that interests us. For example, let’s say that we were building a
    computer vision system to recognize faces. The only part of the image we are interested in finding and describing is
    the parts of the image that contain faces — we simply don’t care about the rest of the image’s content.
    Provided that we could find the faces in the image, we may construct a mask to show only the faces in the image."""
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    h_stack = np.hstack([img, mask, result])
    cv2.imshow("Stack", h_stack)
    if cv2.waitKey(1) & 0xFF == ord('q'):       #adds delay and looks for key press 'q' to break the loop
        break

cap1.release()  #release() -> Closes video file or capturing device.
                #it releases the hardware and software resources. BUT, in the new version of openCV,
                #it executes automatically after exiting the loop of frames.
cv2.destroyAllWindows()