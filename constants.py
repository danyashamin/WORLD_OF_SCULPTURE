import pygame as pg
pg.init()
from math import sin, cos, tan, atan2, pi

TILE = 100
NUM_RAYS = 300
FOV = pi/3
HALF_FOV = FOV/2
DELTA_ANGLE = FOV/NUM_RAYS