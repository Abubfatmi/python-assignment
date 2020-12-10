import pygame
from pygame.locals import *
import cv2
import numpy

color=False
camera_index = 0
camera=cv2.VideoCapture(camera_index)
camera.set(3,640)
camera.set(4,480)
screen_width, screen_height = 640, 480
screen=pygame.display.set_mode((screen_width,screen_height))

def getCamFrame(color,camera):
    retval,frame=camera.read()
    if not color:
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame=numpy.rot90(frame)
    frame=pygame.surfarray.make_surface(frame) 
    return frame

def blitCamFrame(frame,screen):
    screen.blit(frame,(0,0))
    return screen

screen.fill(0) 
frame=getCamFrame(color,camera)
screen=blitCamFrame(frame,screen)
pygame.display.flip()
pygame.image.save(screen, 'C:\\Users\\abuba\\OneDrive\\Desktop\\facerec\\unknown_faces\\aah2'+'.jpg')


pygame.quit()
cv2.destroyAllWindows()
