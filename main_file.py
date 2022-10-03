from algoritms import *

CARD_CUR = Card('CARD_TRIAL')
player = Player(CARD_CUR.width/2, CARD_CUR.height/2, 0, 2)
while running:
    running = player.drawing(CARD_CUR, running)
    fps = clock.get_fps()
    clock.tick()
pg.quit()