from PPlay.gameimage import GameImage
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.sound import*


def mostrarIntro(janela, caminhos_imagens, duracao_por_imagem=3):
    """Exibe uma sequencia de imagens em tela cheia, uma apos a outra,
    antes da fase comecar (ex: historia, creditos de abertura, etc).

    caminhos_imagens: lista de strings com o caminho de cada imagem, em ordem.
    duracao_por_imagem: quantos segundos cada imagem fica na tela.

    Clique do mouse -> pula pra proxima imagem.
    ESC -> pula a intro inteira.
    """
    keyboard = Keyboard()
    mouse = Mouse()
    somS= Sound('sons/somSuspense.mp3')
    somS.play()
    for caminho in caminhos_imagens:
        imagem = GameImage(caminho)
        imagem.scale_x = janela.width / imagem.width
        imagem.scale_y = janela.height / imagem.height
        imagem.set_position(0, 0)

        tempo_restante = duracao_por_imagem

        while tempo_restante > 0:
            if keyboard.key_pressed("ESC"):
                return  # pula a intro toda, sai da funcao

            imagem.draw()
            janela.update()

            if mouse.button_pressed(mouse.RIGHT):
                break  # pula pra proxima imagem da lista

            tempo_restante -= janela.delta_time()

    somS.stop()