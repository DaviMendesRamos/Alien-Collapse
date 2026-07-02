from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.timer import *
import pygame
from inimigos import *
from tropas import *
from grid import Grid
import ondas
import colapso
from dadostrp import*
from mensagem import*
from grid import*




def loop(janela,baralho,creditos, colapsoCon,Mfundo):
    vetor = []
    mouse = Mouse()
    trpSelected = ''
    running = True
    money = 500
    teste = GameImage('imagens/mapa2.png')
    teste.scale_x = 800 / teste.width
    teste.scale_y = 600 / teste.height
    portao=Portao(1000)
    portao.sprite.rotation = 270
    portao.sprite.set_position(705, 470)
    retangulo = Sprite('imagens/retangulo.png')
    retangulo.set_position(janela.width/2 - retangulo.width/2,10)
    perdeu = Sprite('imagens/retangulo.png')
    perdeu.set_position(janela.width/2 - perdeu.width/2,400)
    vendendo = False
    vetBaralho1 = [Sprite('imagens/quadradoP.png'), Sprite('imagens/quadradoP.png'), Sprite('imagens/quadradoP.png'),Sprite('imagens/quadradoP.png'),
                Sprite('imagens/quadradoP.png')]

    # --- Grid de posicionamento ---
    # ajuste origem/colunas/linhas/tam_celula conforme o layout real do seu mapa.png
    grid = Grid(origem_x=0, origem_y=0, colunas=12, linhas=9, tam_celula=66,
                celulas_bloqueadas=[(0, 1), (1, 1), (1, 2), (1, 6), (1, 7),(2, 7), (3, 7), (4, 7), (4, 6), (4, 5),(0, 6),
                (4, 4), (4, 3), (4, 2), (4, 1),(5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5),(6, 6),(9, 2),
                (8, 5), (9, 5), (9, 6), (9, 7), (10, 7),(8, 8),(10, 2), (10, 3),(9, 0), (10, 0),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)],
                sniper=[(0,0),(1,0),(0,7),(2,4),(5,2),(6,3),(6,4),(7,7),(8,7),(8,3),(8,4),(9,4),(9,3),(3,1),(2,1),(2,6),(3,6)])  # coloque aqui as células do caminho dos inimigos

    keyboard = Keyboard()
    click_cooldown = 0
    onda = 0
    if colapsoCon == True:
        onda_atual = colapso.criar_ondas(onda)
    else:
        onda_atual = ondas.criar_ondas()
    

    while running:
        if keyboard.key_pressed("ESC"):
            break
        if mouse.button_pressed(mouse.RIGHT) and click_cooldown <= 0:
            trpSelected = ''

        teste.draw()
        portao.sprite.draw()
        a,b = mouse.get_position()

        click_cooldown -= 100* janela.delta_time()

        for i in range (len(baralho)):
            vetBaralho1[i].transparency = 140
            vetBaralho1[i].draw()
            vetBaralho1[i].set_position(i*70 + 240,540)
            baralho[i].sprite.draw()
            baralho[i].sprite.set_position(i*70 + 250,550)

        for trp in baralho:

            if mouse.button_pressed(mouse.LEFT) and click_cooldown <= 0:#verifica o clique e o cooldown
                if mouse.is_over_object(trp.sprite): # se tiver clicado em soldado seleciona o mesmo
                    # clique no ícone: seleciona a tropa
                    trpSelected = trp.nome
                    click_cooldown = 80
        for trp1 in vetor:
             if mouse.button_pressed(mouse.LEFT) and click_cooldown <= 0:#verifica o clique e o cooldown
                if mouse.is_over_object(trp1.sprite): # se tiver clicado em soldado seleciona o mesmo
                    vendendo = True
                    tropaVenda=trp1
                    click_cooldown = 80
        if vendendo == True:
            vetor, grid,money,fim= VenderTropa(tropaVenda,vetor,janela,mouse,grid,money)
            if fim == True:
                vendendo = False
        # --- Mostra o grid enquanto o jogador está prestes a colocar uma tropa ---
        if trpSelected != '':
            sniper = (trpSelected == 'Sniper')
            grid.draw(janela, alpha=70, sniper_ativo=sniper)
            grid.draw_highlight(janela, a, b, sniper=sniper, alpha=90)

            celula_atual = grid.pixel_para_celula(a, b)
            if celula_atual is not None:
                col, lin = celula_atual
                cx, cy = grid.celula_para_pixel(col, lin)

                trp_selecionada = next((t for t in baralho if t.nome == trpSelected), None)
                if trp_selecionada is not None:
                    desenhar_alcance(janela, cx, cy, trp_selecionada.alcance)

        for trp in baralho:
            if mouse.is_over_object(trp.sprite):
                mostrarTropa(trp.nome, baralho,janela)
        # Coloca a tropa no grid
        if mouse.button_pressed(mouse.LEFT) and click_cooldown <= 0:

            mx, my = mouse.get_position()
            celula = grid.pixel_para_celula(mx, my)

            if celula is not None and trpSelected != '':
                col, lin = celula
                if trpSelected == 'Sniper':
                    sniper = True
                else:
                    sniper = False
                if grid.celula_disponivel(col, lin,sniper):

                    for trp in baralho:

                        if trpSelected == trp.nome and money >= trp.custo:

                            x, y = grid.celula_para_pixel(col, lin)

                            if trp.nome == 'soldado':
                                    
                                nova_tropa = tropa.criarSoldado(x, y)
                                trpSelected = ''
                            elif trp.nome == 'solari':
                                nova_tropa = tropa.criarSolari(x, y)
                                trpSelected = ''
                            elif trp.nome == 'eclipse':
                                nova_tropa = tropa.criarEclipse(x, y)
                                trpSelected = ''
                            elif trp.nome == 'granadeiro':
                                nova_tropa = tropa.criarGranadeiro(x, y)
                                trpSelected = ''
                            elif trp.nome == 'caça':
                                nova_tropa = tropa.criarCaca(x, y)
                                trpSelected = ''
                            elif trp.nome == 'caça solari':
                                nova_tropa = tropa.criarCacaSolari(x, y)
                                trpSelected = ''
                            elif trp.nome == 'Sniper':
                                nova_tropa = tropa.criarSniper(x, y)
                                trpSelected = ''
                            elif trp.nome=='Torre':
                                nova_tropa = tropa.criarTorre(x, y)
                                trpSelected = ''

                            vetor.append(nova_tropa)
                            grid.ocupar_celula(col, lin, nova_tropa)
                            money -= trp.custo
                            click_cooldown = 100
                            break
                        elif trpSelected == trp.nome and money < trp.custo:
                            mostrarMensagem('dinheiro insuficiente', janela.width/2, janela.height/2, janela, 0.8,fundo = teste)
           
        retangulo.draw()
        janela.draw_text(f"Money: {money}", janela.width/2-30,13, color=(100,200,100),fonte= 'daydream', tamanho=20)
        janela.draw_text(f'Vida do Portão: {portao.vida}',janela.width/2 -30,30, color=(100,200,100), fonte= 'daydream',tamanho=20)
        janela.draw_text(f'ONDA: {onda+1}', janela.width/2 -90,30,color=(100,200,100), fonte= 'daydream',tamanho=20)
        if onda <3 and colapsoCon == False:
            money, onda, portao.vida = onda_atual[onda].update(janela,money,onda,portao.vida)#atualiza a onda
            if onda<3:
                loopTrp(janela, vetor, onda_atual[onda].vet)#passa o vetor de tropas e o vetor de inimigos ativos e atualiza as tropas
                if (portao.chegouPortao(onda_atual[onda].vet)):
                    janela.update()
                    break
            
        else:
            money, onda, portao.vida = onda_atual[onda].update(janela,money,onda, portao.vida)
            loopTrp(janela, vetor, onda_atual[onda].vet)
            if portao.chegouPortao(onda_atual[onda].vet):
                
                teste.draw()
                mostrarMensagem('Você foi derrotado', janela.width/2, janela.height/2, janela, 3, fundo = teste)
                janela.update()
                break
        
        janela.update()
    if len(onda_atual[onda-1].vet) <=0 :
        
        creditos = creditos + (onda*10)
        return creditos
    else:
        creditos = creditos + ((onda-1)*10)