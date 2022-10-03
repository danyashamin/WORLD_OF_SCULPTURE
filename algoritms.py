from constants import *

class Card():
    def __init__(self, name):
        self.file = open(name)
        self.list = self.file.read().split('\n')
        self.width = len(self.list[0])*TILE
        self.height = len(self.list)*TILE
        self.dict = dict()
        for i, row in enumerate(self.list):
            for j, char in enumerate(row):
                if char!='.':
                    self.dict[(j*TILE, i*TILE)] = char
def mapping(a, b):
    return ((a//TILE)*TILE, (b//TILE)*TILE)
def ray_casting(player, card_cur):
    ox, oy = player.x, player.y
    mx, my = mapping(ox, oy)
    cur_angle = player.angle - HALF_FOV
    for ray in range(NUM_RAYS):
        cos_cur = cos(cur_angle)
        sin_cur = sin(cur_angle)
        x, dx = (mx+TILE, 1) if cos_cur>=0 else (mx, -1)
        for i in range(0, card_cur.width, TILE):
            depth_v = (x-ox)/cos_cur
            yv = oy+depth_v*sin_cur
            if mapping(x+dx, yv) in card_cur.dict:
                letter_v = card_cur.dict[mapping(x+dx, yv)]
                break