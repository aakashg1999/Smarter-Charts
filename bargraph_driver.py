import cv2
import numpy as np
import math
import statistics
import time
import pdb
import xlsxwriter

def Setup(Image_Name,Output_Name):
    start=time.time()

    img = cv2.imread(Image_Name)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    row,col,channels=img.shape
    #print(row,col,channels)
    bgcolor=img[row-1][col-1]
    bgpoint=[col-1,row-1]

    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 30)
    corners = np.int0(corners)

    '''
    #for visualization
    for corner in corners:
        x,y = corner.ravel()
        #print(corner[0])
        cv2.circle(img,(x,y),3,(255,0,0),-1)

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    #step0 :- sort corners according to x and y coordinates
    new_corner=[]
    for corner in corners:
        x,y = corner.ravel()
        #print(corner[0])
        new_corner.append([x,y])
    #print(new_corner[0])
    #for x co ordinates in increasing

    def check_range(y1,y2):
        if y2 == y1:
            return True
        elif y2 == y1+1:
            return True
        elif y2 == y1-1:
            return True
        else :
            return False

    def check_range_2(x1,x2):
        if x2 == x1:
            return True
        elif x2 == x1+2:
            return True
        elif x2 == x1-2:
            return True
        else :
            return False

    new_corner_x=new_corner

    def sort_x():
        for j in range(len(new_corner)-1):
            for i in range(len(new_corner)-j-1):
                if new_corner_x[i][0]>new_corner_x[i+1][0]:
                    new_corner_x[i],new_corner_x[i+1]=new_corner_x[i+1],new_corner_x[i]
    #print(new_corner_x)
    #for y co ordinates in non decreasing
    for j in range(len(new_corner)-1):
        for i in range(len(new_corner)-j-1):
            if new_corner[i][1]<new_corner[i+1][1]:
                new_corner[i],new_corner[i+1]=new_corner[i+1],new_corner[i]
    #print(new_corner)
    #--------------------------------------------------------------
    #step1- detecting x axis

    list_possibility=[]
    j=0

    #gathering list of possibility
    while j<len(new_corner)-1:
        within_range=check_range(new_corner[j][1],new_corner[j+1][1])
        #print(within_range," " ,new_corner[j][1] )
        if within_range:
                temp=0
                i=j
                while within_range:
                    i=i+1
                    try:
                        within_range=check_range(new_corner[j][1],new_corner[i+1][1])
                        temp+=1
                    except IndexError:
                        break
                    
                list_possibility.append([new_corner[j][1],temp+1])
                j=j+temp+1
        else:
            j+=1

    #sorting list of possibility
    for j in range(len(list_possibility)-1):
        for i in range(len(list_possibility)-j-1):
            if list_possibility[i][1]<list_possibility[i+1][1]:
                list_possibility[i],list_possibility[i+1]=list_possibility[i+1],list_possibility[i]
    #print(list_possibility)
    #---------------------------------------------------------------
    #step2 : detect vertical point of a bar
    #print(new_corner_x)
    y_coordinate=list_possibility[0][0]
    frequency=list_possibility[0][1]
    i=0

    while new_corner[i][1] != y_coordinate:
        i+=1
            
    list_x_axis=[]
    for j in range(0,frequency):
        within_range=check_range(y_coordinate,new_corner[i+j][1])
        if within_range:
            list_x_axis.append(new_corner[i+j])
            
    #print(list_x_axis)
    #print(list_x_axis)
    if len(list_x_axis)==frequency:
        sort_x()

    verify_x_axis=False
        #print(new_corner_x)

    for point in list_x_axis:
        for i in range(len(new_corner_x)):
            if point == new_corner_x[i]:
        
                    if i==(len(new_corner_x)-2):
                        within_range=check_range_2(point[0],new_corner_x[i+1][0])
                        if within_range is True:
                            verify_x_axis=True
                            verification_point=[point,new_corner_x[i+1]]
                            break
                    elif i<(len(new_corner_x)-2) and i>=0:
                        within_range=check_range_2(point[0],new_corner_x[i+1][0])
                        within_range_2=check_range_2(point[0],new_corner_x[i+2][0])
                        if within_range != within_range_2 :
                            verify_x_axis=True
                            verification_point=[point,new_corner_x[i+1]]                      
                            break
                        
    #print(verification_point)
    '''
    for corner in verification_point:
        x,y = corner[0],corner[1]
        #print(corner[0])
        cv2.circle(img,(x,y-3),3,(255,0,0),-1)
        
        print(img[y-2][x-4])
        print(img[y+2][x-5])
        print(img[y-2][x+5])
        print(img[y+2][x+4])
    '''         

    #-----------------------------------------------------------
    #step4 : horizontal scanning 3px over x axis
        #y_gap is gap above x-axis
    def x_scanner(y_gap,x_axis_pt,col,bgcolor):
        i=col-1
        y_cood=x_axis_pt[1]-y_gap
        Dict_colors={}
        li_colors=[]
        while i>0:
            if(color_match(bgcolor,img[y_cood][i])) is False:
                
                temp=i
                #pdb.set_trace()
                
                while(color_match(img[y_cood][temp],img[y_cood][i])) is True:
                    i-=1
                if temp != i+1 and temp-i-1 !=1:
                    li_colors.append(img[y_cood][temp])
                    #print(img[y_cood][i])
                    Dict_colors[len(li_colors)-1]=[i+1,temp,temp-i-1]
                    
            else:
                i-=1
        return Dict_colors,y_cood,li_colors
        
    def color_match(color1,color2):
        if color1[0]==color2[0]:
            if color1[1]==color2[1]:
                if color1[2]==color2[2]:
                    return True
        return False

    x_axis_pt= verification_point[:][0]

    dictionary,y_cood,li_colors=x_scanner(3,x_axis_pt,col,bgcolor)
    #print(dictionary)
    #print(len(li_colors))
    #------------------------------------------------
    #step 5 : Determinig horizontal length of a bar and bars
    t_li=[]
    temp_li=[]
    temp_li_count=[]
    for i in range(0,len(li_colors)):
        t_li.append(i)
        
    for i in range(0,len(li_colors)):
        if i in t_li:
            count=0
            temp=dictionary[i][2]
            t_li.remove(i)
            
            for j in range(0,len(li_colors)):
                if j!= i:
                    if check_range_2(temp,dictionary[j][2]) or check_range(temp,dictionary[j][2]) is True:
                        count+=1
                        #print(temp,dictionary[j][2])
                        t_li.remove(j)

            temp_li.append(i)
            temp_li_count.append(count)

    #for i in range(0,len(temp_li)):

    idx=temp_li_count.index(max(temp_li_count))
    count=temp_li_count[idx]
    temp_li_count.remove(temp_li_count[idx])

    main_idx=idx
    dic_idx=temp_li[idx]
    thick=dictionary[dic_idx][2]

    #print(dictionary)
    #print(thick)
    #print(li_colors)
    #---------------------
    #step6: calculate vertical height
    final_dict={}
    def vertical_height(x_axis_row,color_bar,cood_bar_col,y_gap):
        point_axis=[cood_bar_col,x_axis_row]
        #pdb.set_trace()
        for i in range(0,y_gap+1):
            #print(img[x_axis_row-i][cood_bar_col])
            if color_match(img[x_axis_row-i][cood_bar_col],color_bar) is True:
                count=0
                while color_match(img[x_axis_row-i-count][cood_bar_col],color_bar) is True :
                    count +=1
                return count
        return 0

    x_axis_cood=verification_point[:][0]
    x_axis_cood=x_axis_cood[1]
    for i in dictionary.keys():
        #check thickness and create final dict
        #if dictionary[i]
        
        if check_range(thick,dictionary[i][2]) or check_range_2(thick,dictionary[i][2]) is True:
            avg=int((dictionary[i][1]+dictionary[i][0])/2)
            count=vertical_height(x_axis_cood,li_colors[i],avg,3)
            #print(dictionary[i],li_colors[i],count, x_axis_cood)
            final_dict[i]=[dictionary[i][0],dictionary[i][1],dictionary[i][2],count]
    #print(final_dict)

    #------------------------
    #step 7: image edit and export

    def clamp(x): 
      return max(0, min(x, 255))



    workbook = xlsxwriter.Workbook(Output_Name)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('C:C', 30)
    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 15)

    j=2

    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Color of Bar', bold)
    worksheet.write('B1', 'Height in px', bold)
    worksheet.write('C1', 'Image with Markings', bold)

    for i in final_dict.keys():
        
        cell_format = workbook.add_format()
        cell_format.set_bg_color("#{0:02x}{1:02x}{2:02x}".format(clamp(li_colors[i][2]), li_colors[i][1], li_colors[i][0]))
        worksheet.write('A'+str(j), 'Color', cell_format)
        x_li=[final_dict[i][0],final_dict[i][1]]
        y_li=[x_axis_cood,x_axis_cood-final_dict[i][-1]]
        #print(verification_point,verification_point[1][1] )
        for x in x_li:
            for y in y_li:
                cv2.circle(img,(x,y),3,(0,0,0),-1)

        worksheet.write('B'+str(j), final_dict[i][-1])
        j+=1

    j+=1    
    worksheet.write('B'+str(j), 'Row x Column', bold)
    j+=1
    worksheet.write('B'+str(j), str(row)+" x "+str(col), bold)

    cv2.imwrite("Bar.png", img)
    worksheet.insert_image('C2', "Bar.png", {'x_offset': 15, 'y_offset': 10})
    workbook.close()
    '''
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return True


