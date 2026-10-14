
import pygame

from config import (
    LARGURA,
    ALTURA,
    FPS,
    TITULO,
    COR_FUNDO,
    TAMANHO_CELULA,
    COR_PAREDE,
    COR_CHAO,
    COR_GRADE,
    COR_JOGADOR,
)

from mapa import MAPA, POSICAO_INICIAL


def desenhar_mapa(tela):

    # Calcula as dimensões do mapa em pixels
    largura_mapa = len(MAPA[0]) * TAMANHO_CELULA
    altura_mapa = len(MAPA) * TAMANHO_CELULA

    # Centraliza o mapa na janela
    origem_x = (LARGURA - largura_mapa) // 2
    origem_y = (ALTURA - altura_mapa) // 2

    # Percorre as linhas e colunas do mapa
    for y, linha in enumerate(MAPA):
        for x, celula in enumerate(linha):

            # Converte coordenadas do mapa em pixels
            pixel_x = origem_x + x * TAMANHO_CELULA
            pixel_y = origem_y + y * TAMANHO_CELULA

            retangulo = pygame.Rect(
                pixel_x,
                pixel_y,
                TAMANHO_CELULA,
                TAMANHO_CELULA,
            )

            # Desenha paredes e corredores
            if celula == "1":
                cor = COR_PAREDE
            else:
                cor = COR_CHAO

            pygame.draw.rect(tela, cor, retangulo)

            # Desenha os limites das células
            pygame.draw.rect(
                tela,
                COR_GRADE,
                retangulo,
                1,
            )

    # Posição inicial do jogador
    jogador_x, jogador_y = POSICAO_INICIAL

    pixel_jogador_x = origem_x + jogador_x * TAMANHO_CELULA
    pixel_jogador_y = origem_y + jogador_y * TAMANHO_CELULA

    # Representa o jogador por um círculo
    pygame.draw.circle(
        tela,
        COR_JOGADOR,
        (int(pixel_jogador_x), int(pixel_jogador_y)),
        8,
    )


def main():

    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)

    relogio = pygame.time.Clock()
    executando = True

    while executando:

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        # Renderização
        tela.fill(COR_FUNDO)
        desenhar_mapa(tela)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
