from constants import *

class Card():
    def __init__(self, card_name):
        self.file = CARDS[card_name]
        self.list = self.file.read().split('\n')
        self.WIDTH = len(self.list[0])*TILE
        self.HEIGHT = len(self.list)*TILE
        self.DICT = dict()
        for i, row in enumerate(self.list):
            for j, char in enumerate(row):
                if char!='.':
                    self.DICT[(j*TILE, i*TILE)] = char

def mapping(a, b):
    return ((a//TILE)*TILE, (b//TILE)*TILE)
def ray_casting(player, CARD_CUR):
    walls = []
    ox, oy = player.x, player.y
    mx, my = mapping(ox, oy)
    cur_angle = player.angle - HALF_FOV
    for ray in range(NUM_RAYS):
        cur_cos = cos(cur_angle)
        cur_sin = sin(cur_angle)
        x, dx = (mx+TILE, 1) if cur_cos>=0 else (mx, -1)
        for i in range(0, CARD_CUR.WIDTH, TILE):
            depth_v = (x-ox)/cur_cos
            yv = oy+depth_v*cur_sin
            map_v = mapping(x+dx, yv)
            if map_v in CARD_CUR.DICT:
                letter_v = CARD_CUR.DICT[mapping(x+dx, yv)]
                break
            x+=dx*TILE
        y, dy = (my+TILE, 1) if cur_sin>=0 else (my, -1)
        for i in range(0, CARD_CUR.HEIGHT, TILE):
            depth_h = (y-oy)/cur_sin
            xh = ox+depth_h*cur_cos
            map_h = mapping(xh, y+dy)
            if map_h in CARD_CUR.DICT:
                letter_h = CARD_CUR.DICT[map_h]
                break
            y+=dy*TILE
        depth, letter, offset = (depth_v, letter_v, yv) if depth_v<depth_h else (depth_h, letter_h, xh)
        depth*=cos(player.angle-cur_angle)
        depth = max(depth, 0.0001)
        proj_height = min(int(PROJ_COEF/depth), 2*SCREEN_HEIGHT)
        offset = int(offset)%TILE
        wall_image = pg.transform.scale(TEXTURES_WALLS[letter].subsurface(WALL_SCALE*offset, 0, WALL_SCALE, WALL_HEIGHT), (SCREEN_SCALE, proj_height))
        walls.append((depth, wall_image, (ray*SCREEN_SCALE, SCREEN_HEIGHT/2-proj_height/2)))
        cur_angle+=DELTA_ANGLE
    return walls
            

class Player():
    def __init__(self, x, y, angle):
        self.x, self.y = x, y
        self.angle = angle
    def pos(self):
        return (self.x, self.y)
    def drawing(self, card_cur, running):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
        walls = ray_casting(self, card_cur)
        objs = walls
        for obj in sorted(objs, key=lambda n:n[0], reverse=True):
            if obj[0]:
                distance, image, pos = obj
                SCREEN.blit(image, pos)
        pg.display.update()
        return running