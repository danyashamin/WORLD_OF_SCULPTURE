from algoritms import *

CARD_CUR = Card('CARD_TRIAL')
player = Player(CARD_CUR.WIDTH/2, CARD_CUR.HEIGHT/2, 0, 2)

while running:
    running = player.drawing(CARD_CUR, running)