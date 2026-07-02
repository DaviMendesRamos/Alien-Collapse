import PPlay
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
import pygame
import math
from mensagem import*

# Caminho predefinido: lista de (x, y) que os inimigos seguem em ordem
CAMINHO = [
    (0, 70),   # entrada (fora da tela, topo)
    (70, 70),
    (70, 470),
    (265, 470),
    (265, 60),
    (470, 60),
    (470, 330),
    (600, 330),
    (600, 480),
    (750, 480),  # destino final (portão)
]


class inimigo():
    def __init__(self, nome, vida, dinheiro, escudo, velocidade, aereo,waypoint_idx, sprite):
        self.nome = nome
        self.vida = vida
        self.dinheiro = dinheiro
        self.escudo = escudo
        self.velocidade = velocidade
        self.velocidade0 = velocidade
        self.aereo = aereo
        self.sprite = sprite
        self.waypoint_idx = waypoint_idx  # começa mirando no segundo ponto (já está no primeiro)

    def seguir_caminho(self):
        if self.waypoint_idx >= len(CAMINHO):
            return

        alvo_x, alvo_y = CAMINHO[self.waypoint_idx]
        dx = alvo_x - self.sprite.x
        dy = alvo_y - self.sprite.y
        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia < self.velocidade * 2:
            self.waypoint_idx += 1
        elif not self.nome=='dravok rei':
            self.sprite.rotation = math.degrees(math.atan2(-dy, dx))
            self.sprite.x += (dx / distancia) * self.velocidade
            self.sprite.y += (dy / distancia) * self.velocidade
        else:
            self.sprite.x += (dx / distancia) * self.velocidade
            self.sprite.y += (dy / distancia) * self.velocidade
            

    def chegou(self):
        return self.waypoint_idx >= len(CAMINHO)

    def receber_dano(self, dano, danoesp):
        if self.escudo > 0:
            self.escudo -= danoesp
            if self.escudo < 0:
                self.escudo = 0
        else:
            self.vida -= dano

    def morreu(self):
        return self.vida <= 0 
        

    def criarDravok(pos = CAMINHO[0], waypoint=1):
        ini = inimigo('dravok', 100, 50, 0, 1,False,waypoint,Sprite('imagens/dravok.png'))
        ini.sprite.set_position(*pos)
        return ini

    def criarPesado(pos = CAMINHO[0],waypoint=1):
        ini = inimigo('dravok pesado', 400, 150, 0, 0.5,False,waypoint, Sprite('imagens/Pesado.png'))
        ini.sprite.set_position(*pos)
        return ini
    def criarVoador(pos = CAMINHO[0],waypoint=1):
        ini = inimigo('dravok voador', 200, 150, 0, 1.5,True,waypoint, Sprite('imagens/dravok_voador.png'))
        ini.sprite.set_position(*pos)
        return ini
    def criarAfobado(pos = CAMINHO[0],waypoint=1):
        ini = inimigo('dravok afobado', 50, 25, 50, 2.5,False,waypoint, Sprite('imagens/afobado.png'))
        ini.sprite.set_position(*pos)
        return ini
    def criarCamburao(pos = CAMINHO[0],waypoint=1):
        ini = inimigo('dravok camburao', 3000, 1500, 50, 0.5,False,waypoint, Sprite('imagens/camburao.png'))
        ini.sprite.set_position(*pos)
        return ini
    def criarRei(pos = CAMINHO[0],waypoint=1):
        ini = inimigo('dravok rei', 30000, 15000, 15000, 0.6,False,waypoint, Sprite('imagens/rei_dravok.png'))
        ini.sprite.set_position(*pos)
        return ini



class Orda:

    def __init__(self, Onda):
        self.Onda = Onda
        self.vet = []
        self.cooldown = 0
        self.finalizada = False

    def update(self, janela, money, onda, portaovida):

        self.cooldown += 100 * janela.delta_time()

        if self.cooldown > 80:
            self.cooldown = 0

            if self.Onda:
                ini = self.Onda.pop(0)
                self.vet.append(ini)

        for ini in self.vet:
            if ini.morreu():
                money += ini.dinheiro
                if ini.nome == 'dravok camburao':
                    contador =0
                    for pos in CAMINHO:
                        if ini.sprite.x > pos[0] or ini.sprite.y > pos[1]:
                            contador+=1
                        else:
                            break
                    self.vet.append(inimigo.criarDravok(pos = (ini.sprite.x, ini.sprite.y),waypoint=contador))
                    self.vet.append(inimigo.criarPesado(pos = (ini.sprite.x, ini.sprite.y),waypoint=contador))
                    self.vet.append(inimigo.criarVoador(pos = (ini.sprite.x, ini.sprite.y),waypoint=contador))
                    self.vet.append(inimigo.criarAfobado(pos = (ini.sprite.x, ini.sprite.y),waypoint=contador)) 
                if ini.nome=='dravok rei':
                    mostrarMensagem('Parabens, Voce derrotou os Dravoks', janela.width/2, janela.height/2, janela, 0.8)

        self.vet = [ini for ini in self.vet if not ini.morreu()]

        for ini in self.vet:
            ini.seguir_caminho()
            ini.sprite.draw()

        # wave terminou
        if len(self.vet) == 0 and len(self.Onda) == 0 and not self.finalizada:
            onda += 1
            portaovida+=20
            self.finalizada = True

        return money, onda, portaovida
