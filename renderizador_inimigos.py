
import math
import pygame

from config import LARGURA, ALTURA, CAMPO_VISAO, DURACAO_FLASH_INIMIGO
from renderizador import (
    DISTANCIA_PROJECAO,
    LARGURA_COLUNA,
    NUM_COLUNAS,
)

# Altura do inimigo em unidades do mundo
ALTURA_INIMIGO = 0.9


def criar_sprite_inimigo():

    sprite = pygame.Surface(
        (32, 48),
        pygame.SRCALPHA,
    )

    # Pernas
    pygame.draw.rect(sprite, (75, 25, 30), (7, 36, 7, 12))
    pygame.draw.rect(sprite, (75, 25, 30), (18, 36, 7, 12))

    # Corpo
    pygame.draw.rect(sprite, (125, 37, 42), (5, 23, 22, 17))

    # Braços
    pygame.draw.rect(sprite, (100, 30, 35), (1, 25, 6, 17))
    pygame.draw.rect(sprite, (100, 30, 35), (25, 25, 6, 17))

    # Chifres
    pygame.draw.polygon(
        sprite,
        (90, 25, 30),
        [(5, 15), (2, 2), (13, 11)],
    )

    pygame.draw.polygon(
        sprite,
        (90, 25, 30),
        [(27, 15), (30, 2), (19, 11)],
    )

    # Cabeça
    pygame.draw.rect(
        sprite,
        (170, 55, 55),
        (7, 11, 18, 17),
    )

    # Olhos
    pygame.draw.rect(sprite, (245, 205, 65), (10, 17, 5, 4))
    pygame.draw.rect(sprite, (245, 205, 65), (18, 17, 5, 4))

    # Boca
    pygame.draw.rect(sprite, (45, 15, 20), (13, 24, 7, 3))

    return sprite


def desenhar_inimigos(
    tela,
    inimigos,
    posicao_jogador,
    angulo_jogador,
    sprite,
    profundidades,
):

    jogador_x, jogador_y = posicao_jogador

    # Renderiza primeiro os inimigos mais distantes
    inimigos_ordenados = sorted(
        inimigos,
        key=lambda inimigo: math.dist(
            inimigo["posicao"],
            posicao_jogador,
        ),
        reverse=True,
    )

    for inimigo in inimigos_ordenados:

        if not inimigo["ativo"]:
            continue

        inimigo_x, inimigo_y = inimigo["posicao"]

        # Vetor entre jogador e inimigo
        dx = inimigo_x - jogador_x
        dy = inimigo_y - jogador_y

        # Ângulo relativo à câmera
        angulo_relativo = (
            math.atan2(dy, dx) - angulo_jogador
        )

        # Normaliza entre -pi e +pi
        angulo_relativo = (
            (angulo_relativo + math.pi)
            % (2 * math.pi)
            - math.pi
        )

        # Descarta inimigos muito fora do campo de visão
        if abs(angulo_relativo) > CAMPO_VISAO / 2 + 0.2:
            continue

        # Profundidade perpendicular à câmera
        profundidade = (
            dx * math.cos(angulo_jogador)
            + dy * math.sin(angulo_jogador)
        )

        # Descarta inimigos atrás ou muito próximos
        if profundidade <= 0.1:
            continue

        # Projeta a posição horizontal do inimigo
        centro_x = int(
            LARGURA / 2
            + math.tan(angulo_relativo) * DISTANCIA_PROJECAO
        )

        # Calcula a altura projetada
        altura_sprite = max(
            1,
            min(
                ALTURA * 2,
                int(
                    ALTURA_INIMIGO
                    * DISTANCIA_PROJECAO
                    / profundidade
                ),
            ),
        )

        # Preserva a proporção da imagem
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

        y_inicio = (ALTURA - altura_sprite) // 2

        # Ignora sprites fora da tela
        if x_fim <= 0 or x_inicio >= LARGURA:
            continue

        sprite_escalado = pygame.transform.scale(
            sprite,
            (largura_sprite, altura_sprite),
        )




        # Inimigo pisca três vezes quando recebe dano
        tempo_flash = inimigo.get("tempo_flash", 0.0)

        if tempo_flash > 0:

            # Tempo transcorrido desde o disparo
            tempo_decorrido = (
                DURACAO_FLASH_INIMIGO - tempo_flash
            )

            # Alterna entre branco e normal a cada 0.15 s
            intervalo_piscada = 0.15

            fase = int(
                tempo_decorrido / intervalo_piscada
            )

            # Fases pares: branco
            # Fases ímpares: sprite original
            if fase % 2 == 0:

                sprite_escalado.fill(
                    (200, 200, 200),
                    special_flags=pygame.BLEND_RGB_ADD,
                )


        primeira_coluna = max(
            0,
            x_inicio // LARGURA_COLUNA,
        )

        ultima_coluna = min(
            NUM_COLUNAS - 1,
            (x_fim - 1) // LARGURA_COLUNA,
        )

        for coluna in range(
            primeira_coluna,
            ultima_coluna + 1,
        ):

            # Parede mais próxima: oculta o inimigo
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

            # Recorta a faixa visível do sprite
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
