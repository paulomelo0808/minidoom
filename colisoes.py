import math

from config import RAIO_JOGADOR
from mapa import MAPA, LARGURA_MAPA, ALTURA_MAPA

def posicao_livre(x, y):

    #Definir area do jogador
    coluna_minima = math.floor(x - RAIO_JOGADOR)
    coluna_maxima = math.floor(x + RAIO_JOGADOR)

    linha_minima = math.floor(y - RAIO_JOGADOR)
    linha_maxima = math.floor(y + RAIO_JOGADOR)

    for linha in range(linha_minima, linha_maxima + 1):
        for coluna in range(coluna_minima, coluna_maxima + 1):

            #Impedir jogar fora do mapa
            if not (
                0 <= coluna < LARGURA_MAPA
                and 0 <= linha < ALTURA_MAPA
            ):
                return False

            #Ignora células que não sao paredes
            if MAPA[linha][coluna] != '1':
                continue

            #Encontra o ponto de parede mais proxima ao jogador
            ponto_x = max(coluna, min(x, coluna +1))
            ponto_y = max(linha, min(y, linha + 1))

            #Distancia entre o centro do jogador e o ponto da parede
            distancia_x = x - ponto_x
            distancia_y = y - ponto_y

            distancia_quadrada = (
                distancia_x ** 2 + distancia_y ** 2
            )

            #Verifica se o circulo invade a parede
            if distancia_quadrada < RAIO_JOGADOR ** 2:
                return False

    return True