import pygame
from PPlay.sprite import *
from PPlay.window import *
from PPlay.uikit import*
from grid import*


def mostrarTropa(nometrp, baralho, janela):
    for i in range(len(baralho)):
        if baralho[i].nome == nometrp:
            tropa = baralho[i]

    quadrado =Sprite('imagens/retangulasso.png')
    quadrado.set_position(580, 70)
    quadrado.transparency = 150
    quadrado.draw()
   
    janela.draw_text(f'Nome: {tropa.nome}', 590, 90, color=(255, 255, 255), tamanho=23,fonte= 'daydream')
    janela.draw_text(f'Custo: {tropa.custo}', 590, 115, color=(255, 255, 255), tamanho=23,fonte= 'daydream')
    janela.draw_text(f'Dano: {tropa.dano}', 590, 140, color=(255, 255, 255), tamanho=23,fonte= 'daydream')
    janela.draw_text(f'Dano escudo: {tropa.danoesp}', 590, 165, color=(255, 255, 255), tamanho=23,fonte= 'daydream')
    janela.draw_text(f'Alcance: {tropa.alcance}', 590, 190, color=(255, 255, 255), tamanho=23,fonte= 'daydream')
    janela.draw_text(f'Cadencia: {tropa.velocidade}', 590, 215, color=(255, 255, 255), tamanho=23,fonte= 'daydream')
    if tropa.aereo == True:

        janela.draw_text(f'anti-aereo: Sim', 590, 240, color=(255, 255, 255), tamanho=23,fonte= 'daydream')
    else:

        janela.draw_text(f'anti-aereo: Nao', 590, 240, color=(255, 255, 255), tamanho=23,fonte= 'daydream')
    if tropa.slow>1:

        janela.draw_text(f'Poder: retarda os inimigos', 590, 265, color=(255, 255, 255), tamanho=20,fonte= 'daydream')
    if tropa.nome == 'Torre':
        janela.draw_text(f'Poder: acelera as tropas', 590, 265, color=(255, 255, 255), tamanho=20,fonte= 'daydream')
   
def VenderTropa(tropa, vetor, janela,mouse,grid, money):
    quadrado = Sprite('imagens/retangulasso.png')
    quadrado.set_position(580, 70)
    quadrado.transparency = 150

    btn = Button(130, 40, 'Vender', cor_base=(80,0,0), cor_hover='red')
    btn.set_position(605, 200)


    quadrado.draw()
    btn.update()
    btn.draw()
    janela.draw_text(f'Reembolso: {tropa.custo/2}', 590, 150, color=(255, 255, 255), tamanho=27, fonte='daydream')
    if mouse.button_pressed(mouse.RIGHT):
        return vetor,grid,money, True
    if btn.is_clicked():
        vetor.remove(tropa)
        money+=tropa.custo/2
        x,y = grid.pixel_para_celula(tropa.sprite.x, tropa.sprite.y)
        grid.liberar_celula(x,y)
        return vetor ,grid,money, True
    return vetor,grid,money, False




        