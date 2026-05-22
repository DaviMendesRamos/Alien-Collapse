from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
from PPlay.mouse import *
import pygame
from inimigos import *
from tropas import *


def loop(janela):
    vetor = []
    mouse = Mouse()
    trpSelected = ''
    running = True
    money = 200
    teste = GameImage('imagens/mapa.png')
    teste.scale_x = 800 / teste.width
    teste.scale_y = 600 / teste.height
    Soldado = Sprite('imagens/soldado.png')
    Soldado.set_position(400, 550)
    portao = GameImage('imagens/Gate.png')
    portao.scale_x = 0.07
    portao.scale_y = 0.07
    portao.rotation = 270
    portao.set_position(705, 470)

    keyboard = Keyboard()
    click_cooldown = 0

    onda_atual = Orda([
        inimigo.criarDravok(),
        inimigo.criarDravok(),
        inimigo.criarDravok(),
        inimigo.criarPesado(),
    ])

    while running:
        if keyboard.key_pressed("ESC"):
            break

        teste.draw()
        portao.draw()
        a,b = mouse.get_position()
        
        if mouse.button_pressed (mouse.LEFT):
            print(a,b)

        Soldado.draw()
        click_cooldown -= 100* janela.delta_time()

        if mouse.button_pressed(mouse.LEFT) and click_cooldown <= 0:#verifica o clique e o cooldown
            if mouse.is_over_object(Soldado): # se tiver clicado em soldado seleciona o mesmo
                # clique no ícone: seleciona a tropa
                trpSelected = 'Soldado'
                click_cooldown = 100

            elif trpSelected == 'Soldado' and money >= 100: # se o soldado tiver selecionado, verifica o dinheiro
                # clique no mapa: coloca a tropa
                mx, my = mouse.get_position() #pega a posiçao de clique do mouse
                vetor.append(tropa.criarSoldado(mx, my)) #cria a tropa e adiciona no vetor de tropas
                money -= 100
                click_cooldown = 100
        janela.draw_text(f"Money: {money}", 20,20)

        money = onda_atual.update(janela,money)#atualiza a onda
        loopTrp(janela, vetor, onda_atual.vet)#passa o vetor de tropas e o vetor de inimigos ativos e atualiza as tropas

        janela.update()
