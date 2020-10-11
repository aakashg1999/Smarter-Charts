import cv2
import numpy as np
import math
import statistics
import time

start=time.time()

def dist(x1,y1,x2,y2):
    x_dist=(x1-x2)
    y_dist=(y1-y2)
    t_dist=math.hypot(x_dist,y_dist)
    return t_dist

img = cv2.imread('Download.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

row,col,channels=img.shape
#print(row,col,channels)
'''
final_i,final_j=0,0
for i in range(row):
    for j in range(col):
        if img[i,j] is not [255,255,255]:
            print(img[i,j])

        if img[i,j] is not [255,255,255] and not [0,0,0]:
            final_i,final_j=i,j
            print(img[final_i,final_j])
            break
'''

        

corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 30)
corners = np.int0(corners)

for corner in corners:
    x,y = corner.ravel()
    #print(corner[0])
    cv2.circle(img,(x,y),6,255,-1)

cv2.circle(img,(197,240),7,[0,0,255],-1)
cv2.circle(img,(62,177),7,[0,0,255],-1)
cv2.circle(img,(70,320),7,[0,0,255],-1)
cv2.circle(img,(197,91),7,[0,0,255],-1)
cv2.circle(img,(346,255),7,[0,0,255],-1)

#centre of the circle
origin=[197,240]

#ref vector can be any 1 point on circumference
ref_vec=[0,1]

pts=[[70,320],[197,91],[346,255],[62,177]]

def clockwiseangle_and_distance(point):
    vector=[point[0]-origin[0],point[1]-origin[1]]
    lenvector=math.hypot(vector[0],vector[1])
    if lenvector==0:
        return -math.pi,0
    normalized=[vector[0]/lenvector,vector[1]/lenvector]
    dotprod=(ref_vec[0]*normalized[0])+(ref_vec[1]*normalized[1])
    diffprod=(ref_vec[0]*normalized[1])-(ref_vec[1]*normalized[0])
    angle=math.atan2(diffprod,dotprod)
    if angle<0:
        return 2*math.pi+angle,lenvector
    return angle,lenvector

li2=sorted(pts,key=clockwiseangle_and_distance)
print(li2)


#print(img[197,240])
d1=dist(197,240,62,177)
d2=dist(197,240,70,320)
d3=dist(197,240,197,91)
d4=dist(197,240,346,255)
li=[d1,d2,d3,d4]
print(statistics.mean(li))


angle_li=[]

for i in range(len(li2)):
    next_pt=(i+1)%len(li2)
    len_pts=math.hypot((li2[i][0]-li2[next_pt][0]),(li2[i][1]-li2[next_pt][1]))
    angle=2*(math.asin(len_pts/(2*statistics.mean(li))))
    angle_li.append(math.degrees(angle))

print(angle_li)
sum_angle=0
for angle in angle_li:
    sum_angle+=angle
print(sum_angle)
cv2.imshow('Corner',img)
end= time.time()
print("time take is :", end-start)


