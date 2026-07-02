class Grid:
    """
    Grid de células para posicionamento de tropas.
    Converte posição do mouse em coordenadas de célula e controla
    quais células já estão ocupadas.
    """
    def __init__(self, origem_x, origem_y, colunas, linhas, tam_celula,
                 celulas_bloqueadas=None, sniper=None):
        self.origem_x = origem_x       # posição x onde o grid começa na tela
        self.origem_y = origem_y       # posição y onde o grid começa na tela
        self.colunas = colunas
        self.linhas = linhas
        self.tam_celula = tam_celula

        # dicionário: (coluna, linha) -> tropa ocupando a célula (ou None)
        self.ocupadas = {}

        # células que não podem receber tropas (ex: caminho dos inimigos)
        self.bloqueadas = set(celulas_bloqueadas) if celulas_bloqueadas else set()

        # células onde tropas do tipo sniper PODEM ser colocadas (exclusivo pra elas)
        self.sniper = set(sniper) if sniper else set()

    def celula_para_pixel(self, col, lin):
        """Retorna o centro (x, y) em pixels de uma célula do grid."""
        x = self.origem_x + col * self.tam_celula + self.tam_celula / 2
        y = self.origem_y + lin * self.tam_celula + self.tam_celula / 2
        return x, y

    def pixel_para_celula(self, x, y):
        """Converte uma posição em pixels para (coluna, linha) do grid.
        Retorna None se o ponto estiver fora dos limites do grid."""
        col = int((x - self.origem_x) // self.tam_celula)
        lin = int((y - self.origem_y) // self.tam_celula)

        if 0 <= col < self.colunas and 0 <= lin < self.linhas:
            return col, lin
        return None

    def celula_disponivel(self, col, lin, sniper=False):
        """Verifica se a célula existe, não está bloqueada e está livre.
        Se 'sniper' for True, a célula só é considerada disponível se
        estiver na lista de células permitidas para sniper (self.sniper)."""
        if not (0 <= col < self.colunas and 0 <= lin < self.linhas):
            return False
        if (col, lin) in self.bloqueadas:
            return False
        if sniper and (col, lin) not in self.sniper:
            return False
        if self.ocupadas.get((col, lin)) is not None:
            return False
        return True

    def ocupar_celula(self, col, lin, tropa_colocada):
        """Marca a célula como ocupada por uma tropa."""
        self.ocupadas[(col, lin)] = tropa_colocada

    def liberar_celula(self, col, lin):
        """Libera a célula (ex: quando a tropa morre/é vendida)."""
        if (col, lin) in self.ocupadas:
            del self.ocupadas[(col, lin)]

    def draw(self, janela, cor_linha=(255, 255, 255), cor_bloqueada=(120, 0, 0),
              cor_sniper_indisponivel=(80, 0, 0), alpha=255, sniper_ativo=False):
        """Desenha as linhas do grid inteiro na tela.
        Se 'sniper_ativo' for True, todas as células fora de self.sniper
        (as que não podem receber sniper) ficam pintadas de vermelho.
        alpha vai de 0 (invisível) a 255 (totalmente opaco)."""
        import pygame
        screen = janela.screen

        largura_total = self.colunas * self.tam_celula
        altura_total = self.linhas * self.tam_celula

        # superfície separada com canal alpha, onde as linhas serão desenhadas
        superficie = pygame.Surface((largura_total, altura_total), pygame.SRCALPHA)

        for col in range(self.colunas):
            for lin in range(self.linhas):
                rect = pygame.Rect(
                    col * self.tam_celula,
                    lin * self.tam_celula,
                    self.tam_celula,
                    self.tam_celula
                )
                if (col, lin) in self.bloqueadas:
                    pygame.draw.rect(superficie, (*cor_bloqueada, alpha), rect)
                elif sniper_ativo and (col, lin) not in self.sniper:
                    pygame.draw.rect(superficie, (*cor_sniper_indisponivel, alpha), rect)
                pygame.draw.rect(superficie, (*cor_linha, alpha), rect, 1)

        screen.blit(superficie, (self.origem_x, self.origem_y))

    def draw_highlight(self, janela, mx, my, sniper=False,
                        cor_disponivel=(0, 220, 0), cor_indisponivel=(220, 0, 0),
                        alpha=90):
        """Destaca a célula sob o mouse (mx, my): verde se disponível, vermelha se não.
        'sniper' deve indicar se a tropa selecionada no momento é do tipo sniper —
        nesse caso só fica verde se a célula estiver na lista de células
        permitidas para sniper (self.sniper) e não estiver ocupada.
        alpha vai de 0 (invisível) a 255 (totalmente opaco)."""
        import pygame
        screen = janela.screen

        celula = self.pixel_para_celula(mx, my)
        if celula is None:
            return

        col, lin = celula
        rect = pygame.Rect(
            self.origem_x + col * self.tam_celula,
            self.origem_y + lin * self.tam_celula,
            self.tam_celula,
            self.tam_celula
        )

        cor = cor_disponivel if self.celula_disponivel(col, lin, sniper) else cor_indisponivel

        # preenchimento semi-transparente por cima da célula
        superficie = pygame.Surface((self.tam_celula, self.tam_celula), pygame.SRCALPHA)
        superficie.fill((*cor, alpha))
        screen.blit(superficie, rect.topleft)
        pygame.draw.rect(screen, cor, rect, 2)


def desenhar_alcance(janela, x, y, alcance, cor=(255, 255, 255), alpha=60):
    """Desenha um círculo semi-transparente representando o alcance de uma tropa,
    centralizado em (x, y) — normalmente o centro da célula sob o mouse.
    alpha vai de 0 (invisível) a 255 (totalmente opaco)."""
    import pygame
    screen = janela.screen

    diametro = int(alcance * 2)
    superficie = pygame.Surface((diametro, diametro), pygame.SRCALPHA)

    # preenchimento
    pygame.draw.circle(superficie, (*cor, alpha), (alcance, alcance), alcance)
    # borda mais visível, pra ficar fácil de enxergar o limite exato
    pygame.draw.circle(superficie, (*cor, 200), (alcance, alcance), alcance, 2)

    screen.blit(superficie, (x - alcance, y - alcance))