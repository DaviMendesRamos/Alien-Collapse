from PPlay.sprite import *
from PPlay.window import *
from PPlay.mouse import *
from tropas import*
from PPlay.gameimage import*
import historia
import colapso
from mensagem import*
from intro import mostrarIntro

def menu(creditos):
    width = 800
    height = 600
    
    Quadrinhos=True
    background = (100, 150, 120)
    janela = Window(width, height)
    janela.set_title("Menu Principal")
    teste = GameImage('imagens/menu_fundo.png')
    teste.scale_x = 800 / teste.width
    teste.scale_y = 600 / teste.height
    titulo = Sprite('imagens/titulo.png')
    titulo.set_position(width/2- titulo.width/2,40)
    btnhistoria = Sprite('imagens/modo_historia_fundo.png')
    btncolapso = Sprite('imagens/modo_colapso_fundo.png')
    btnsair = Sprite('imagens/sair.png')
    loja = Sprite('imagens/loja.png')
    loja.set_position(570, 20)
    equipados = Sprite('imagens/equipados.png')
    equipados.set_position(45, 20)
    MoneyR= Sprite('imagens/retanguloP.png')
    MoneyR.set_position(620, 70)
    vetCompradas = [tropa('soldado', 100, 25, 0, 150, 10, 1,1, False, Sprite('imagens/soldado.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3'))]
    vetEquipadas = vetCompradas.copy()
    vetEquipadasQ = [Sprite('imagens/quadrado.png'), Sprite('imagens/quadrado.png'), Sprite('imagens/quadrado.png'),Sprite('imagens/quadrado.png'),
               Sprite('imagens/quadrado.png'), Sprite('imagens/quadrado.png'), Sprite('imagens/quadrado.png'),Sprite('imagens/quadrado.png')]
    
    vetLoja = [tropa('soldado', 100, 25, 0, 150, 10, 1,1, False, Sprite('imagens/soldado.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3')),
                tropa('solari',150, 25 ,25, 150, 10, 1, 1,True, Sprite('imagens/solari.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3')),
                tropa('eclipse', 300, 10, 10, 150, 5, 99, 1.5,True, Sprite('imagens/Solari_Eclipse.png'), 'imagens/tiro_eclipse.png', Sound('sons/som_tiro_S.mp3')),
                tropa('granadeiro', 300, 50, 0, 150, 5, 100, 1, False, Sprite('imagens/granadeiro.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3')),
                tropa('caça', 500, 75 ,0, 150, 15, 1, 1, True, Sprite('imagens/nave_de_caca.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3')),
                tropa('caça solari',500, 75, 75, 150, 15, 1, 1, True, Sprite('imagens/nave_solari.png'), 'imagens/tiro.png', Sound('sons/som_naveS.mp3')),
                tropa('Sniper',650, 200 ,0, 400, 5,1,1,True, Sprite('imagens/sniper.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3')),
                tropa('Torre',1000, 0, 0, 250, 50, 1, 1 ,False, Sprite('imagens/torre_solari.png'), 'imagens/tiro.png', Sound('sons/som_tiro_S.mp3'))]
    vetLojaQ=[Sprite('imagens/quadrado.png'), Sprite('imagens/quadrado.png'), Sprite('imagens/quadrado.png'),Sprite('imagens/quadrado.png'),
               Sprite('imagens/quadrado.png'), Sprite('imagens/quadrado.png'), Sprite('imagens/quadrado.png'),Sprite('imagens/quadrado.png')]
    Mfundo = Music('sons/musicaFundo.mp3')
    Mfundo.play(-1)
    btnhistoria.set_position(width/2 - btnhistoria.width/2 , height/2 - 80)
    btncolapso.set_position(width/2 - (btncolapso.width/2), height/2)
    btnsair.set_position(width/2 - (btnsair.width/2), height/2 + 80)
    mouse = Mouse()
    
    
    cooldown_clique = 0

    while True:
        teste.draw()
        indice = 0

        for i in range(4):
            for j in range(2):

                if indice >= len(vetLoja):
                    break

                x = j * 100 + 600
                y = i * 100 + 130

                vetLoja[indice].sprite.set_position(x, y)
                vetLojaQ[indice].set_position(x-18, y-25)
                
                
                vetLojaQ[indice].draw()
                vetLoja[indice].sprite.draw()
                janela.draw_text(f'Preço: {vetLoja[indice].custo}',x-5,y - 12, cor = (100,200,250), fonte='daydream', tamanho=15)
                if vetLoja[indice] in vetCompradas or vetLoja[indice].nome =='soldado':
                    janela.draw_text('Comprado',x-5,y - 24, cor = (100,200,250), fonte='daydream',tamanho=15)

                indice += 1
        indice = 0
        for i in range(4):
            for j in range(2):

                if indice >= len(vetEquipadas):
                    break

                x = j * 100 + 60
                y = i * 100 + 110
                vetEquipadasQ[indice].set_position(x-18, y-15)
                vetEquipadas[indice].sprite.set_position(x, y)
                vetEquipadasQ[indice].draw()
                vetEquipadas[indice].sprite.draw()
                

                indice += 1
        cooldown_clique += janela.delta_time() *2
         
        for i in range(len(vetLoja)):
            if mouse.is_over_object(vetLoja[i].sprite) and mouse.button_pressed(1) and cooldown_clique > 1:

                # Não comprou ainda
                if not any(t.nome == vetLoja[i].nome for t in vetCompradas):

                    if creditos >= vetLoja[i].custo:
                        creditos -= vetLoja[i].custo
                        vetCompradas.append(vetLoja[i])
                    else:
                        mostrarMensagem('Creditos insuficientes', janela.width/2, janela.height/2, janela, 0.8,fundo=teste)

                # Comprou mas não equipou
                elif not any(t.nome == vetLoja[i].nome for t in vetEquipadas) and len(vetEquipadas) < 5:
                    vetEquipadas.append(vetLoja[i])
                elif not any(t.nome == vetLoja[i].nome for t in vetEquipadas) and len(vetEquipadas) >= 5:
                    mostrarMensagem('Limite de tropas atingido', janela.width/2, janela.height/2, janela, 0.8,fundo=teste)
                

                # Já está equipada → desequipa
                else:
                    for trop in vetEquipadas:
                        if trop.nome == vetLoja[i].nome:
                            vetEquipadas.remove(trop)
                            break

                cooldown_clique = 0
        
       
        if mouse.button_pressed(1) and cooldown_clique >= 1:
            if mouse.is_over_object(btnhistoria):
                colapso=False
                if Quadrinhos==True:
                    Mfundo.pause()

                    mostrarIntro(janela, [
                        'imagens/Slide1.jpg',
                        'imagens/Slide2.jpg',
                        'imagens/Slide3.jpg',
                        'imagens/Slide4.jpg',
                        'imagens/Slide5.jpg',
                        'imagens/Slide6.jpg',
                        'imagens/Slide7.jpg',
                        'imagens/Slide8.jpg',
                        'imagens/Slide9.jpg',
                    ], duracao_por_imagem=3)
                    Quadrinhos=False
                    Mfundo.play()
                creditos = historia.loop(janela, vetEquipadas, creditos,colapso , Mfundo) 
                cooldown_clique = 0 
                
            elif mouse.is_over_object(btncolapso):
                colapso=True
                creditos = historia.loop(janela, vetEquipadas, creditos,colapso ,Mfundo)
                cooldown_clique = 0
                
            elif mouse.is_over_object(btnsair):
                break 
        loja.draw()
        equipados.draw()
        MoneyR.draw()
        janela.draw_text(f'Creditos : {creditos}',630,75, cor = (50,200,50), fonte='daydream', tamanho =15)
        janela.set_background_color(background)
        titulo.draw()
        btnhistoria.draw()
        btncolapso.draw()
        btnsair.draw()
        janela.update()
    return creditos

# Executa o menu apenas se este arquivo for o principal
if __name__ == "__main__":
    creditos = 500
    creditos = menu(creditos)