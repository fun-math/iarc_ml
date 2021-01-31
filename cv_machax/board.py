import numpy as np 
import cv2

def detect(cv_img) :
	img=cv_img.copy()
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	b,g,r=np.rollaxis(img,2,0)
	h,s,v=np.rollaxis(img_hsv,2,0)

	mask_colour=((r-g)^2+(g-b)^2+(b-r)^2)>10
	mask_colour=(mask_colour*255).astype(np.uint8)

	mask_blue=(95<=h)*(h<=110)*mask_colour
	# mask_blue=(mask_blue*255).astype(np.uint8)
	# mask_colour=(mask_colour*255).astype(np.uint8)
	# # print(mask_blue.shape)
	_, contours, hierarchy= cv2.findContours(mask_blue,cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)
	
	size=mask_blue.shape[0]
	mask=mask_blue.reshape((size,size,1))
	mask=np.repeat(mask,3,-1)
	cv2.imshow('mask',mask)
	cv2.waitKey(50)
	# print(len(contours))
	i=0
	max_area=0
	brd=[]
	for cnt in contours :
		if cv2.contourArea(cnt)>1e2 :
			# i+=1
			hull=cv2.convexHull(cnt)
			(x,y),(h,w),theta=cv2.minAreaRect(hull)
			area=cv2.contourArea(hull)
			# print(area,h,w)
			if 1.0*abs(h*w-area)/(h*w)<0.05 :
				if abs(np.arctan(1.0*h/w)-np.pi/4)>np.pi/36:
					continue
				i+=1
				if area>max_area :
					max_area=area
					brd=hull
					# print(area)

			# box=cv2.boxPoints(rect)
			# box=np.int0(box)
	if i==0:
		return [False,0]
	return [True,brd]
	# print(i)
	# cv2.drawContours(mask,[brd],0,(0,0,255),3) 
	# mask=np.zeros_like(mask_colour)
	# print(i)

	# cv2.imshow('mask',mask)
	# cv2.imshow('org',mask_colour)
	# cv2.waitKey(0)


if __name__=='__main__':
	cap=cv2.VideoCapture('videos/video2.avi')
	while True :
		ret,frame=cap.read()
		hull=detect(frame)
		if hull[0] :
			cv2.drawContours(frame,[hull[1]],0,(0,0,255),3)
		cv2.imshow('frame',frame)
		cv2.waitKey(50)	
	# img=cv2.imread('5imgc7.jpg')
	# hull=detect(img)
	# if hull[0] :
	# 	cv2.drawContours(img,[hull[1]],0,(0,0,255),3)
	# cv2.imshow('img',img)
	# cv2.waitKey(0)