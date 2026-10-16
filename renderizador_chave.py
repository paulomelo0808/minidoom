
import math
import pygame

from config import LARGURA, ALTURA, CAMPO_VISAO
from objetivos import POSICAO_CHAVE
from renderizador import (
    DISTANCIA_PROJECAO,
    LARGURA_COLUNA,
    NUM_COLUNAS,
)

ALTURA_CHAVE = 0.45
ALTURA_REFERENCIA = 0.9


def criar_sprite_chave():
    """Cria uma chave dourada em pixel art."""

    sprite = pygame.Surface(
        (24, 40),
        pygame.SRCALPHA,
    )

    dourado = (235, 185, 55)
    brilho = (255, 225, 110)
    sombra = (150, 100, 30)

    # Cabeça circular da chave
    pygame.draw.circle(sprite, sombra, (12, 10), 9)
    pygame.draw.circle(sprite, dourado, (12, 9), 8)

    # Abertura transparente
    pygame.draw.circle(
        sprite,
        (0, 0, 0, 0),
        (12, 9),
        4,
    )

    # Haste
    pygame.draw.rect(
        sprite,
        dourado,
        (10, 17, 5, 21),
    )

    # Reflexo na haste
    pygame.draw.rect(
        sprite,
        brilho,
        (10, 18, 2, 18),
    )

    # Dentes da chave
    pygame.draw.rect(
        sprite,
        dourado,
        (14, 28, 7, 5),
    )

    pygame.draw.rect(
        sprite,
        dourado,
        (14, 35, 6, 4),
    )

    return sprite


def desenhar_chave(
    tela,
    posicao_jogador,
    angulo_jogador,
    sprite,
    profundidades,
):
    """Projeta a chave no cenário FPS."""

    jogador_x, jogador_y = posicao_jogador
    chave_x, chave_y = POSICAO_CHAVE

    # Vetor do jogador até a chave
    dx = chave_x - jogador_x
    dy = chave_y - jogador_y

    # Ângulo relativo à câmera
    angulo_relativo = (
        math.atan2(dy, dx) - angulo_jogador
    )

    angulo_relativo = (
        (angulo_relativo + math.pi)
        % (2 * math.pi)
        - math.pi
    )

    # Descarta objetos fora do campo de visão
    if abs(angulo_relativo) > CAMPO_VISAO / 2 + 0.2:
        return

    # Profundidade perpendicular à câmera
    profundidade = (
        dx * math.cos(angulo_jogador)
        + dy * math.sin(angulo_jogador)
    )

    if profundidade <= 0.1:
        return

    # Posição horizontal na tela
    centro_x = int(
        LARGURA / 2
        + math.tan(angulo_relativo)
        * DISTANCIA_PROJECAO
    )

    # Tamanho da chave conforme a distância
    altura_sprite = max(
        1,
        min(
            ALTURA * 2,
            int(
                ALTURA_CHAVE
                * DISTANCIA_PROJECAO
                / profundidade
            ),
        ),
    )

    largura_sprite = max(
        1,
        int(
            altura_sprite
            * sprite.get_width()
            / sprite.get_height()
        ),
    )

    x_inicio = centro_x - largura_sprite // 2
    x_fim = x_inicio + largura_sprite

    if x_fim <= 0 or x_inicio >= LARGURA:
        return

    # Alinha a base da chave ao nível do chão
    altura_referencia = int(
        ALTURA_REFERENCIA
        * DISTANCIA_PROJECAO
        / profundidade
    )

    base_y = ALTURA // 2 + altura_referencia // 2
    y_inicio = base_y - altura_sprite

    # Redimensiona a imagem
    sprite_escalado = pygame.transform.scale(
        sprite,
        (largura_sprite, altura_sprite),
    )

    primeira_coluna = max(
        0,
        x_inicio // LARGURA_COLUNA,
    )

    ultima_coluna = min(
        NUM_COLUNAS - 1,
        (x_fim - 1) // LARGURA_COLUNA,
    )

    # Desenha somente onde não houver parede
    for coluna in range(
        primeira_coluna,
        ultima_coluna + 1,
    ):

        if profundidade >= profundidades[coluna]:
            continue

        inicio_faixa = max(
            0,
            x_inicio,
            coluna * LARGURA_COLUNA,
        )

        fim_faixa = min(
            LARGURA,
            x_fim,
            (coluna + 1) * LARGURA_COLUNA,
        )

        largura_faixa = fim_faixa - inicio_faixa

        if largura_faixa <= 0:
            continue

        area = pygame.Rect(
            inicio_faixa - x_inicio,
            0,
            largura_faixa,
            altura_sprite,
        )

        tela.blit(
            sprite_escalado,
            (inicio_faixa, y_inicio),
            area,
        )
