import cv2
import numpy as np
import TheBrickModel as model
from _3DVisualization import *
import cv2

def avergefunc (img):
  

     temp=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
     temp = cv2.GaussianBlur(temp, (9, 9), 0)
     #temp = cv2.GaussianBlur(temp, (9, 9), 0)
     gray1 = cv2.GaussianBlur(temp, (5, 5), 0)
     blur1 = cv2.medianBlur(gray1, 9)
     im = cv2.GaussianBlur(blur1, (5, 5), 0)
    
     for i in range(len( im)):
       for j in range(len( im[1])):
           im[i][j] = 255 if im[i][j] >=110 else 0

     return  im


def rectAroundBrick (contours, img):
        '''
        This function takes the contours of an image as input,
        draws rectangles around them,
        saves the points used to calculate the rects in Brick objects,
        creates Wall object of them
        '''
        idx=0
        bricks = []      # better defined here or global?
        for cnt in contours:
                xList = [x[0][0] for x in cnt]
                yList = [x[0][1] for x in cnt]
                x_min= min(xList)
                x_max= max (xList)
                y_min = min (yList)
                y_max= max (yList)
                
                #if len(cnt)>30 and len(cnt)<70:
                cv2.rectangle(img,(x_min,y_max),(x_max,y_min),(0,255,255),3)
                roi=img[y_min:y_max,x_min:x_max]
                if y_max-y_min >=50 and x_max- x_min >=50:
                     roi= cv2.resize(roi,(50,50))
                     roi = roi.reshape(1,50,50,3)
                     #print(classifier.predict_classes(roi))
                     #if classifier.predict_classes(roi)== 1:
                     bricks.append(model.Brick(p1= (x_min,y_min),p2= (x_max,y_max)))
                          #print(bricks[-1].p1,bricks[-1].p2)
                #cv2.imwrite('new non_brick' + str(65+idx) + '.jpg', roi)
        #print (bricks)
                          
        wall = model.Wall(Bricks=bricks)
        #cv2.imshow("output",img)
        #cv2.waitKey(0)
        wall.walldescriptor()
        #draw3Dwall(wall)
        return wall



def img_analyzor(img_bath):
     '''
     this function pre_processes the wall image to find contours
     calls the function rectAround bricks and
     give it the contours to handle the rest
     '''
     alpha = float (1)     # Simple contrast control
     beta = int (100)
     img = cv2.imread(img_bath)
     mul_img = cv2.multiply(img, np.array([alpha]))                    # mul_img = img*alpha
     img1 = cv2.add(mul_img, beta)
     img2=avergefunc(img1)
     kernel = np.ones((13, 13),np.uint8)
     erosion = cv2.morphologyEx(img2, cv2.MORPH_ERODE, kernel, iterations = 1)
     # create binary image
     gray1 = cv2.GaussianBlur(img2, (5, 5), 0)
     blur1 = cv2.medianBlur(gray1, 9)
     blur2 = cv2.GaussianBlur(blur1, (5, 5), 0)
     blur3 = cv2.medianBlur(blur2, 9)
     blur4 = cv2.GaussianBlur(blur3, (5, 5), 0)
     blur5 = cv2.medianBlur(blur4, 9)
     edge=cv2.Canny(erosion,50,60)

     r, thresholded= cv2.threshold(edge,0,250, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)

     #using bilateral Filter
     blur = cv2.bilateralFilter(thresholded,9,75,75)
     t, binary = cv2.threshold(blur,127, 255, cv2.THRESH_BINARY)

     # find contours
     (_, contours, _) = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, 
         cv2.CHAIN_APPROX_SIMPLE)

     # find the length of contours and store them an an array:
#      lengthsOfConts=[]
#      longcontours=[]
#      for (i, c) in enumerate(contours):
#              if len(c)>30:
#                      longcontours.append(c)
#                      lengthsOfConts.append(len(c))


     #draw the contours on the image:
     return rectAroundBrick(contours,img)