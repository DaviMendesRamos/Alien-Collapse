import random
from inimigos import*
from PPlay.sprite import*


def criar_ondas():
    vetor = [None]*10
    for j in range (10):
        
        OndaAtual = Orda([None]*10)
        for i in range (10):
            
            inimigos = [
            inimigo.criarPesado(),
            inimigo.criarDravok()
        ]
            enemy = random.choice(inimigos)
            OndaAtual.Onda[i] = enemy
            print(OndaAtual.Onda[i])

        vetor[j] = OndaAtual
    

    return vetor
