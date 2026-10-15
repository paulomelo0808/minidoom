import math
import pygame

from config import LARGURA, ALTURA, CAMPO_VISAO
from raycasting import lancar_raio

#Largura e quantidade de colunas
LARGURA_COLUNA = 4
NUM_COLUNAS = math.ceil(LARGURA / LARGURA_COLUNA)

#Distancia ate o plano de projecao
DISTANCIA_PROJECAO = (
    (LARGURA / 2) / math.tan(CAMPO_VISAO / 2)
)

COR_TETO = (35, 35, 47)
COR_CHAO = (75, 65, 60)

def desenhar_fps(tela, posicao_jogador, angulo_jogador):

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


        _, _, distancia = resultado

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

        #Desenha a coluna da parede
        pygame.draw.rect(
            tela, 
            cor_parede,
            (
                coluna * LARGURA_COLUNA,
                y_inicio,
                LARGURA_COLUNA,
                altura_parede,
            ),
        )

    return profundidades