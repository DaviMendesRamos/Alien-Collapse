import pygame
from PPlay.sprite import *
from PPlay.window import *
from PPlay.timer import *
from PPlay.gameimage import *



def mostrarMensagem(mensagem, x, y, janela, duracao, fundo = GameImage('imagens/mapa2.png')):
    quadrado = Sprite('imagens/retangulo.png')
    x -= quadrado.width / 2
    y -= quadrado.height / 2
    quadrado.set_position(x, y)
    quadrado.transparency = 200

    visivel = True

    def esconder():
        nonlocal visivel
        visivel = False

    Timer.after(duracao, esconder)

    while visivel:
        fundo.draw()
        quadrado.draw()
        janela.draw_text(f'{mensagem}', x + 15, y + 10, color=(255, 255, 255), tamanho=23, fonte='daydream')
        Timer.update()
        
        janela.update()