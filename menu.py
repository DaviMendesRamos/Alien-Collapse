from PPlay.sprite import *
from PPlay.window import *
from PPlay.mouse import *
from tropas import*


import historia
import colapso
vetCompradas = [tropa('soldado', 100, 25, 25, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png')]
vetEquipadas = [tropa('soldado', 100, 25, 25, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png')]



def menu(creditos):
    width = 800
    height = 600
    vetLoja = [tropa('soldado', 100, 25, 25, 150, 1, Sprite('imagens/soldado.png'), 'imagens/tiro.png'), tropa('solari',150,25,25,150,1, Sprite('imagens/solari.png'), 'imagens/tiro.png')]
    background = (100, 150, 120)
    janela = Window(width, height)
    janela.set_title("Menu Principal")

    btnhistoria = Sprite('imagens/btnhistoria.png')
    btncolapso = Sprite('imagens/btncolapso.png')
    btnsair = Sprite('imagens/btnsair.png')
    
    
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
    loja =Sprite('imagens/loja (2).png')
    loja.set_position(330,120)
    mouse = Mouse()
    
    
    cooldown_clique = 0

    while True:
        
        for i in range(2):
            for j in range(2):
                vetLoja[i].sprite.set_position(i*100,j*100)
                janela.draw_text(f'preço: {vetLoja[i].custo}',i*100, j*100-10)
        for tropa in vetLoja:
            tropa.sprite.draw()
        if cooldown_clique > 0:
            cooldown_clique -= janela.delta_time()

       
        if mouse.button_pressed(1) and cooldown_clique <= 0:
            if mouse.is_over_object(btnhistoria):

                creditos = historia.loop(janela, vetBaralho, creditos) 
                cooldown_clique = 0.5 
                
            elif mouse.is_over_object(btncolapso):
                
                colapso.loop(janela)
                cooldown_clique = 0.5
                
            elif mouse.is_over_object(btnsair):
                break 
        janela.draw_text(f'Creditos : {creditos}',100,100)
        janela.set_background_color(background)
        loja.draw()
        btnhistoria.draw()
        btncolapso.draw()
        btnsair.draw()
        janela.update()
    return creditos

# Executa o menu apenas se este arquivo for o principal
if __name__ == "__main__":
    creditos = 0
    creditos = menu(creditos)