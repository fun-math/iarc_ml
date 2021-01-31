import cv2
import numpy as np 

img=cv2.imread('5imgc7.jpg')
g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_, contours, hierarchy= cv2.findContours(g,cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours :
	if cv2.contourArea(cnt)>1e2 :
		cv2.drawContours(img,[cnt],0,(0,0,255))
print(len(contours))
cv2.imshow('img',img)
cv2.imshow('g',g)
cv2.waitKey(0)
