from PPlay.sprite import *
from PPlay.window import *
from PPlay.mouse import *
from tropas import*
import historia
import colapso

def menu(creditos):
    width = 800
    height = 600
    
    background = (100, 150, 120)
    janela = Window(width, height)
    janela.set_title("Menu Principal")

    btnhistoria = Sprite('imagens/btnhistoria.png')
    btncolapso = Sprite('imagens/btncolapso.png')
    btnsair = Sprite('imagens/btnsair.png')
    vetEquipadas = [tropa('soldado', 100, 25, 25, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png')]
    vetCompradas = [tropa('soldado', 100, 25, 25, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png')]
    vetLoja = [tropa('soldado', 100, 25, 25, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png'),
                tropa('solari',150,25,25,150,1, Sprite('imagens/solari.png'), 'imagens/tiro.png')]
    
    escala_botoes = 0.2
    escala_sair = 0.5
    
    btnhistoria.scale_x = escala_botoes
    btnhistoria.scale_y = escala_botoes
    btncolapso.scale_x = escala_botoes
    btncolapso.scale_y = escala_botoes
    btnsair.scale_x = escala_sair
    btnsair.scale_y = escala_sair
    
    btnhistoria.set_position(width/2 - (btnhistoria.width * escala_botoes / 2), height/2 - 80)
    btncolapso.set_position(width/2 - (btncolapso.width * escala_botoes / 2), height/2)
    btnsair.set_position(width/2 - (btnsair.width * escala_sair / 2), height/2 + 80)
    mouse = Mouse()
    
    
    cooldown_clique = 0

    while True:
        
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
                if creditos > vetLoja[i].custo:
                    if not any(t.nome == vetLoja[i].nome for t in vetCompradas):
                        creditos -= vetLoja[i].custo
                        vetCompradas.append(vetLoja[i])
                        vetEquipadas.append(vetLoja[i])

                    cooldown_clique = 0
                else:
                    cooldown_clique = 0
                    janela.draw_text('Sem creditos', 100, 100)
                    janela.update()
       
        if mouse.button_pressed(1) and cooldown_clique >= 1:
            if mouse.is_over_object(btnhistoria):
                creditos = historia.loop(janela, vetEquipadas, creditos) 
                cooldown_clique = 0 
                
            elif mouse.is_over_object(btncolapso):
                colapso.loop(janela)
                cooldown_clique = 0
                
            elif mouse.is_over_object(btnsair):
                break 
        janela.draw_text(f'Creditos : {creditos}',100,50, tamanho =15)
        janela.set_background_color(background)
        btnhistoria.draw()
        btncolapso.draw()
        btnsair.draw()
        janela.update()
    return creditos

# Executa o menu apenas se este arquivo for o principal
if __name__ == "__main__":
    creditos = 1000
    creditos = menu(creditos)