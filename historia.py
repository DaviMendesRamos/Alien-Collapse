from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
from PPlay.mouse import *
import pygame
from inimigos import *
from tropas import *



def loop(janela,baralho,creditos):
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
    portao=Portao(100)
    portao.sprite.rotation = 270
    portao.sprite.set_position(705, 470)

    keyboard = Keyboard()
    click_cooldown = 0
    onda = 0
    onda_atual= [Orda([
        inimigo.criarDravok(),
        inimigo.criarDravok(),
        inimigo.criarDravok(),
        inimigo.criarPesado(),
    ]),
    Orda([
        inimigo.criarDravok(),
        inimigo.criarDravok(),
        inimigo.criarPesado(),
        inimigo.criarPesado(),
        inimigo.criarPesado(),
        inimigo.criarPesado(),
        inimigo.criarDravok()
        ])
    ]

    while running:
        if keyboard.key_pressed("ESC"):
            break

        teste.draw()
        portao.sprite.draw()
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
        janela.draw_text(f'Vida do Portão: {portao.vida}',150,20)
        if onda <2:
            money, onda = onda_atual[onda].update(janela,money,onda)#atualiza a onda
            if onda<2:
                loopTrp(janela, vetor, onda_atual[onda].vet)#passa o vetor de tropas e o vetor de inimigos ativos e atualiza as tropas
                if (portao.chegouPortao(onda_atual[onda].vet)):
                    janela.update()
                    break
            
        else:
            break

        janela.update()
    if len(onda_atual[onda-1].vet) <=0 :
        
        creditos = creditos + (onda*10)
        return creditos
    else:
        creditos = creditos + ((onda-1)*10)
