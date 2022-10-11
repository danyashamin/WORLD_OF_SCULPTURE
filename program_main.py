from algoritms import *

card_cur_name = 'CARD_TRIAL'
card_cur_obj = Card(card_cur_name)
player = Player(card_cur_obj.WIDTH/2, card_cur_obj.HEIGHT/2, 0, 2)

while running:
    running = player.drawing(card_cur_obj, running)