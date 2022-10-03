import pygame as pg
pg.init()
from math import sin, cos, tan, atan2, pi

TILE = 100
NUM_RAYS = 300
FOV = pi/3
HALF_FOV = FOV/2
DELTA_ANGLE = FOV/NUM_RAYS
DIST = NUM_RAYS/(2*tan(HALF_FOV))
PROJ_COEF = 3*DIST*TILE
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_SCALE = SCREEN_WIDTH/NUM_RAYS
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TEXTURES_WALLS = {'1':pg.image.load('game_files\TEXTURES\TEXTURES_WALLS\WALL_TRIAL.bmp').convert()}
CARDS = {"CARD_TRIAL":open('game_files\CARDS\CARD_TRIAL.txt')}
TEXTURES_WIDTH = 1200
TEXTURES_HEIGHT = 1200
TEXTURES_SCALE = TEXTURES_WIDTH/TILE
running = True
clock = pg.time.Clock()