import operator
from TheBrickModel import *

'''
This module provides the functionality for comparison between 2 wall objects,
'''
#compair function
def status_comparison(a,b):
     bricks=a.bricks
     bricks2=b.bricks 
 
     for q in range (len(bricks2)):
          
          i1= max(bricks,key=lambda Brick:Brick.newP) #take maximam position in a
          n1=i1.newP
         
          i2= max(bricks2,key=lambda Brick:Brick.newP)#take maximum position in b
          n2=i2.newP
          if bricks[q].brNo ==bricks2[q].brNo and n1== n2: #compair with brick numbers in wall and last position of brick in wall
              f='wall is complete'
              i3= max(bricks2,key=lambda Brick:Brick.newP)
              n3=i3.newP
              bricks2[q].newP= n3
              print('last position of first wall',n2)
              print('last position of second wall',n3)
          else:
              f='wall is not complete'
              if  bricks2[q].brickInRowNo==0:
               i3= max(bricks2,key=lambda Brick:Brick.newP)#if the raw complete start new raw
               n3=i3.newP[1]  
               bricks2[q].newP=(0,n3+BRICK_SEPERATION,0)#x=0, cause it is the start of wall which =0, and (y=old y+BRICK_SEPERATION)
               print('new position in new raw',n3)
              else:
                i1= max(bricks,key=lambda Brick:Brick.newP)
                n1=i1.newP
                i3= max(bricks2,key=lambda Brick:Brick.newP)#if the raw not complete ,get next position of the brick
                n3=i3.newP
                bricks2[q].newP=(n3[0]+BRICK_SEPERATION+BRICK_LENGTH,n3[1],0)
                print('last position of larger wall',n1)
                print('last position of smaller wall',n3)
          return  f,'new position',bricks2[q].newP

#must equal in hight and different in width
    #testing:
#a= Wall(hight=1,width=2)
#b= Wall(hight=1,width=2)
#z=status_comparison(a,b)
#print ((z))

##note .. assumed that bricks2 is smaller than bricks if they are not equal
