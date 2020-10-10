import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
from math import hypot
import pdb

def setup(img_name,Centre,Radius):
    img = cv2.imread(img_name)
    CpPoint=Centre
    rad=Radius
    rad10pct=int(rad*0.2)
    #pts=[[CpPoint[0]-rad10pct,CpPoint[1]+rad10pct],[CpPoint[0]+rad10pct,CpPoint[1]+rad10pct],[CpPoint[0]+rad10pct,CpPoint[1]-rad10pct],[CpPoint[0]-rad10pct,CpPoint[1]-rad10pct]]

    
    def color_checking(li,check_point):
        px=img[check_point[1]][check_point[0]]
        for ele in li:
            if ele[0]==px[0] and ele[1]==px[1] and ele[2]==px[2]:
                return False 
        li.append(px)
        #li_pts.append(check_point)
        #print(check_point)
        return True
        
    def check_edge(check_point,check_var):
        if check_var is 0:
            pxm2=img[check_point[1]-3][check_point[0]]       
            px=img[check_point[1]][check_point[0]]
            pxp2=img[check_point[1]+3][check_point[0]]
            if pxp2[0]==px[0] and pxp2[1]==px[1] and pxp2[2]==px[2]:
                    return False
            if pxm2[0]==px[0] and pxm2[1]==px[1] and pxm2[2]==px[2]:
                    return False
            return True
        
        if check_var is 1:
            pxm2=img[check_point[1]][check_point[0]-3]
            px=img[check_point[1]][check_point[0]]
            pxp2=img[check_point[1]][check_point[0]+3]
            if pxp2[0]==px[0] and pxp2[1]==px[1] and pxp2[2]==px[2]:
                    return False
            if pxm2[0]==px[0] and pxm2[1]==px[1] and pxm2[2]==px[2]:
                    return False
            return True
        
       
    '''
    cv2.circle(img,(pts[0][0],pts[0][1]),7,[0,0,255],-1)
    cv2.circle(img,(pts[1][0],pts[1][1]),7,[0,0,255],-1)
    cv2.circle(img,(pts[2][0],pts[2][1]),7,[0,0,255],-1)
    cv2.circle(img,(pts[3][0],pts[3][1]),7,[0,0,255],-1)
    cv2.imshow("naam",img)
    '''
    
    li=[]
    li_pts=[]
    li_edge=[]
    for i in range(4):
        pts=[[CpPoint[0]-rad10pct,CpPoint[1]-rad10pct],[CpPoint[0]+rad10pct,CpPoint[1]-rad10pct],[CpPoint[0]+rad10pct,CpPoint[1]+rad10pct],[CpPoint[0]-rad10pct,CpPoint[1]+rad10pct]]
        start=pts[i]
        end=pts[(i+1)%4]
        #print(i , " ", i+1)
        #print(start," ", end)
        
        if start[0] is end[0]:
            
            if (start[1]-end[1]) >=  0:
                temp_pt_start=end
                temp_pt_end=start
            else:
                temp_pt_start=start
                temp_pt_end=end
            while temp_pt_start[1] != temp_pt_end[1]:
                temp_pt_start[1]+=1
                TF=color_checking(li,temp_pt_start)
                if TF is True:
                    TFE=check_edge(temp_pt_start,0)
                    #print(TFE)
                    if TFE is False:
                        li_pts.append([temp_pt_start[0],temp_pt_start[1]])
                        px=img[temp_pt_start[1]][temp_pt_start[0]]
                        li.append(px)
                    elif TFE is True:
                        li_edge.append([temp_pt_start[0],temp_pt_start[1]])
                    #print(li_pts)
        
        else :
            
            if (start[0]-end[0]) >=  0:
                temp_pt_start=end
                temp_pt_end=start
            else:
                temp_pt_start=start
                temp_pt_end=end
            while temp_pt_start[0] != temp_pt_end[0]:
                temp_pt_start[0]+=1
                TF=color_checking(li,temp_pt_start)
                if TF is True:
                    TFE=check_edge(temp_pt_start,1)
                    #print(TFE)
                    if TFE is False:
                        li_pts.append([temp_pt_start[0],temp_pt_start[1]])
                        px=img[temp_pt_start[1]][temp_pt_start[0]]
                        li.append(px)
                    elif TFE is True:
                        li_edge.append([temp_pt_start[0],temp_pt_start[1]])
                    #print(li_pts)
                        
    
    
    
#    print(li)
    print(li_edge)
    for point in li_edge:
        for point2 in li_edge:
            
            if point[0] <= point2[0] and point[0]+2 >= point2[0] :
                if point[1] <= point2[1] and point[1]+2 >= point2[1]:
                    if point[0] is not point2[0] or point[1] is not point2[1]:
                        li_edge.remove(point2)
                        
    #cv2.circle(img,(167,210),4,[255,0,0],-1)
    #cv2.imshow("naam",img)
    #print(li_pts,"      ")
    #print(li_edge,"      ")
#CpPoint x1,y1
    li_x3y3=[]
    
    for point in li_edge:
        try:
            m=(point[1]-CpPoint[1])/(point[0]-CpPoint[0])
            c=((CpPoint[1]*point[0])-(point[1]*CpPoint[0]))/(point[0]-CpPoint[0])
            a=1
            x3deno=1+(m**2)
            x3b=(2*(m*c-CpPoint[1]*m-CpPoint[0]))/x3deno
            x3c=(CpPoint[0]**2+c**2+CpPoint[1]**2-(2*CpPoint[1]*c)-rad**2)/x3deno
            x3disc=((x3b)**2)-4*(x3c)
            if x3disc > 0:
                num_roots = 2
                x31 = (((-x3b) + sqrt(x3disc))/(2*a))     
                x32 = (((-x3b) - sqrt(x3disc))/(2*a))
                #print("There are 2 roots: %f and %f" % (x31, x32))
            elif x3disc == 0:
                num_roots = 1
                x3 = (-x3b) / 2*a
                #print("There is one root: ", x3)
            elif x3disc <0:
                print("Fatal Error")

            if num_roots==2:
                y31=m*x31+c
                y32=m*x32+c
                if hypot(x31-point[0],y31-point[1]) < hypot(x32-point[0],y32-point[1]):
                    x3=x31
                    y3=y31
                else:
                    x3=x32
                    y3=y32
                #print(y31," ",y32)
            elif num_roots==1:
                y3=m*x3+c
            
        except:
            #x1=x2=x3
            x3=CpPoint[0]
            y31=CpPoint[1]+rad
            y32=CpPoint[1]-rad

            if y31-point[1]>y32-point[1]:
                y3=y32
            else:
                y3=y31       
        li_x3y3.append([x3,y3])

    '''
    for try_pt in li_edge:
        #print(try_pt)
        cv2.circle(img,(int(try_pt[0]),int(try_pt[1])),2,[0,0,255],-1)
    
    for try_pt in li_x3y3:
        #print(try_pt)
        cv2.circle(img,(int(try_pt[0]),int(try_pt[1])),2,[0,0,255],-1)
    cv2.imshow("naam",img)
    '''
    return(li_x3y3,li_edge,li_pts,li)





















    
