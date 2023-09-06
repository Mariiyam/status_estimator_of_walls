'''
This module defines the functions that take wall objects as arguments, 
plots 3D visualizations of them, and provides interaction facilities:
left,right, up , down and zoom
'''
from TheBrickModel import *
import pygame  # pip install pygame
from pygame.locals import *
import sys

from OpenGL.GL import *  # pip install pyopengl
from OpenGL.GLU import *

surfaces = (
    (4,5,1,0)
    )



def drawBrick(verticies,edges):

   # to color the surfaces:
    glBegin(GL_QUADS)
    for vertex in (2,6,7,3):
        glColor3fv([0.5,0.5,.5])
        glVertex3fv(verticies[vertex])
    glEnd()
    
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def draw3Dwall(wall):
    edges = (
		(0,1),
		(0,2),
		(0,4),
		(1,3),
		(1,5),
		(2,3),
		(2,6),
		(3,7),
		(4,5),
		(4,6),
		(6,7),
		(5,7)
		)

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(90, (display[0]/display[1]), 0.1, 1000.0)

    glTranslatef(-10,-5, -10)
    glRotatef(0,1,.5,0)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-BRICK_LENGTH,0.0, 0.0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(BRICK_LENGTH,0.0, 0.0)
                if event.key == pygame.K_UP:
                    glTranslatef(0.0,BRICK_DEPTH, 0.0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0.0,-BRICK_DEPTH, 0.0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button== 4:
                    glTranslatef(0,0,1)
                if event.button== 5:
                    glTranslatef(0,0,-1)

        glRotatef(1, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for brick in wall.bricks:
            verticies =(
            (brick.newP[0],brick.newP[1],brick.newP[2]),
            (brick.newP[0]+brick.BRICK_LENGTH,brick.newP[1],brick.newP[2]),
            (brick.newP[0],brick.newP[1],brick.newP[2]+brick.BRICK_WIDTH),
            (brick.newP[0]+brick.BRICK_LENGTH,brick.newP[1],brick.newP[2]+brick.BRICK_WIDTH),
            (brick.newP[0],brick.newP[1]+brick.BRICK_DEPTH,brick.newP[2]),
            (brick.newP[0]+brick.BRICK_LENGTH,brick.newP[1]+brick.BRICK_DEPTH,brick.newP[2]),
            (brick.newP[0],brick.newP[1]+brick.BRICK_DEPTH,brick.newP[2]+brick.BRICK_WIDTH),
            (brick.newP[0]+brick.BRICK_LENGTH,brick.newP[1]+brick.BRICK_DEPTH,brick.newP[2]+brick.BRICK_WIDTH)
            )
    
            drawBrick(verticies,edges)
        pygame.display.flip()
        pygame.time.wait(10)

#x = Wall(hight= 1,width= 1)
#draw3Dwall(x)
#x.walldescriptor()
