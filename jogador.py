import math
import pygame

from config import VELOCIDADE_MOVIMENTO
from colisoes import posicao_livre

def atualizar_posicao(posicao, angulo, teclas, delta_tempo):

    #Aponta para frente
    frente_x = math.cos(angulo)
    frente_y = math.sin(angulo)

    #Perpendicular à direcao do jogador
    lateral_x = -frente_y
    lateral_y = frente_x

    movimento_x = 0.0 #Movimento acumulado neste quadro
    movimento_y = 0.0

    if teclas[pygame.K_w]: #Avançar
        movimento_x += frente_x
        movimento_y += frente_y

    if teclas[pygame.K_s]: #Recuar
        movimento_x -= frente_x
        movimento_y -= frente_y

    if teclas[pygame.K_a]: #Mover para a esquerda
        movimento_x -= lateral_x
        movimento_y -= lateral_y

    if teclas[pygame.K_d]: #Mover para a direita
        movimento_x += lateral_x
        movimento_y += lateral_y

    comprimento = math.hypot(
        movimento_x,
        movimento_y,
    )

    if comprimento == 0:
        return posicao

    movimento_x /= comprimento
    movimento_y /= comprimento

    #Aplicar velocidade e tempo decorrido
    nova_x = (
        posicao[0]
        + movimento_x * VELOCIDADE_MOVIMENTO * delta_tempo
    )

    nova_y = (
        posicao[1]
        + movimento_y * VELOCIDADE_MOVIMENTO * delta_tempo
    )

    
    # Começa com a posição atual do jogador
    x_atual, y_atual = posicao

    # Tenta movimentar no eixo X
    if posicao_livre(nova_x, y_atual):
        x_atual = nova_x

    # Tenta movimentar no eixo Y
    if posicao_livre(x_atual, nova_y):
        y_atual = nova_y

    # Retorna a posição permitida
    return x_atual, y_atual
