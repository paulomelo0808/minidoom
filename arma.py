import pygame

from config import (
    LARGURA,
    ALTURA,
    ESCALA_ARMA,
    COR_MIRA,
)


def criar_sprite_arma():
    
    # Inicializa a superfície base com suporte a transparência (canal alfa)
    sprite = pygame.Surface(
        (128, 100),
        pygame.SRCALPHA,
    )

    # Base e corpo metálico da pistola
    pygame.draw.polygon(sprite, (20, 24, 31), [(45, 55), (83, 55), (94, 100), (34, 100)])
    pygame.draw.polygon(sprite, (79, 88, 101), [(50, 59), (78, 59), (88, 97), (40, 97)])

    # Detalhes do cano, abertura e reflexo de luz
    pygame.draw.rect(sprite, (32, 39, 49), (55, 43, 18, 25))
    pygame.draw.rect(sprite, (12, 16, 22), (58, 45, 12, 9))
    pygame.draw.rect(sprite, (154, 164, 175), (59, 61, 9, 18))

    # Empunhadura
    pygame.draw.polygon(sprite, (35, 42, 51), [(52, 79), (76, 79), (80, 100), (48, 100)])

    # Representação das mãos segurando a arma (esquerda e direita)
    pygame.draw.polygon(sprite, (145, 98, 73), [(14, 100), (32, 79), (51, 77), (51, 100)])
    pygame.draw.polygon(sprite, (145, 98, 73), [(114, 100), (96, 79), (77, 77), (77, 100)])

    # Aplica o multiplicador de escala mantendo a proporção
    largura = 128 * ESCALA_ARMA
    altura = 100 * ESCALA_ARMA

    return pygame.transform.scale(
        sprite,
        (largura, altura),
    )


def desenhar_arma(tela, sprite, deslocamento_y = 0):

    # Fixa o centro do sprite no centro inferior da tela
    x = (LARGURA - sprite.get_width()) // 2

    y = (ALTURA - sprite.get_height() - deslocamento_y)

    tela.blit(sprite, (x, y))


def desenhar_mira(tela):

    centro_x = LARGURA // 2
    centro_y = ALTURA // 2

    distancia = 6
    comprimento = 10

    # Desenha os quatro traços perpendiculares que compõem o retículo da mira
    pygame.draw.line(tela, COR_MIRA, (centro_x - distancia - comprimento, centro_y), (centro_x - distancia, centro_y), 2)
    pygame.draw.line(tela, COR_MIRA, (centro_x + distancia, centro_y), (centro_x + distancia + comprimento, centro_y), 2)
    pygame.draw.line(tela, COR_MIRA, (centro_x, centro_y - distancia - comprimento), (centro_x, centro_y - distancia), 2)
    pygame.draw.line(tela, COR_MIRA, (centro_x, centro_y + distancia), (centro_x, centro_y + distancia + comprimento), 2)

def desenhar_flash(tela, sprite, deslocamento_y = 0):

    centro_x = LARGURA // 2

    boca_y = (ALTURA - sprite.get_height() - deslocamento_y + 45 * ESCALA_ARMA)

    #Parte externa do clarao
    pygame.draw.polygon( tela, (255, 165, 35), [
                                                    (centro_x, boca_y - 5),
                                                    (centro_x - 23, boca_y - 5),
                                                    (centro_x, boca_y - 15),
                                                    (centro_x + 23, boca_y - 5),
                                                ],
    )

    pygame.draw.polygon( tela, (255, 245, 170), [
                                                    (centro_x, boca_y - 35),
                                                    (centro_x - 9, boca_y - 9),
                                                    (centro_x + 9, boca_y - 9),
                                                ],
    )
    