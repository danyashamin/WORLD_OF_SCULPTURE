import pygame as pg
pg.init()
from math import pi, sin, cos, tan, atan2, degrees, sqrt

NUM_RAYS = 300
CENTER_RAY = NUM_RAYS//2-1
FAKE_RAYS = 100
FAKE_RAYS_RANGE = FAKE_RAYS+NUM_RAYS-1+FAKE_RAYS
TILE = 100
FOV = pi/3
HALF_FOV = FOV/2
DOUBLE_PI = pi*2
DELTA_ANGLE = FOV/NUM_RAYS
DIST = NUM_RAYS/(2*tan(HALF_FOV))
PROJ_COEF = 3*DIST*TILE
SCREEN = pg.display.set_mode((1200, 800))
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
SCREEN_SCALE = SCREEN_WIDTH/NUM_RAYS
CARDS = {'CARD_TRIAL':open('game_files\CARDS\CARD_TRIAL.txt')}
TEXTURES_WALLS = {'1':pg.image.load('game_files\TEXTURES\TEXTURES_WALLS\WALL_TRIAL.bmp').convert(), '2':pg.image.load('game_files\TEXTURES\TEXTURES_WALLS\WALL_TRIAL_2.bmp').convert()}
TEXTURES_SPRITES = {'sprite_trial':[pg.image.load(f'game_files\TEXTURES\TEXTURES_SPRITES\SPRITE_TRIAL\SPRITE_TRIAL.{i}.bmp') for i in range(8)]}
clock = pg.time.Clock()
running = True
TEXTURES_WIDTH = TEXTURES_WALLS['1'].get_width()
TEXTURES_HEIGHT = TEXTURES_WALLS['1'].get_height()
TEXTURES_SCALE = TEXTURES_WIDTH/TILE
COLORS = {'WHITE':(255, 255, 255)}