from collections import deque
from mapa import MAPA, LARGURA_MAPA, ALTURA_MAPA

def celula_livre(x, y):
    if not (
        0 <= x < LARGURA_MAPA and 0 <= y < ALTURA_MAPA
    ):
        return False

    return MAPA[y][x] == "0"


def calcular_caminho(inicio, destino):
    if not celula_livre(*inicio):
        return []

    if not celula_livre(*destino):
        return []

    fila = deque([inicio])

    anteriores = {inicio: None}

    direcoes = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    while fila:
        atual = fila.popleft()

        if atual == destino:
            break

        x, y = atual

        for dx, dy in direcoes:
            proxima = (x + dx, y + dy)

            if not celula_livre(*proxima):
                continue
    
            if proxima in anteriores:
                continue
    
            anteriores[proxima] = atual

            fila. append(proxima)

    if destino not in anteriores:
        return []

    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse()

    return caminho