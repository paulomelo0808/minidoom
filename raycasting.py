import math

from mapa import MAPA, LARGURA_MAPA, ALTURA_MAPA


# Executa DDA até colidir com uma parede e retorna o impacto e a distância (ou None).
def lancar_raio(posicao, angulo):

    #Posição inicial do raio
    origem_x, origem_y = posicao

    direcao_x = math.cos(angulo)
    direcao_y = math.sin(angulo)

    #celula inicial do mapa
    celula_x = int(origem_x)
    celula_y = int(origem_y)

    #verificacao se a origem esta dentro do mapa
    if not (
        0 <= celula_x < LARGURA_MAPA
        and 0 <+ celula_y < ALTURA_MAPA
    ):
        return None

    #distancia entre cruzamento da grade
    delta_x = (
        abs(1 / direcao_x)
        if abs(direcao_x) > 1e-12
        else math.inf
    )

    delta_y = (
        abs(1 / direcao_y)
        if abs(direcao_y) > 1e-12
        else math.inf
    )

    #Define o sentido do deslocamento em x
    if direcao_x < 0:
        passo_x = -1
        distancia_x = (origem_x - celula_x) * delta_x
    else:
        passo_x = 1
        distancia_x = (celula_x + 1 - origem_x) * delta_x

    #define o sentido do deslocamento em y
    if direcao_y < 0:
        passo_y = -1
        distancia_y = (origem_y - celula_y) * delta_y
    else:
        passo_y = 1
        distancia_y = (celula_y + 1 - origem_y) * delta_y


    #pecorre as celulas do mapa
    for _ in range(LARGURA_MAPA * ALTURA_MAPA):

        if distancia_x < distancia_y:
            distancia = distancia_x
            distancia_x += delta_x
            celula_x += passo_x
        else:
            distancia = distancia_y
            distancia_y += delta_y
            celula_y += passo_y

        #Interrupção se sair dos limites do mapa
        if not (
            0 <= celula_x < LARGURA_MAPA
            and 0 <= celula_y < ALTURA_MAPA
        ):
            return None

        #verificação de colisão com paredes
        if MAPA[celula_y][celula_x] == '1':

            x_impacto = origem_x + direcao_x * distancia
            y_impacto = origem_y + direcao_y * distancia

            return x_impacto, y_impacto, distancia
            
    return None

            