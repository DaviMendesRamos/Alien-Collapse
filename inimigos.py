import PPlay
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
import pygame
import math

# Caminho predefinido: lista de (x, y) que os inimigos seguem em ordem
CAMINHO = [
    (0, 129),   # entrada (fora da tela, topo)
    (100, 129),
    (100, 520),
    (280, 520),
    (280, 70),
    (515, 70),
    (646, 337),
    (640, 514),
    (773, 514),  # destino final (portão)
]


class inimigo():
    def __init__(self, nome, vida, dinheiro, escudo, velocidade, sprite):
        self.nome = nome
        self.vida = vida
        self.dinheiro = dinheiro
        self.escudo = escudo
        self.velocidade = velocidade
        self.sprite = sprite
        self.waypoint_idx = 1  # começa mirando no segundo ponto (já está no primeiro)

    def seguir_caminho(self):
        if self.waypoint_idx >= len(CAMINHO):
            return

        alvo_x, alvo_y = CAMINHO[self.waypoint_idx]
        dx = alvo_x - self.sprite.x
        dy = alvo_y - self.sprite.y
        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia < self.velocidade * 2:
            self.waypoint_idx += 1
        else:
            self.sprite.rotation = math.degrees(math.atan2(-dy, dx))
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
        return self.vida <- 0 
        

    def criarDravok():
        ini = inimigo('dravok', 100, 100, 0, 2, Sprite('imagens/dravok.png'))
        ini.sprite.set_position(*CAMINHO[0])
        return ini

    def criarPesado():
        ini = inimigo('dravok pesado', 400, 400, 0, 1, Sprite('imagens/Pesado.png'))
        ini.sprite.set_position(*CAMINHO[0])
        return ini


class Orda:
    def __init__(self, Onda):
        self.Onda = Onda
        self.vet = []
        self.cooldown = 0

    def update(self, janela, money):
        self.cooldown += 100 * janela.delta_time()

        if self.cooldown > 500:
            self.cooldown = 0
            if self.Onda:
                ini = self.Onda.pop(0)
                self.vet.append(ini)
        for i in self.vet:
            for ini in self.vet:
                if ini.morreu():
                    money += ini.dinheiro
        self.vet = [ini for ini in self.vet if not ini.morreu()]
        for ini in self.vet:
            ini.seguir_caminho()
            ini.sprite.draw()
        return money
