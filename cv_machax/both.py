import numpy as np 
import cv2
from time import time as tm
import glob

def detect(cv_img) :
	img=cv_img.copy()
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	# img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	b,g,r=np.rollaxis(img,2,0)
	h,s,v=np.rollaxis(img_hsv,2,0)

	mask_colour=((r-g)^2+(g-b)^2+(b-r)^2)>10
	mask_colour=(mask_colour*255).astype(np.uint8)

	(low,high)=(95,108)
	mask_blue=(low<=h)*(h<=high)*mask_colour
	
	kernel=np.ones((5,5),np.uint8)
	mask_blue=cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)
	# mask_blue=cv2.GaussianBlur(mask_blue,(5,5),0)
	
	_, contours, hierarchy= cv2.findContours(mask_blue,cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)

	i=0
	area=0
	for cnt in contours :
		if cv2.contourArea(cnt)>1e2 :
			M=cv2.moments(cnt)
			rect=cv2.minAreaRect(cnt)
			(x,y),(h,w),theta=rect
			# if abs(np.arctan(1.0*h/w)-np.pi/4)>np.pi/36:
				# continue
			hull=cv2.convexHull(cnt)
			epsilon=0.1*cv2.arcLength(hull,True)
			approx=cv2.approxPolyDP(hull,epsilon,True)
			if len(approx)==4:#1.0*abs(M['m00']-h*w)/(h*w)<0.3 :
				i+=1
				if M['m00']>area :
					final_m=M
					# brd=rect
					brd=approx
					area=M['m00']
	print(i)
	size=mask_blue.shape[0]
	mask=mask_blue.reshape((size,size,1))
	mask=np.repeat(mask,3,-1)
	if i>0 :
		cv2.drawContours(mask,[brd],0,(0,0,255),3)
		# cv2.drawContours(mask,[np.int0(cv2.boxPoints(brd))],0,(0,0,255),3)
				
	# cv2.imshow('mask',mask)
	# cv2.waitKey(250)
	if i==0:
		return [False,0,mask]

	else :
		return [True,brd,mask]
	mask_colour=((r-g)^2+(g-b)^2+(b-r)^2)<10
	# mask_blue=(98<=h)*(h<=105)#*mask_colour
	# mask_blue=(mask_blue*255).astype(np.uint8)
	mask_colour=(mask_colour*255).astype(np.uint8)
	# print(mask_blue.shape)
	_, contours, hierarchy= cv2.findContours(mask_colour,cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)

	i=0
	# mask=np.zeros((800,800,3),np.uint8)
	# mask=mask_colour.reshape((800,800,1))
	# mask=np.repeat(mask,3,-1)
	# print(mask.shape)
	hulls=[]
	min_dist=1e6
	for cnt in contours :
		if 1e2<cv2.contourArea(cnt)<1e6 :
			# cv2.drawContours(mask,[cnt],0,(0,255,0),3)
			hull=cv2.convexHull(cnt)
			# r=input()
			M=cv2.moments(hull)
			rect=cv2.minAreaRect(hull)
			(x,y),(h,w),theta=rect
			# area=cv2.contourArea(hull)
			# print(1.0*h/w)
			# if abs(1.0*h/w-1.5)>0.5 and abs(1.0*w/h-0.67)>0.2 :
				# continue
			if 1.0*abs(h*w-M['m00'])/(h*w)<0.05:
				bx=final_m['m10']/final_m['m00']
				by=final_m['m01']/final_m['m00']
				mx=M['m10']/M['m00']
				my=M['m01']/M['m00']
				dist=(bx-mx)**2+(by-my)**2
				if dist<min_dist :
					mod=rect
					min_dist=dist
				# return [True,hull]
				# cv2.drawContours(mask,[hull],0,(0,255,0),3)
				# cv2.imshow('mask',mask)
				# cv2.waitKey(0)
				i+=1 
	print(i,'\n')
	if i==0 :
		return [False,0]
	else :
		return [True,brd,mod]
	# print(i)
	# mask=np.zeros_like(mask_colour)

	# cv2.imshow('mask',mask)
	# cv2.imshow('org',mask_colour)
	# cv2.waitKey(50)


if __name__=='__main__':
	# filenames=glob.glob('4/*.jpg')
	t=0
	n=0
	cap=cv2.VideoCapture('../../videos/video10.avi')
	writer=cv2.VideoWriter('../../videos/result_mask10_close_approx.avi',cv2.VideoWriter_fourcc(*'MJPG'),2,(512,512))
	m=0
	while True :
		ret,img=cap.read()
		if not ret:
			break
		# img=cv2.imread(f)
		# print(img.shape)
		tic=tm()
		res=detect(img)
		# print('l'+str(len(res)))
		toc=tm()
		if res[0]:
			cv2.drawContours(img,[res[1]],0,(0,0,255),3)
			# cv2.drawContours(img,[np.int0(cv2.boxPoints(res[1]))],0,(0,0,255),3)
			# cv2.drawContours(img,[np.int0(cv2.boxPoints(res[2]))],0,(0,255,0),3)
			m+=1
		# print(img.shape)
		f=cv2.resize(res[2],(512,512))
		writer.write(f)
		cv2.imshow('mask',f)
		cv2.imshow('img',img)
		cv2.waitKey(30)
		t+=(toc-tic)
		n+=1
	print(1.0*n/t)
	print(m/n)
	writer.release()