import numpy as np 
import cv2
from time import time as t

def detect(cv_img) :
	img=cv_img.copy()
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	b,g,r=np.rollaxis(img,2,0)
	h,s,v=np.rollaxis(img_hsv,2,0)


	mask_colour=((r-g)^2+(g-b)^2+(b-r)^2)<10
	# mask_blue=(98<=h)*(h<=105)#*mask_colour
	# mask_blue=(mask_blue*255).astype(np.uint8)
	mask_colour=(mask_colour*255).astype(np.uint8)
	# print(mask_blue.shape)
	_, contours, hierarchy= cv2.findContours(mask_colour,cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)

	i=0
	# mask=np.zeros((800,800,3),np.uint8)
	mask=mask_colour.reshape((800,800,1))
	mask=np.repeat(mask,3,-1)
	print(mask.shape)
	for cnt in contours :
		if 1e3<cv2.contourArea(cnt)<1e5 :
			# cv2.drawContours(mask,[cnt],0,(0,255,0),3)
			hull=cv2.convexHull(cnt)
			# r=input()
			(x,y),(h,w),theta=cv2.minAreaRect(hull)
			# area=cv2.contourArea(hull)
			if 1.0*abs(h*w-cv2.contourArea(hull))/(h*w)<0.05:
				cv2.drawContours(mask,[hull],0,(0,255,0),3)
				# cv2.imshow('mask',mask)
				# cv2.waitKey(0)
				i+=1 
	print(i)
	# mask=np.zeros_like(mask_colour)

	cv2.imshow('mask',mask)
	# cv2.imshow('org',mask_colour)
	cv2.waitKey(0)


if __name__=='__main__':
	img=cv2.imread('5imgc7.jpg')
	tic=t()
	detect(img)
	toc=t()
	print(toc-tic)