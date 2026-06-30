from PPlay.sprite import *
from PPlay.window import *
from PPlay.mouse import *
from tropas import*
from PPlay.gameimage import*
import historia
import colapso

def menu(creditos):
    width = 800
    height = 600
    
    
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
    btnsair = Sprite('imagens/btnsair.png')
    vetCompradas = [tropa('soldado', 100, 25, 25, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png')]
    vetEquipadas = vetCompradas.copy()
    
    vetLoja = [tropa('soldado', 100, 25, 25, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png'),
                tropa('solari',150,25,25,150,1, Sprite('imagens/solari.png'), 'imagens/tiro.png')]
    

    
    btnhistoria.set_position(width/2 - btnhistoria.width/2 , height/2 - 80)
    btncolapso.set_position(width/2 - (btncolapso.width/2), height/2)
    btnsair.set_position(width/2 - (btnsair.width/2), height/2 + 80)
    mouse = Mouse()
    
    
    cooldown_clique = 0

    while True:
        teste.draw()
        indice = 0

        for i in range(2):
            for j in range(2):

                if indice >= len(vetLoja):
                    break

                x = j * 100 + 540
                y = i * 100 + 80

                vetLoja[indice].sprite.set_position(x, y)
                janela.draw_text(f'Preço: {vetLoja[indice].custo}',x,y - 10)
                vetLoja[indice].sprite.draw()

                indice += 1
        indice = 0
        janela.draw_text('Tropas Equipadas', 100, 100, tamanho=20, cor=(0,0,0))
        for i in range(2):
            for j in range(2):

                if indice >= len(vetEquipadas):
                    break

                x = j * 100 + 100
                y = i * 100 + 120

                vetEquipadas[indice].sprite.set_position(x, y)
                vetEquipadas[indice].sprite.draw()

                indice += 1
        cooldown_clique += janela.delta_time()
         
        for i in range(len(vetLoja)):
            if mouse.is_over_object(vetLoja[i].sprite) and mouse.button_pressed(1) and cooldown_clique > 1:

                # Não comprou ainda
                if not any(t.nome == vetLoja[i].nome for t in vetCompradas):

                    if creditos >= vetLoja[i].custo:
                        creditos -= vetLoja[i].custo
                        vetCompradas.append(vetLoja[i])
                    else:
                        janela.draw_text('Sem creditos', 100, 100)

                # Comprou mas não equipou
                elif not any(t.nome == vetLoja[i].nome for t in vetEquipadas):
                    vetEquipadas.append(vetLoja[i])

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
                creditos = historia.loop(janela, vetEquipadas, creditos,colapso ) 
                cooldown_clique = 0 
                
            elif mouse.is_over_object(btncolapso):
                colapso=True
                creditos = historia.loop(janela, vetEquipadas, creditos,colapso )
                cooldown_clique = 0
                
            elif mouse.is_over_object(btnsair):
                break 
        
        janela.draw_text(f'Creditos : {creditos}',100,50, tamanho =15)
        janela.set_background_color(background)
        titulo.draw()
        btnhistoria.draw()
        btncolapso.draw()
        btnsair.draw()
        janela.update()
    return creditos

# Executa o menu apenas se este arquivo for o principal
if __name__ == "__main__":
    creditos = 1000
    creditos = menu(creditos)