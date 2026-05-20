from PPlay.sprite import *
from PPlay.window import *
from PPlay.mouse import *


import historia
import colapso

def menu():
    width = 800
    height = 600

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
    
    mouse = Mouse()
    

    cooldown_clique = 0

    while True:
        
        if cooldown_clique > 0:
            cooldown_clique -= janela.delta_time()

       
        if mouse.button_pressed(1) and cooldown_clique <= 0:
            if mouse.is_over_object(btnhistoria):
                
                historia.loop(janela) 
                cooldown_clique = 0.5 
                
            elif mouse.is_over_object(btncolapso):
                
                colapso.loop(janela)
                cooldown_clique = 0.5
                
            elif mouse.is_over_object(btnsair):
                break 

        janela.set_background_color(background)
        btnhistoria.draw()
        btncolapso.draw()
        btnsair.draw()
        janela.update()


if __name__ == "__main__":
    menu()