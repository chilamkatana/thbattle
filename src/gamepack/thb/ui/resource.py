import pyglet
import os

from client.ui.resource import ResLoader

with ResLoader(__file__) as args:
    locals().update(args)
    card_attack = tx('attack.tga')
    card_graze = tx('graze.tga')
    card_heal = tx('heal.tga')
    card_demolition = tx('card_demolition.tga')
    card_reject = tx('card_reject.tga')
    card_sealarray = tx('card_sealarray.tga')
    tag_sealarray = anim('tag_sealarray.png', [300, 500, 300], True)
    card_nazrinrod= tx('card_nazrinrod.tga')
    card_opticalcloak = tx('card_opticalcloak.tga')
    card_opticalcloak_small = tx('card_opticalcloak_small.tga')
    card_greenufo = tx('card_greenufo.tga')
    card_greenufo_small = tx('card_greenufo_small.tga')
    card_redufo = tx('card_redufo.tga')
    card_redufo_small = tx('card_redufo_small.tga')
    card_zuidai = tx('card_zuidai.tga')
    tag_zuidai = anim('tag_zuidai.png', [100]*3, True)

    parsee_port = tx('parsee_port.png')
    youmu_port = tx('youmu_port.png')
    ldevil_port = tx('ldevil_port.png')


    for k in args.keys(): del k
    del args
