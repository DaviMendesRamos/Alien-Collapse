from PPlay.sprite import*
from PPlay.window import*
from PPlay.gameimage import*
from PPlay.gameobject import*
from PPlay.keyboard import*
import menu
import pygame
def loop():
    running = True
    janela = Window(1000,800)
    teste = GameImage('imagens/mapa-1.png')
    teste.scale_x = 1000 / teste.width
    teste.scale_y = 800 / teste.height
    portao = GameImage('imagens/Gate.png')
    portao.scale_x = 0.08
    portao.scale_y = 0.08
    portao.rotation = 270
    portao.set_position(885,640)
    soldado = Sprite('imagens/soldado.png')
    soldado.scale_x = 0.2
    soldado.scale_y = 0.2
    keyboard =Keyboard()
    while running:

        if keyboard.key_pressed("ESC"):
            menu.menu()

        teste.draw()
        portao.draw()
        soldado.draw()

        janela.update()

    janela.close()