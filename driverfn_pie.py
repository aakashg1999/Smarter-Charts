import CentreDetect as CD
import RadiusCalc as RD
import cv2
import totalColors as tC
import pointsCalc as PC
import pdb
import xlsxwriter


def setup(img_name,Output_Name):
    li=[]
    li_pts=[]
    li_edge=[]
    li_x3y3=[]

    Cpoints=CD.setup(img_name,7)
    Radius=RD.setup(img_name,10,Cpoints,6)

    #pdb.set_trace()
    #li_x3y3,li_edge,li_pts,li=tC.setup(img_name,[197,240],157)
    li_x3y3,li_edge,li_pts,li=tC.setup(img_name,[Cpoints[0],Cpoints[1]],Radius)
    img=cv2.imread(img_name)
    sum_angle,angle_li,final_li=PC.setup([0,1],Cpoints,li_x3y3,img_name)
    #print(sum_angle)
    cv2.circle(img,(Cpoints[0],Cpoints[1]),6,[0,0,255],-1)
    cv2.circle(img,(Cpoints[0]+Radius,Cpoints[1]),6,[0,0,255,-1])
    for try_pt in li_x3y3:
        cv2.circle(img,(int(try_pt[0]),int(try_pt[1])),2,[0,0,255],-1)
    #cv2.imshow('h',img)

    def clamp(x): 
      return max(0, min(x, 255))

    workbook = xlsxwriter.Workbook(Output_Name)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('C:C', 30)
    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 15)
    j=2
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Color of Segment', bold)
    worksheet.write('B1', '%age Value', bold)
    worksheet.write('C1', 'Image with Markings', bold)
    for i in range(len(final_li)):
        cell_format = workbook.add_format()
        cell_format.set_bg_color("#{0:02x}{1:02x}{2:02x}".format(clamp(final_li[i][2]), final_li[i][1], final_li[i][0]))
        worksheet.write('A'+str(j), 'Color', cell_format)
        temp="{:.2f}".format((angle_li[i]/360)*100)
        worksheet.write('B'+str(j), str(temp)+str("%"))
        j+=1
    j+=1    
    worksheet.write('B'+str(j), 'Sum of Angles', bold)
    j+=1
    worksheet.write('B'+str(j),str(sum_angle)+" Degrees" , bold)
    cv2.imwrite("PIE.png", img)
    worksheet.insert_image('C2', "PIE.png", {'x_offset': 15, 'y_offset': 10})
    workbook.close()
    return True    

