import PPlay
from PPlay.sprite import*
from PPlay.window import*
from PPlay.gameimage import*
from PPlay.gameobject import*
from PPlay.keyboard import*
import pygame

def Orda():
    n = 5
    vet = []
    running = True
    while running:

        for i in range(n):
            dravok = Sprite('dravok.png')
            dravok.set_position(50, 100)
            vet.append(dravok)

        for dravok in vet:
            dravok.draw()
            if dravok.y > 600:
                vet.remove(dravok)
            dravok.y-= 250*janela.delta_time()

    