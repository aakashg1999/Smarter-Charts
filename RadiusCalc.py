import cv2
import numpy as np
import math
import statistics
import time
import pdb


start=time.time()
def color_check(color_check_pts,x,y,img_name):
    img=cv2.imread(img_name)
    
    px_img=img[y][x]
    for li_check in color_check_pts:
        if px_img[0]==li_check[0] and px_img[1]==li_check[1] and px_img[2]==li_check[2]:
            return True
        
    return False
    
def solve_y(r,x1,y1):
    r2=r*r
    xminusxsq5=(r-1)*(r-1)
    yminusysq5=r2-xminusxsq5
    d5=(((-2)*y1)*((-2)*y1))-4*((y1*y1)-yminusysq5)
    if d5 >= 0:
        root51=((2*y1)+math.sqrt(d5))/2
        root52=((2*y1)-math.sqrt(d5))/2
    return[[x1+r-1,int(root51)],[x1+r-1,int(root52)],
           [x1-r+1,int(root51)],[x1-r+1,int(root52)]]

def setup(img_name,step,Cenpoints,radius):
    img=cv2.imread(img_name)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    #cv2.circle(img,(Cenpoints[0],Cenpoints[1]),2,[0,0,255],-1)
    check_pts=solve_y(radius,Cenpoints[0],Cenpoints[1])
    
    color_check_pts=[]
    for pts in check_pts:
        temp=img[pts[1]][pts[0]]
        color_check_pts.append(temp)

    rad=True
    
    while rad:
        radius+=step
        T_F_color=[]
        temp_pts=solve_y(radius,Cenpoints[0],Cenpoints[1])
        for pts in temp_pts:
            T_F_color.append(color_check(color_check_pts,pts[0],pts[1],img_name))
        
        T_F_T=False
        for T_F in T_F_color:
            T_F_T= T_F_T or T_F
        rad=rad and T_F_T
        
    '''
    if radius > step:
        radius-=2*step
    rad=True
    T_F_color=[]
    for i in range(0,step,1):
        T_F_color=[]
        temp_pts=solve_y(radius,Cenpoints[0],Cenpoints[1])
        for pts in temp_pts:
            T_F_color.append(color_check(color_check_pts,pts[0],pts[1],img_name))

        T_F_T=False
        for T_F in T_F_color:
            T_F_T= T_F_T or T_F
        rad=rad and T_F_T
        if rad is False:
            break
        radius+=1
    '''
    return radius


