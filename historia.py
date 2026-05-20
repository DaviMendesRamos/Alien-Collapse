from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
import pygame


def criar_orda():
    n = 5
    vet = []
    for i in range(n):
        dravok = Sprite('imagens/dravok.png')
        dravok.set_position(50 + (i * 40), 100) 
        vet.append(dravok)
    return vet


def loop(janela):
    running = True
    
    teste = GameImage('imagens/mapa-1.png')
    teste.scale_x = 800 / teste.width
    teste.scale_y = 600 / teste.height
    
    portao = GameImage('imagens/Gate.png')
    portao.scale_x = 0.07
    portao.scale_y = 0.07
    portao.rotation = 270
    portao.set_position(705, 470)
    
    soldado = Sprite('imagens/soldado.png')
    soldado.scale_x = 0.2
    soldado.scale_y = 0.2
    
    keyboard = Keyboard()
    
    timerWave = 0
    tempo_de_espera = 10
    inimigos_na_tela = []

    while running:
       
        if keyboard.key_pressed("ESC"):
            break 
            
        timerWave += janela.delta_time()
        
      
        if timerWave > tempo_de_espera:
            nova_orda = criar_orda()
            inimigos_na_tela.extend(nova_orda) 
            timerWave = 0

        
        for dravok in inimigos_na_tela[:]: 
            dravok.y += 50 * janela.delta_time()
            dravok.x += 50 * janela.delta_time()
            
       
            if dravok.y > 600:
                inimigos_na_tela.remove(dravok)

        
        teste.draw()
        portao.draw()
        soldado.draw()
        
        for dravok in inimigos_na_tela:
            dravok.draw()

        janela.update()