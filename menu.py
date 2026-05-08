from PPlay.sprite import*
from PPlay.window import*
from PPlay.mouse import*
import historia
import pygame


def menu():
    width = 800
    height = 600

    background = (100,150,120)
    janela = Window(width, height)

    btnhistoria = Sprite('imagens/btnhistoria.png')
    btncolapso = Sprite('imagens/btncolapso.png')
    btnsair = Sprite('imagens/btnsair.png')
    btnhistoria.scale_x = 0.2
    btnhistoria.scale_y = 0.2
    btncolapso.scale_x = 0.2
    btncolapso.scale_y = 0.2
    btnsair.scale_x = 0.5
    btnsair.scale_y = 0.5
    btnhistoria.set_position(width/2 - (btnhistoria.width/2*0.2), height/2 -80)
    btncolapso.set_position(width/2 - (btncolapso.width/2*0.2), height/2 )
    btnsair.set_position(width/2 - (btnsair.width/2*0.5), height/2 +80)
    mouse = Mouse()
    while True:
        if mouse.is_over_object(btnhistoria) and mouse.button_pressed(1):
            historia.loop()

        if mouse.is_over_object(btncolapso) and mouse.button_pressed(1):
            janela.close()
            import colapso

        if mouse.is_over_object(btnsair) and mouse.button_pressed(1):
            break

        janela.set_background_color(background)
        btnhistoria.draw()
        btncolapso.draw()
        btnsair.draw()
        janela.update()
menu()