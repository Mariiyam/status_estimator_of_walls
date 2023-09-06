'''
This module represents the structre of the objects we use: the wall and the brick classes
'''

# brick dimensions in cm:
BRICK_LENGTH = 20   # x direction
BRICK_WIDTH = 12.5  # z direction
BRICK_DEPTH = 7.5   # y direction
BRICK_SEPERATION = 0.5 # x & y direction
delta = 20        # accuracy range of the rectangles drawn around the brick


def brickVertices(bricks):
        for brick in bricks:
                 vertices =(
            (brick.newP[0],brick.newP[1],brick.newP[2]),
            (brick.newP[0]+brick.BRICK_LENGTH,brick.newP[1],brick.newP[2]),
            (brick.newP[0],brick.newP[1],brick.newP[2]+brick.BRICK_WIDTH),
            (brick.newP[0]+brick.BRICK_LENGTH,brick.newP[1],brick.newP[2]+brick.BRICK_WIDTH),
            (brick.newP[0],brick.newP[1]+brick.BRICK_DEPTH,brick.newP[2]),
            (brick.newP[0]+brick.BRICK_LENGTH,brick.newP[1]+brick.BRICK_DEPTH,brick.newP[2]),
            (brick.newP[0],brick.newP[1]+brick.BRICK_DEPTH,brick.newP[2]+brick.BRICK_WIDTH),
            (brick.newP[0]+brick.BRICK_LENGTH,brick.newP[1]+brick.BRICK_DEPTH,brick.newP[2]+brick.BRICK_WIDTH)
            )
                 print (vertices)


def clustering_raws(bricks, maxgap):
    bricksWithRaws= []
    i=1
    bricks[0].rawNo = 1
    groups = [[bricks[0]]]
    for brick in bricks[1:]:
        if abs(brick.p1[1] - groups[-1][-1].p1[1]) <= maxgap:
            brick.rawNo= groups[-1][-1].rawNo
            groups[-1].append(brick)
        else:
            brick.rawNo = groups[-1][-1].rawNo + 1
            groups.append([brick])
    # to calculate newp and brick dimensions:    
    for raw in range(len(groups)):
            if (raw+1)%2==0:       
                for i in range (len(groups[raw])):
                    #print(i)
                    groups[raw][i].brickInRowNo = i+1
                    groups[raw][i].BRICK_WIDTH= BRICK_WIDTH
                    groups[raw][i].BRICK_DEPTH = BRICK_DEPTH
                    if i==0: 
                        groups[raw][i].BRICK_LENGTH = BRICK_LENGTH/2
                        groups[raw][i].bd = (BRICK_LENGTH/2,BRICK_DEPTH,BRICK_WIDTH)
                        groups[raw][i].newP = (0,(BRICK_DEPTH+BRICK_SEPERATION)*(raw),0)
                        #print(groups[raw][i].BRICK_LENGTH)
                    #here was the code: the last brick is half#    
                        
                    else:
                        groups[raw][i].BRICK_LENGTH = BRICK_LENGTH
                        groups[raw][i].bd = (BRICK_LENGTH, BRICK_DEPTH,BRICK_WIDTH)
                        groups[raw][i].newP = ((i-1)*(BRICK_LENGTH+ BRICK_SEPERATION)+BRICK_LENGTH/2+BRICK_SEPERATION,(BRICK_DEPTH+BRICK_SEPERATION)*(raw),0)
                        #groups[raw][i].newP = ((groups[raw][i-1].newP[1])+ (groups[raw][i-1].BRICK_LENGTH) + (BRICK_SEPERATION),(BRICK_DEPTH+BRICK_SEPERATION)*(raw),0)
                        #print(groups[raw][i].BRICK_LENGTH)
                         
            else:        
                for i in range (len(groups[raw])):
                    groups[raw][i].brickInRowNo = i+1
                    groups[raw][i].BRICK_LENGTH = BRICK_LENGTH
                    groups[raw][i].BRICK_WIDTH= BRICK_WIDTH
                    groups[raw][i].BRICK_DEPTH = BRICK_DEPTH
                    groups[raw][i].bd = (BRICK_LENGTH, BRICK_DEPTH,BRICK_WIDTH)
                    if i==0:
                        groups[raw][i].newP = (0,(BRICK_DEPTH+BRICK_SEPERATION)*(raw),0)
                        #print(groups[raw][i].BRICK_LENGTH)
                    else:
                        groups[raw][i].newP = ((i)*(BRICK_LENGTH+ BRICK_SEPERATION),(BRICK_DEPTH+BRICK_SEPERATION)*(raw),0)
                        #print(groups[raw][i].BRICK_LENGTH)
                        
                    
                            
    maxNumberofRaws = len(groups)
    
    for sub_bricks in groups:
            for brick in sub_bricks:
                    bricksWithRaws.append(brick)
    return bricksWithRaws, maxNumberofRaws


def wall_model_builder1(wall):
    #wall.walldescriptor()
    bricks= wall.bricks
    bricks =sorted(bricks, key=lambda Brick: (Brick.p1[1],Brick.p1[0]),reverse = True)

 # to obtain the raw numbers, dimensions, the number of brick in the raw, and 3D points for each brick:
    bricks, maxNumberofRaws = clustering_raws(bricks, delta)


# to obtain the brick ID 
    for i in range (len(bricks)):
        bricks[i].brNo= i+1

    wall.bricks = bricks
    #wall.walldescriptor()
    return wall
                    



def wall_model_builder2(wall):
    ''' this function generates a model of wall given its hight and width in centimetres
    it calculates the number of raws and nmber of bricks in each raw starting from 1
    it estimates the end of a wall's raw to a brick or half a brick '''
        
    bricks = []
    x=0
    y=0
    z=0
    
    #one way to do the wall model:
    flt1= wall.width%(BRICK_LENGTH+BRICK_SEPERATION)
    NumberOfBricksInRaw = int(wall.width/(BRICK_LENGTH+BRICK_SEPERATION))
    ##flt2= wall.hight%(BRICK_DEPTH+BRICK_SEPERATION)
    NumberOfRaws = int(wall.hight/(BRICK_DEPTH+BRICK_SEPERATION))
    #print (NumberOfBricksInRaw,NumberOfRaws,flt1,flt2)

    for j in range(NumberOfRaws):
        j+=1
        x=0
        if j%2==0:
                for i in range (NumberOfBricksInRaw):
                    i+=1
                    p = (x,y,0)
                    if i==1:
                        bd = (BRICK_LENGTH/2, BRICK_DEPTH,BRICK_WIDTH)
                    else:
                        bd = (BRICK_LENGTH, BRICK_DEPTH, BRICK_WIDTH)
                    brick =  Brick(br_No= z+1,rawNo= j,brickInRowNo=i,newP= p,brick_dimentions=bd)
                    bricks.append(brick)
                    x+=bd[0]+BRICK_SEPERATION
                    z+=1
                 
                if flt1 <= 0.5*BRICK_LENGTH and flt1 >0:
                            i =NumberOfBricksInRaw+1
                            p = (x,y,0)
                            bd = (BRICK_LENGTH, BRICK_DEPTH, BRICK_WIDTH)
                            brick =  Brick(br_No= z+1,rawNo= j,brickInRowNo=i,newP= p,brick_dimentions=bd)
                            bricks.append(brick)
                            
                else:
                            i= NumberOfBricksInRaw+1
                            p = (x,y,0)
                            bd = (BRICK_LENGTH, BRICK_DEPTH, BRICK_WIDTH)
                            brick =  Brick(br_No= z+1,rawNo= j,brickInRowNo=i,newP= p,brick_dimentions=bd)
                            bricks.append(brick)
                            i+=1
                            x+=bd[0]+BRICK_SEPERATION
                            z+=1
                            p = (x,y,0)
                            bd = (BRICK_LENGTH/2, BRICK_DEPTH, BRICK_WIDTH)
                            brick =  Brick(br_No= z+1,rawNo= j,brickInRowNo=i,newP= p,brick_dimentions=bd)
                            bricks.append(brick)                    
                y+=BRICK_DEPTH+BRICK_SEPERATION
                
        else:
                for i in range (NumberOfBricksInRaw):
                    i+=1
                    p = (x,y,0)
                    bd = (BRICK_LENGTH, BRICK_DEPTH, BRICK_WIDTH)
                    brick =  Brick(br_No= z+1,rawNo= j,brickInRowNo=i,newP= p,brick_dimentions=bd)
                    bricks.append(brick)
                    x+=bd[0]+BRICK_SEPERATION
                    z+=1
                 
                if flt1 <= 0.5*BRICK_LENGTH and flt1 >0:
                            i =NumberOfBricksInRaw+1
                            p = (x,y,0)
                            bd = (BRICK_LENGTH/2, BRICK_DEPTH, BRICK_WIDTH)
                            brick =  Brick(br_No= z+1,rawNo= j,brickInRowNo=i,newP= p,brick_dimentions=bd)
                            bricks.append(brick)
                            z+=1
                            
                else:
                            i= NumberOfBricksInRaw+1
                            p = (x,y,0)
                            bd = (BRICK_LENGTH, BRICK_DEPTH, BRICK_WIDTH)
                            brick =  Brick(br_No= z+1,rawNo= j,brickInRowNo=i,newP= p,brick_dimentions=bd)
                            bricks.append(brick)
                            z+=1
                                    

                            
                y+=BRICK_DEPTH+BRICK_SEPERATION
                
                
 
    wall.bricks = bricks
    #wall.walldescriptor()
    return wall



# Brick class
class Brick:
    def __init__(self, br_No= None, p1= (None,None),p2=(None,None),rawNo=None,
             brickInRowNo=None,newP=(None,None,None),brick_dimentions=(None,None,None)):
            self.p1 = p1
            self.p2 = p2
            self.brNo= br_No
            self.rawNo = rawNo
            self.brickInRowNo = brickInRowNo
            self.newP = newP
            self.brick_dimentions = brick_dimentions
            self.BRICK_LENGTH = brick_dimentions[0]
            self.BRICK_DEPTH= brick_dimentions[1]
            self.BRICK_WIDTH= brick_dimentions[2]
    
    # to draw a wireframe of a single brick
    def _3DdrawBrick (self):
            pass

    def brick_vertices(self):
        return (newP, (newP[0],newP[1],newP[2]+BRICK_WIDTH),(newP[0],newP[1]+BRICK_DEPTH,newP[2]),
               (newP[0],newP[1]+BRICK_DEPTH,newP[2]+BRICK_WIDTH),(newP[0]+BRICK_LENGTH,newP[1],newP[2]),
                (newP[0]+BRICK_LENGTH,newP[1],newP[2]+BRICK_WIDTH),(newP[0]+BRICK_LENGTH,newP[1]+BRICK_DEPTH,newP[2]),
                (newP[0]+BRICK_LENGTH,newP[1]+BRICK_DEPTH,newP[2]+BRICK_WIDTH))
    # prints a description of a single brick
    def descriptor(self):
            print ("{}.raw number: {} brick in raw number:{} , cords: {}, p1 and p2: {},{}".format(self.brNo,self.rawNo,self.brickInRowNo,self.newP, self.p1,self.p2))


# wall of bricks class

class Wall:
    bricks = []
    def __init__(self, Bricks = None, hight=None, width = None ):
            if Bricks != None:
                self.bricks= Bricks
                wall_model_builder1(wall= self)
            else:
                self.hight = hight*100
                self.width = width*100
                wall_model_builder2(wall= self)

    # prints a description of a wall
    def walldescriptor(self):
            for brick in self.bricks:
                    brick.descriptor()
##
#x = Wall(hight= 0.7,width= 0.7)
##brickVertices(x.bricks)
##x.walldescriptor()
##x= sortBricks(x)
##x.walldescriptor()


        
