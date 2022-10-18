from algoritms import *

card_cur_name = 'CARD_TRIAL'
card_new_name = 'CARD_TRIAL'
card_cur = Card(card_cur_name)
player = Player(card_cur.WIDTH/2, card_cur.HEIGHT/2, 0, 2)
cycle_cur_type = 'trial'
cycle_new_type = 'trial'
while running:
    if cycle_cur_type == 'trial':
        running = player.drawing(card_cur, running)
    fps = clock.get_fps()
    clock.tick()
pg.quit()