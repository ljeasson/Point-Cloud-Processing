import numpy as np
import cv2

img = cv2.imread("tahoe_big.png")
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

img = cv2.bitwise_not(img)
th2 = cv2.adaptiveThreshold(img,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,-2)
cv2.imshow("th2", th2)
cv2.imwrite("th2.jpg", th2)
cv2.waitKey(0)
cv2.destroyAllWindows()

horizontal = th2
vertical = th2
rows,cols = horizontal.shape
horizontalsize = int(cols / 30)
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize,1))
horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, -1))
cv2.imshow("horizontal", horizontal)
cv2.imwrite("horizontal.jpg", horizontal)
cv2.waitKey(0)
cv2.destroyAllWindows()

verticalsize = int(rows / 30)
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))
cv2.imshow("vertical", vertical)
cv2.imwrite("vertical.jpg", vertical)
cv2.waitKey(0)
cv2.destroyAllWindows()

vertical = cv2.bitwise_not(vertical)
cv2.imshow("vertical_bitwise_not", vertical)
cv2.imwrite("vertical_bitwise_not.jpg", vertical)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 1
edges = cv2.adaptiveThreshold(vertical,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,-2)
cv2.imshow("edges", edges)
cv2.imwrite("edges.jpg", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 2
kernel = np.ones((2, 2), dtype = "uint8")
dilated = cv2.dilate(edges, kernel)
cv2.imshow("dilated", dilated)
cv2.imwrite("dilated.jpg", dilated)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 3
smooth = vertical.copy()

# Step 4
smooth = cv2.blur(smooth, (4,4))
cv2.imshow("smooth", smooth)
cv2.imwrite("smooth.jpg", smooth)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 5
(rows, cols) = np.where(img == 0)
vertical[rows, cols] = smooth[rows, cols]

cv2.imshow("vertical_final", vertical)
cv2.imwrite("vertical_final.jpg", vertical)
cv2.waitKey(0)
cv2.destroyAllWindows()


#inverse the image, so that lines are black for masking
horizontal_inv = cv2.bitwise_not(horizontal)
#perform bitwise_and to mask the lines with provided mask
masked_img = cv2.bitwise_and(img, img, mask=horizontal_inv)
#reverse the image back to normal
masked_img_inv = cv2.bitwise_not(masked_img)
cv2.imshow("masked img", masked_img_inv)
cv2.imwrite("result2.jpg", masked_img_inv)
cv2.waitKey(0)
cv2.destroyAllWindows()


'''
image = cv2.imread("tahoe_big.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 15)

thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,3)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
erode = cv2.erode(thresh, kernel, iterations=1)
dilate = cv2.dilate(erode, kernel, iterations=3)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

mask = np.zeros(image.shape, dtype=np.uint8)
for c in cnts:
    area = cv2.contourArea(c)
    if area > 850:
        cv2.drawContours(mask, [c], -1, (255,255,255), -1)

mask = cv2.dilate(mask, kernel, iterations=1)
image = 255 - image
result = 255 - cv2.bitwise_and(mask, image)

cv2.imshow('result', result)
cv2.waitKey(0)
'''