import math
import pygame

from config import LARGURA, ALTURA, CAMPO_VISAO
from raycasting import lancar_raio
from objetivos import POSICAO_SAIDA

#Largura e quantidade de colunas
LARGURA_COLUNA = 4
NUM_COLUNAS = math.ceil(LARGURA / LARGURA_COLUNA)

#Distancia ate o plano de projecao
DISTANCIA_PROJECAO = (
    (LARGURA / 2) / math.tan(CAMPO_VISAO / 2)
)

COR_TETO = (35, 35, 47)
COR_CHAO = (75, 65, 60)
# A saída fica diante da parede leste da sua célula
X_PAREDE_PORTA = int(POSICAO_SAIDA[0]) + 1
Y_PAREDE_PORTA = int(POSICAO_SAIDA[1])


def criar_textura_porta():
    textura = pygame.Surface((64, 64))

    # Estrutura externa escura
    textura.fill((35, 40, 52))

    # Moldura metálica
    pygame.draw.rect(
        textura,
        (125, 145, 160),
        (5, 3, 54, 58),
    )

    # Borda interna
    pygame.draw.rect(
        textura,
        (28, 53, 75),
        (10, 7, 44, 50),
    )

    # Corpo da porta
    pygame.draw.rect(
        textura,
        (42, 89, 125),
        (14, 10, 36, 44),
    )

    # Painel superior
    pygame.draw.rect(
        textura,
        (64, 135, 175),
        (19, 15, 26, 14),
    )

    # Painel inferior
    pygame.draw.rect(
        textura,
        (39, 72, 98),
        (19, 35, 26, 13),
    )

    # Divisão central metálica
    pygame.draw.rect(
        textura,
        (145, 168, 185),
        (14, 31, 36, 3),
    )

    # Maçaneta dourada
    pygame.draw.rect(
        textura,
        (245, 205, 75),
        (44, 32, 4, 6),
    )

    # Rebites da moldura
    for x in (7, 56):
        for y in (8, 55):
            pygame.draw.rect(
                textura,
                (195, 205, 215),
                (x, y, 2, 2),
            )

    return textura



def desenhar_fps(tela, posicao_jogador, angulo_jogador, textura_porta):

    profundidades = [math.inf] * NUM_COLUNAS
    
    #Desenhar  o teto
    tela.fill(COR_TETO)

    #Desenhar o chão
    pygame.draw.rect(
        tela,
        COR_CHAO,
        (0,  ALTURA // 2, LARGURA, ALTURA // 2)
    )

    #Lancar um raio para coluna 
    for coluna in range(NUM_COLUNAS):
        camera_x = (
            2 * (coluna + 0.5) / NUM_COLUNAS - 1
        )

        desvio = math.atan(
            camera_x * math.tan(CAMPO_VISAO / 2)
        )

        angulo_raio = angulo_jogador + desvio

        #Encontrar a parede
        resultado = lancar_raio(
            posicao_jogador,
            angulo_raio,
        )

        if resultado is None:
            continue


        x_impacto, y_impacto, distancia = resultado

        distancia_perpendicular = max( 0.001, distancia * math.cos(desvio),)
        profundidades[coluna] = distancia_perpendicular

        altura_parede = int(DISTANCIA_PROJECAO / distancia_perpendicular) #Altura das paredes projetadas
        
        y_inicio = (ALTURA - altura_parede) // 2 #Centralizaçao

        #Escurece paredes distantes
        brilho = max(
            45, 
            min(205, int(220 / (1 + distancia_perpendicular * 0.12)),
            ),
        )

        cor_parede = (
            brilho,
            max(0, brilho - 10),
            max(0, brilho - 25),
        )

        atingiu_porta = (
            abs(x_impacto - X_PAREDE_PORTA) < 0.0001
            and Y_PAREDE_PORTA <= y_impacto
            < Y_PAREDE_PORTA + 1
        )

        x_tela = coluna * LARGURA_COLUNA

        if atingiu_porta:

            # Posição horizontal do impacto dentro da textura
            u = y_impacto - Y_PAREDE_PORTA

            coluna_textura = min(
                textura_porta.get_width() - 1,
                int(u * textura_porta.get_width()),
            )

            # Seleciona uma faixa vertical da textura
            faixa_textura = textura_porta.subsurface(
                (
                    coluna_textura,
                    0,
                    1,
                    textura_porta.get_height(),
                )
            )

            # Projeta essa faixa na altura da parede
            faixa_escalada = pygame.transform.scale(
                faixa_textura,
                (LARGURA_COLUNA, altura_parede),
            )

            # Desenha a faixa da porta
            tela.blit(
                faixa_escalada,
                (x_tela, y_inicio),
            )

        else:

            # Paredes comuns continuam com sua cor original
            pygame.draw.rect(
                tela,
                cor_parede,
                (
                    x_tela,
                    y_inicio,
                    LARGURA_COLUNA,
                    altura_parede,
                ),
            )


    return profundidades