from PPlay.sprite import*
from PPlay.window import*
from PPlay.gameimage import*
from PPlay.gameobject import*
import pygame

janela = Window(1000,800)
teste = GameImage('mapa-1.png')
teste.scale_x = 1000 / teste.width
teste.scale_y = 800 / teste.height
portao = GameImage('Gate.png')
portao.scale_x = 0.08
portao.scale_y = 0.08
portao.rotation = 270
portao.set_position(885,640)
soldado = Sprite('soldado.png')
soldado.scale_x = 0.2
soldado.scale_y = 0.2

while True:
    teste.draw()
    portao.draw()
    soldado.draw()
    janela.update()