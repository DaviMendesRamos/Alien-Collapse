import random
from inimigos import *
from PPlay.sprite import *


def criar_ondas(onda_inicial=0):
    vetor = [None] * 100

    for j in range(100):
        onda_num = onda_inicial + j

        # descobre em que dificuldade essa onda esta e ha quantas ondas
        # o tier atual comecou, pra saber o quanto ja cresceu
        if onda_num < 10:
            posicao_no_tier = onda_num
            tamanho_onda = 10 + posicao_no_tier * 1
        elif onda_num < 20:
            posicao_no_tier = onda_num - 10
            tamanho_onda = 10 + posicao_no_tier * 2
        else:
            posicao_no_tier = onda_num - 20
            tamanho_onda = 10 + posicao_no_tier * 3

        OndaAtual = Orda([None] * tamanho_onda)

        for i in range(tamanho_onda):

            inimigos1 = [
                inimigo.criarPesado(),
                inimigo.criarDravok(),
                inimigo.criarDravok(),
                inimigo.criarDravok()
            ]
            inimigos2 = [
                inimigo.criarDravok(),
                inimigo.criarDravok(),
                inimigo.criarPesado(),
                inimigo.criarPesado(),
                inimigo.criarAfobado()
            ]
            inimigos3 = [
                inimigo.criarDravok(),
                inimigo.criarPesado(),
                inimigo.criarVoador(),
                inimigo.criarVoador(),
                inimigo.criarAfobado(),
                inimigo.criarAfobado()
            ]
            inimigos4 = [
                inimigo.criarDravok(),
                inimigo.criarPesado(),
                inimigo.criarAfobado(),
                inimigo.criarVoador(),
                inimigo.criarCamburao()]

            if onda_num < 10:
                enemy = random.choice(inimigos4)
            elif onda_num < 20:
                enemy = random.choice(inimigos4)
            elif onda_num < 30:
                enemy = random.choice(inimigos4)
            else :
                enemy = random.choice(inimigos4)

            OndaAtual.Onda[i] = enemy

        vetor[j] = OndaAtual

    return vetor