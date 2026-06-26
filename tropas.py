from PPlay.sprite import *

import math


class Tiro:
    def __init__(self, x, y, alvo, dano, danoesp, caminho_sprite):
        self.sprite = Sprite(caminho_sprite) #recebe o caminho de acordo com a tropa que atirou
        self.sprite.set_position(x, y) 
        self.alvo = alvo
        self.dano = dano
        self.danoesp = danoesp #dano contra escudo
        self.velocidade = 20 
        self.ativo = True #se o tiro ainda esta a caminho do alvo

    def update(self): #atualiza o tiro, roda em loop
        if not self.ativo: #verifica se o tiro ainda esta a caminho do alvo
            return
        if self.alvo.morreu(): #deleta o tiro se o alvo morrer
            self.ativo = False
            return
        dx = self.alvo.sprite.x - self.sprite.x
        dy = self.alvo.sprite.y - self.sprite.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < self.velocidade * 2: #destroi o tiro quando atinge o alvo
            self.alvo.receber_dano(self.dano, self.danoesp)
            self.ativo = False
        else: #move o tiro para o alvo
            self.sprite.x += (dx / dist) * self.velocidade
            self.sprite.y += (dy / dist) * self.velocidade
            self.sprite.rotation = math.degrees(math.atan2(-dy, dx)) +90#gira a tropa de acordo com a direção do alvo
            self.sprite.draw()
            


class tropa: #classe da tropa
    def __init__(self, nome, custo, dano, danoesp, alcance, velocidade, sprite, spritetiro):
        self.nome = nome
        self.custo = custo
        self.velocidade = velocidade   # cadência de tiro
        self.dano = dano
        self.danoesp = danoesp         # dano contra escudo
        self.alcance = alcance
        self.sprite = sprite
        self.spritetiro = spritetiro   # caminho da imagem do projétil (string)
        self.tiros = [] #vetor dos tiros daquela tropa
        self.cooldown = 0 #cooldown de tiro

    def atirar(self, inimigos): #recebe o vetor de inimigos ativos
        # encontra o inimigo mais próximo dentro do alcance
        alvo = None
        menor_dist = self.alcance
        for ini in inimigos:
            dx = ini.sprite.x - self.sprite.x
            dy = ini.sprite.y - self.sprite.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= self.alcance and dist < menor_dist: #verifica se ha inimigos dentro do alcance e seta o alvo para o mais proximo
                menor_dist = dist
                alvo = ini
        if alvo:
            dx = alvo.sprite.x - self.sprite.x
            dy = alvo.sprite.y - self.sprite.y
            self.sprite.rotation = math.degrees(math.atan2(-dy, dx)) #gira a tropa de acordo com a direção do alvo
            self.tiros.append(
                Tiro(self.sprite.x, self.sprite.y, alvo, self.dano, self.danoesp, self.spritetiro) #dispara o tiro
            )

    def update(self, janela, inimigos): #roda em loop para atualizar a tropa
        self.sprite.draw() #desenha a tropa
        # velocidade controla cadência: quanto maior, mais rápido atira
        self.cooldown += self.velocidade * janela.delta_time()
        if self.cooldown >= 1:
            self.cooldown = 0
            self.atirar(inimigos) #dispara o loop de atirar
        self.tiros = [t for t in self.tiros if t.ativo]
        for tiro in self.tiros: #atualiza o tiro daquela tropa
            tiro.update()

    def criarSoldado(x, y): #cria um soldado
        trop = tropa('soldado', 100, 25, 0, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png')
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop
    def criarSolari(x,y):
        trop = tropa('solari',150,25,25,150,1, Sprite('imagens/solari.png'), 'imagens/tiroSolari.png')
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop

class Portao(): #classe do portao
    def __init__(self, vida):
        self.vida =vida
        self.sprite = Sprite('imagens/Gate2.png')
    
    def chegouPortao(self,vetIni): #metodo que rebe o portao e o vetor de inimigos ativos
        for ini in vetIni: #percorre cada inimigo do vetor de ativos
            if (ini.sprite.collided(self.sprite)): #verifica se os sprites colidiram
                self.vida -= ini.vida #se sim tira a vida restante do inimigo do portao
                vetIni.remove(ini) #destroi o inimigo
        if self.vida <=0:
            return True#se a vida do portao for menor ou igual a zero retorna true e acaba a partida
        return False #se nao retorna false e continua

def loopTrp(janela, vetor, inimigos): #loop chamado no game para atualizar as tropas colocadas, recebe o vetor de tropas ativas e inimigos
    for trp in vetor:
        trp.update(janela, inimigos)
