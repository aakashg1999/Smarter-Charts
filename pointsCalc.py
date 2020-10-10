import cv2
import numpy as np
import math
import statistics
import time
import pdb


def setup(ref_vector,CpPoint,li_x3y3,img_name):
    origin=CpPoint
    ref_vec=ref_vector
    li=[]
    img = cv2.imread(img_name)
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

    def dist(x1,y1,x2,y2):
        x_dist=(x1-x2)
        y_dist=(y1-y2)
        t_dist=math.hypot(x_dist,y_dist)
        return t_dist
    for try_pt in li_x3y3:
        distance=dist(origin[0],origin[1],try_pt[0],try_pt[1])
        li.append(distance)
        
    li2=sorted(li_x3y3,key=clockwiseangle_and_distance)

    angle_li=[]
    final_li=[]
    for i in range(len(li2)):
        next_pt=(i+1)%len(li2)
        len_pts=math.hypot((li2[i][0]-li2[next_pt][0]),(li2[i][1]-li2[next_pt][1]))
        angle=2*(math.asin(len_pts/(2*statistics.mean(li))))
        angle_li.append(math.degrees(angle))
        y_avg=int(li2[i][1]+li2[next_pt][1])/2.2
        x_avg=int(li2[i][0]+li2[next_pt][0])/2.2
        #print(li2[i])
        print(x_avg,y_avg, img[int(y_avg)][int(x_avg)])
        final_li.append(img[int(y_avg)][int(x_avg)])
    print(angle_li)
    sum_angle=0
    for angle in angle_li:
        sum_angle+=angle
    return sum_angle,angle_li,final_li

'''
start=time.time()
radius_check=6
white_px=[255,255,255]
black_px=[0,0,0]

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

corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 30)
corners = np.int0(corners)

new_corner=[]
for corner in corners:
    x,y = corner.ravel()
    #print(corner[0])
    new_corner.append([x,y])
    cv2.circle(img,(x,y),6,255,-1)

#dist_matrix=centre_point(new_corner)
##i=len(new_corner)-2
##print(new_corner[i],new_corner[11])
##for j in range(len(new_corner)):
##    print(dist_matrix[i][j])



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

li2=sorted(pts,key=clockwiseangle_and_distance)
print(li2)


#print(img[197,240])
d1=dist(197,240,62,177)
d2=dist(197,240,70,320)
d3=dist(197,240,197,91)
d4=dist(197,240,346,255)
li=[d1,d2,d3,d4]
print(li)
#print(statistics.mean(li))


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
'''
