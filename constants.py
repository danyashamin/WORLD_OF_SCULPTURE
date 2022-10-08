import pygame as pg
from math import pi, sin, cos, tan, atan2
pg.init()

SCREEN = pg.display.set_mode((1200, 800))
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
NUM_RAYS = 300
SCREEN_SCALE = SCREEN_WIDTH/NUM_RAYS
TILE = 100
FOV = pi/3
HALF_FOV = FOV/2
DELTA_ANGLE = FOV/NUM_RAYS
DIST = NUM_RAYS/(2*tan(HALF_FOV))
PROJ_COEF = 3*DIST*TILE
CARDS = {'CARD_TRIAL':open('game_files\CARDS\CARD_TRIAL.txt')}
TEXTURES_WALLS = {'1':pg.image.load('game_files\TEXTURES\TEXTURES_WALLS\WALL_TRIAL.bmp').convert()}
WALL_WIDTH = TEXTURES_WALLS['1'].get_width()
WALL_HEIGHT = TEXTURES_WALLS['1'].get_height()
WALL_SCALE = WALL_WIDTH/TILE

running = True
clock = pg.time.Clock()