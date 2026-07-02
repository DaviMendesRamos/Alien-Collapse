from PPlay.sprite import *
from PPlay.sound import *
from PPlay.animation import Animation

import math


class Tiro:
    def __init__(self, x, y, alvo, dano, danoesp,raio,slow, caminho_sprite,
                 caminho_explosao=None, frames_explosao=0):
        self.sprite = Sprite(caminho_sprite) #recebe o caminho de acordo com a tropa que atirou
        self.sprite.set_position(x, y) 
        self.alvo = alvo
        self.dano = dano
        self.danoesp = danoesp
        self.raio = raio #dano contra escudo
        self.velocidade = 20 
        self.slow = slow
        self.ativo = True #se o tiro ainda esta a caminho do alvo

        # --- Explosão (usada apenas pelo granadeiro) ---
        self.caminho_explosao = caminho_explosao
        self.frames_explosao = frames_explosao
        self.explodindo = False
        self.explosao = None
        self.som = Sound('sons/somExplosao.mp3')
        self.som2 = Sound('sons/somEclipse.mp3')

    def _iniciar_explosao(self):
        """Cria e posiciona a animação de explosão no ponto de impacto."""
        self.explosao = Animation(self.caminho_explosao, self.frames_explosao, loop=False)
        self.explosao.set_total_duration(400)  # duração total da explosão em ms
        self.explosao.x = self.sprite.x - self.explosao.width / 2
        self.explosao.y = self.sprite.y - self.explosao.height / 2
        self.explodindo = True

    def update(self,inimigos): #atualiza o tiro, roda em loop
        if not self.ativo: #verifica se o tiro ainda esta a caminho do alvo
            return

        # se já está no meio da explosão, só atualiza/desenha a animação
        if self.explodindo:
            self.explosao.update()
            self.explosao.draw()
            if not self.explosao.rodando: #quando a animação termina, desativa o tiro
                self.ativo = False
            return

        if self.alvo.morreu(): #deleta o tiro se o alvo morrer
            self.ativo = False
            return
        dx = self.alvo.sprite.x - self.sprite.x
        dy = self.alvo.sprite.y - self.sprite.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < self.velocidade * 2: #atingiu o alvo
            
            for ini in inimigos:
                dx = ini.sprite.x - self.sprite.x
                dy = ini.sprite.y - self.sprite.y
                dist = math.sqrt(dx * dx + dy * dy)
                menor_dist = self.raio
                if dist <= self.raio and dist < menor_dist: #verifica se ha inimigos dentro do alcance e seta o alvo para o mais proximo
                    ini.receber_dano(self.dano, self.danoesp,)
                    ini.velocidade = ini.velocidade/self.slow

            self.alvo.receber_dano(self.dano, self.danoesp)
            self.alvo.velocidade = self.alvo.velocidade0/self.slow
            if self.raio ==100:
                self.som.play()
            if self.raio == 99:
                self.som2.play()

            if self.caminho_explosao: #só existe explosão se o tiro tiver sido criado com ela (granadeiro)
                self._iniciar_explosao()
            else:
                self.ativo = False
        else: #move o tiro para o alvo
            self.sprite.x += (dx / dist) * self.velocidade
            self.sprite.y += (dy / dist) * self.velocidade
            self.sprite.rotation = math.degrees(math.atan2(-dy, dx)) +90#gira a tropa de acordo com a direção do alvo
            self.sprite.draw()
            


class tropa: #classe da tropa
    def __init__(self, nome, custo, dano, danoesp, alcance, velocidade, raio,slow,aereo, sprite, spritetiro, somtiro,
                 spriteexplosao=None, framesexplosao=0):
        self.nome = nome
        self.custo = custo
        self.velocidade = velocidade 
        self.velocidade0= velocidade  # cadência de tiro
        self.dano = dano
        self.danoesp = danoesp         # dano contra escudo
        self.alcance = alcance
        self.raio = raio
        self.slow = slow
        self.aereo = aereo
        self.sprite = sprite
        self.spritetiro = spritetiro # caminho da imagem do projétil (string)
        self.somtiro = somtiro  
        self.tiros = [] #vetor dos tiros daquela tropa
        self.cooldown = 0 #cooldown de tiro

        # --- Explosão (usada apenas pelo granadeiro) ---
        self.spriteexplosao = spriteexplosao
        self.framesexplosao = framesexplosao

    def atirar(self, inimigos,vetor ): #recebe o vetor de inimigos ativos
        # encontra o inimigo mais próximo dentro do alcance
        alvo = None
        menor_dist = self.alcance
        if self.nome == 'Torre':
            for trp in vetor:
                dx = trp.sprite.x - self.sprite.x
                dy = trp.sprite.y - self.sprite.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist <= self.alcance and dist < menor_dist:
                    trp.velocidade = trp.velocidade0*1.5
        else:
            for ini in inimigos:
                dx = ini.sprite.x - self.sprite.x
                dy = ini.sprite.y - self.sprite.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist <= self.alcance and dist < menor_dist: #verifica se ha inimigos dentro do alcance e seta o alvo para o mais proximo
                    menor_dist = dist
                    if ini.aereo == True and self.aereo == False: #verifica se o alvo eh aereo e a tropa nao eh aereo
                        alvo = None
                    else:
                        alvo = ini
            if alvo:
                dx = alvo.sprite.x - self.sprite.x
                dy = alvo.sprite.y - self.sprite.y
                self.sprite.rotation = math.degrees(math.atan2(-dy, dx)) #gira a tropa de acordo com a direção do alvo
                self.tiros.append(
                    Tiro(self.sprite.x, self.sprite.y, alvo, self.dano, self.danoesp,self.raio,self.slow, self.spritetiro,
                        caminho_explosao=self.spriteexplosao, frames_explosao=self.framesexplosao) #dispara o tiro
                )
                self.somtiro.play()

    def update(self, janela, inimigos, vetor): #roda em loop para atualizar a tropa
        self.sprite.draw() #desenha a tropa
        # velocidade controla cadência: quanto maior, mais rápido atira
        self.cooldown += self.velocidade * janela.delta_time()
        if self.cooldown >= 10:
            self.cooldown = 0
            self.atirar(inimigos, vetor) #dispara o loop de atirar
        self.tiros = [t for t in self.tiros if t.ativo]
        for tiro in self.tiros: #atualiza o tiro daquela tropa
            tiro.update(inimigos,)

    def criarSoldado(x, y): #cria um soldado
        trop = tropa('soldado', 100, 25, 0, 150, 10, 1,1, False, Sprite('imagens/soldado.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3'))
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop
    def criarSolari(x,y):
        trop = tropa('solari',150,25,25,150,10,1,1,True, Sprite('imagens/solari.png'), 'imagens/tiroSolari.png', Sound('sons/som_tiro_S.mp3'))
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop
    def criarEclipse(x,y):
        trop = tropa('eclipse',300,10,10,100,5,99,1.5,True, Sprite('imagens/Solari_Eclipse.png'), 'imagens/tiro_eclipse.png', Sound('sons/somEclipse.mp3'),
                     spriteexplosao='imagens/explosaoSlow2.png', framesexplosao=14)
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop
    def criarGranadeiro(x,y):
        
        trop = tropa('granadeiro',300,50,0,100,5,100,1,False, Sprite('imagens/granadeiro.png'), 'imagens/granada.png', Sound('sons/som_tiro_S.mp3'),
                      spriteexplosao='imagens/explosao_sheet.png', framesexplosao=14) #adiciona a animação de explosão apenas no granadeiro
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop
    def criarCaca(x,y):
        trop = tropa('caça',500, 100 ,0, 250,15,1,1,True, Sprite('imagens/nave_de_caca.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3'))
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop
    def criarCacaSolari(x,y):
        
        trop = tropa('caça solari',500, 100, 55, 250,15,1,1,True, Sprite('imagens/nave_solari.png'), 'imagens/tiroSolari2.png', Sound('sons/som_naveS.mp3'))
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop
    def criarSniper(x,y):
        trop = tropa('Sniper',650, 200 ,0, 400, 5,1,1,True, Sprite('imagens/sniper.png'), 'imagens/tiro.png', Sound('sons/sniper.mp3'))
        trop.sprite.set_position(x- trop.sprite.width/2, y - trop.sprite.height/2)
        return trop
    def criarTorre(x,y):
        trop = tropa('Torre',1000, 0, 0, 250, 50, 1, 1 ,False, Sprite('imagens/torre_solari.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3'))
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
        trp.update(janela, inimigos, vetor)