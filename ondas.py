from inimigos import*

from PPlay.sprite import*





def criar_ondas():
    return [
        Orda([
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
        ]),
        Orda([
            inimigo.criarDravok(),
            inimigo.criarDravok(),
            inimigo.criarPesado(),
            inimigo.criarPesado(),
            inimigo.criarPesado(),
            inimigo.criarDravok(),
            inimigo.criarDravok(),
            inimigo.criarDravok(),
            inimigo.criarDravok(),
            inimigo.criarDravok(),
            inimigo.criarDravok(),
            inimigo.criarDravok()
        ])
    ]