from constants import *

class Card():
    def __init__(self, name):
        self.file = CARDS[name]
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
    walls = []
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
            x+=dx*TILE
        y, dy = (my+TILE, 1) if sin_cur>=0 else (my, -1)
        for i in range(0, card_cur.height, TILE):
            depth_h = (y-oy)/sin_cur
            xh = ox+depth_h*cos_cur
            if mapping(xh, y+dy) in card_cur.dict:
                letter_h = card_cur.dict[mapping(x+dx, yv)]
                break
            y+=dy*TILE
        depth, letter, offset = (depth_v, letter_v, yv) if depth_v<depth_h else (depth_h, letter_h, xh)
        depth*=cos(player.angle-cur_angle)
        depth = max(depth, 0.0001)
        offset = int(offset)%TILE
        proj_height = min(int(PROJ_COEF/depth), 2*SCREEN_HEIGHT)
        wall_collumn = pg.transform.scale(TEXTURES_WALLS[letter].subsurface(offset*TEXTURES_SCALE, 0, TEXTURES_SCALE, TEXTURES_HEIGHT), (SCREEN_SCALE, proj_height))
        walls.append((depth, wall_collumn, (ray*SCREEN_SCALE, SCREEN_HEIGHT/2-proj_height/2)))
        cur_angle+=DELTA_ANGLE
    return walls

class Player():
    def __init__(self, x, y, angle, speed):
        self.x, self.y = self.pos = (x, y)
        self.angle = angle
        self.speed = speed
        self.forw, self.backw, self.rightw, self.leftw, self.rightp, self.leftp = False, False, False, False, False, False
    def management(self, card_cur):
        if self.forw:
            if not (mapping(self.x+cos(self.angle)*self.speed, self.y) in card_cur.dict):
                self.x+=cos(self.angle)*self.speed
            if not (mapping(self.x, self.y+sin(self.angle)*self.speed) in card_cur.dict):
                self.y+=sin(self.angle)*self.speed
    def drawing(self, card_cur, running):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.forw = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    self.forw = False
        self.management(card_cur)
        walls = ray_casting(self, card_cur)
        objs = walls
        for obj in sorted(walls, key=lambda n:n[0], reverse=True):
            if obj[0]:
                distance, image, pos = obj
                SCREEN.blit(image, pos)
        pg.display.update()
        return running