import cv2
import numpy as np
import math
import statistics
import time
    
def check_whity_blacky(x1,y1,img):
    try:
        px=img[int(y1)][int(x1)]
        whity,blacky=False,False
        if px[0]<=100 and px[1]<=100 and px[2]<=100:
            blacky=True
        if px[0]>=210 and px[1]>=210 and px[2]>=210:
            whity=True
        if whity or blacky:
            return True
        return False
    except:
        return True
    
        
def solve_y(r2,r,x1,y1,xminusxsq2,xminusxsq5):
    yminusysq2=r2-xminusxsq2
    yminusysq5=r2-xminusxsq5
    d2=(((-2)*y1)*((-2)*y1))-4*((y1*y1)-yminusysq2)
    d5=(((-2)*y1)*((-2)*y1))-4*((y1*y1)-yminusysq5)
    if d2 >= 0:
        root21=((2*y1)+math.sqrt(d2))/2
        root22=((2*y1)-math.sqrt(d2))/2
    if d5 >= 0:
        root51=((2*y1)+math.sqrt(d5))/2
        root52=((2*y1)-math.sqrt(d5))/2
    return[[x1+2,root21],[x1+2,root22],[x1+r-1,root51],[x1+r-1,root52],
           [x1-2,root21],[x1-2,root22],[x1-r+1,root51],[x1-r+1,root52]]

def calculate_diff_colors(x1,y1,r,img_name):
    img = cv2.imread(img_name)
    #px_point=img[y1][x1]
    r2=r*r
    #((x1+2)-x1)*((x1+2)-x1)
    xminusxsq2=4
    #((x1+r-1)-x1)*((x1+r-1)-x1)
    xminusxsq5=(r-1)*(r-1)
    li_xy=solve_y(r2,r,x1,y1,xminusxsq2,xminusxsq5)
    li_colors=[]
    for i in range(8):
        w_or_b=check_whity_blacky(li_xy[i][0],li_xy[i][1],img)
        if w_or_b is False:
            px_point=img[int(li_xy[i][1])][int(li_xy[i][0])]
            color_match=False
            for color in li_colors:
                if color[0]==px_point[0] and color[1]==px_point[1] and color[1]==px_point[1]:
                    color_match=True
            if color_match is False:
                li_colors.append(px_point)
    return li_colors,len(li_colors)

def setup(img_name,rad):        
    start=time.time()
    img = cv2.imread(img_name)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    row,col,channels=img.shape
    #pdb.set_trace()

    r=rad
    
    if row>1000 and col>1000:
        r=10

    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 30)
    corners = np.int0(corners)

    new_corner=[]
    for corner in corners:
        x,y = corner.ravel()
        #print(corner[0])
        new_corner.append([x,y])
        cv2.circle(img,(x,y),6,255,-1)

    len_colors=[]
    li_colors=[]
    for corner in new_corner:
        li,leng=calculate_diff_colors(corner[0],corner[1],r,img_name)
        len_colors.append(leng)
        li_colors.append(li)
    max_colors=len_colors.index(max(len_colors))

    
    cv2.circle(img,(new_corner[max_colors][0],new_corner[max_colors][1]),6,[0,0,255],-1)
    end=time.time()
    return(new_corner[max_colors][0],new_corner[max_colors][1])
