from constants import *

class Card():
    def __init__(self, name):
        self.file = CARDS[name]
        self.list = self.file.read().split('\n')
        self.map = dict()
        for i, row in enumerate(self.list):
            for j, char in enumerate(row):
                if char!='.':
                    self.map[(j*TILE, i*TILE)] = char
        self.WIDTH = len(self.list[0])*TILE
        self.HEIGHT = len(self.list)*TILE

def mapping(a, b):
    return ((a//TILE)*TILE, (b//TILE)*TILE)
def ray_casting(player, card_cur):
    walls = []
    ox, oy = player.x, player.y
    mx, my = mapping(ox, oy)
    cur_angle = player.angle - HALF_FOV
    for ray in range(NUM_RAYS):
        cur_cos = cos(cur_angle)
        cur_sin = sin(cur_angle)
        x, dx = (mx+TILE, 1) if cur_cos>=0 else (mx, -1)
        for i in range(0, card_cur.WIDTH, TILE):
            depth_v = (x-ox)/cur_cos
            yv = oy+depth_v*cur_sin
            if mapping(x+dx, yv) in card_cur.map:
                letter_v = card_cur.map[mapping(x+dx, yv)]
                break
            x+=dx*TILE
        y, dy = (my+TILE, 1) if cur_sin>=0 else (my, -1)
        for i in range(0, card_cur.HEIGHT, TILE):
            depth_h = (y-oy)/cur_sin
            xh = ox+depth_h*cur_cos
            if mapping(xh, y+dy) in card_cur.map:
                letter_h = card_cur.map[mapping(xh, y+dy)]
                break
            y+=dy*TILE
        depth, offset, letter = (depth_v, yv, letter_v) if depth_v<depth_h else (depth_h, xh, letter_h)
        depth*=cos(player.angle-cur_angle)
        depth = max(depth, 0.0001)
        proj_height = min(int(PROJ_COEF/depth), 2*SCREEN_HEIGHT)
        offset = int(offset%TILE)
        wall_collumn = pg.transform.scale(TEXTURES_WALLS[letter].subsurface(offset*TEXTURES_SCALE, 0, TEXTURES_SCALE, TEXTURES_HEIGHT), (SCREEN_SCALE, proj_height))
        walls.append((depth, wall_collumn, (ray*SCREEN_SCALE, SCREEN_HEIGHT/2-proj_height/2)))
        cur_angle+=DELTA_ANGLE
    return walls

class SpriteObject():
    def __init__(self, sprite_type, static, pos, shift, scale):
        self.image = TEXTURES_SPRITES[sprite_type]
        self.static = static
        self.pos = self.x, self.y = pos[0], pos[1]
        self.shift = shift
        self.scale = scale
        if not self.static:
            self.sprite_angles = [frozenset(range(i, i+45)) for i in range(0, 360, 45)]
            self.sprite_images = {angles:image for angles, image in zip(self.sprite_angles, self.image)}
    def object_locate(self, player, walls):
        dx, dy = self.x-player.x, self.y-player.y
        theta = atan2(dy, dx)
        gamma = theta - player.angle
        if dx>0 and 180<=degrees(player.angle)<=360 or dx<0 and dy<0:
            gamma+=DOUBLE_PI
        delta_rays = int(gamma/DELTA_ANGLE)
        current_ray = CENTER_RAY+delta_rays
        if 0<=current_ray<=FAKE_RAYS_RANGE:
            if not self.static:
                if theta<0:
                    theta+=DOUBLE_PI
                theta = 360 - int(degrees(theta))
                for angles in self.sprite_angles:
                    if theta in angles:
                        self.image = self.sprite_images[angles]
                        break
            distance_to_sprite = sqrt(dx**2+dy**2)
            distance_to_sprite*=cos(HALF_FOV-current_ray*DELTA_ANGLE)
            proj_height = min(int(PROJ_COEF/distance_to_sprite)*self.scale, 2*SCREEN_HEIGHT*self.scale)
            half_proj_height = proj_height//2
            shift = half_proj_height*self.shift
            sprite_pos = (current_ray*SCREEN_SCALE-half_proj_height, SCREEN_HEIGHT/2-proj_height/2-shift)
            sprite = pg.transform.scale(self.image, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False, )

class Player():
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.forw, self.rightp = False, False
    def management(self, CARD_CUR):
        if self.forw:
            if not (mapping(self.x+cos(self.angle)*self.speed, self.y) in CARD_CUR.map):
                self.x+=cos(self.angle)*self.speed
            if not (mapping(self.x, self.y+sin(self.angle)*self.speed) in CARD_CUR.map):
                self.y+=sin(self.angle)*self.speed
        if self.rightp:
            self.angle += 0.02
            self.angle%=DOUBLE_PI
    def drawing(self, CARD_CUR, running):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.forw = True
                if event.key == pg.K_RIGHT:
                    self.rightp = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    self.forw = False
                if event.key == pg.K_RIGHT:
                    self.rightp = False
        self.management(CARD_CUR)
        SCREEN.fill(COLORS['WHITE'])
        walls = ray_casting(self, CARD_CUR)
        sprites = [sprite.object_locate(self, walls) for sprite in sprites_on_card]
        objs = walls+sprites
        for obj in sorted(objs, key=lambda n:n[0], reverse=True):
            if obj[0]:
                distance, image, pos = obj
                SCREEN.blit(image, pos)
        pg.display.update()
        fps = clock.get_fps()
        clock.tick()
        return running

sprites_on_card = [SpriteObject('SPRITE_TRIAL', False, (300, 300), 1, 2)]
