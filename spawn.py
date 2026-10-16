import math
import random

from config import (
    INIMIGOS_INICIAIS,
    MAX_INIMIGOS_VIVOS,
    LIMIAR_REATIVACAO_SPAWN,
    INTERVALO_SPAWN,
    DISTANCIA_MINIMA_SPAWN,
    DISTANCIA_MINIMA_ENTRE_INIMIGOS,
)

from mapa import MAPA
from navegacao import calcular_caminho
from inimigos import criar_inimigo
from objetivos import POSICAO_CHAVE, POSICAO_SAIDA


def sortear_posicao(inimigos, posicao_jogador):
    """Sorteia uma posição segura e alcançável."""

    possibilidades = []

    celula_jogador = (
        int(posicao_jogador[0]),
        int(posicao_jogador[1]),
    )

    for y, linha in enumerate(MAPA):
        for x, celula in enumerate(linha):

            # Apenas corredores
            if celula != "0":
                continue

            posicao = (x + 0.5, y + 0.5)

            if posicao in (POSICAO_CHAVE, POSICAO_SAIDA):
                continue

            # Evita aparecer perto do jogador
            if math.dist(
                posicao,
                posicao_jogador,
            ) < DISTANCIA_MINIMA_SPAWN:
                continue

            # Verifica a distância até outros inimigos
            muito_perto = False

            for inimigo in inimigos:

                if not inimigo["ativo"]:
                    continue

                if math.dist(
                    posicao,
                    inimigo["posicao"],
                ) < DISTANCIA_MINIMA_ENTRE_INIMIGOS:

                    muito_perto = True
                    break

            if muito_perto:
                continue

            # Garante que há um caminho até o jogador
            caminho = calcular_caminho(
                (x, y),
                celula_jogador,
            )

            if not caminho:
                continue

            possibilidades.append(posicao)

    if not possibilidades:
        return None

    return random.choice(possibilidades)


def criar_inimigos_aleatorios(posicao_jogador):
    """Cria os inimigos iniciais da fase."""

    inimigos = []

    for _ in range(INIMIGOS_INICIAIS):

        posicao = sortear_posicao(
            inimigos,
            posicao_jogador,
        )

        if posicao is None:
            break

        inimigos.append(criar_inimigo(posicao))

    return inimigos


def criar_estado_spawn():
    """Inicializa o controle do temporizador."""

    return {
        "tempo": 0.0,
        "suspenso": False,
    }


def atualizar_spawn(
    inimigos,
    posicao_jogador,
    delta_tempo,
    estado,
    tem_chave,
):
    """Controla os novos inimigos durante a partida."""

    # Remove inimigos eliminados da lista,
    # evitando acúmulo ao longo da partida.
    inimigos[:] = [
        inimigo
        for inimigo in inimigos
        if inimigo["ativo"]
    ]

    # A chave encerra definitivamente os spawns
    if tem_chave:
        return None

    quantidade_vivos = len(inimigos)

    # Se suspenso, só retorna quando restarem 3 ou menos
    if estado["suspenso"]:

        if quantidade_vivos > LIMIAR_REATIVACAO_SPAWN:
            return None

        estado["suspenso"] = False
        estado["tempo"] = 0.0

    # Atingiu o máximo de inimigos
    if quantidade_vivos >= MAX_INIMIGOS_VIVOS:

        estado["suspenso"] = True
        estado["tempo"] = 0.0

        return None

    # Avança o temporizador
    estado["tempo"] += delta_tempo

    if estado["tempo"] < INTERVALO_SPAWN:
        return None

    estado["tempo"] -= INTERVALO_SPAWN

    # Escolhe a posição do novo inimigo
    posicao = sortear_posicao(
        inimigos,
        posicao_jogador,
    )

    if posicao is None:
        estado["tempo"] = 0.0
        return None

    # Cria o inimigo
    inimigos.append(criar_inimigo(posicao))

    # Suspende imediatamente ao atingir o limite
    if len(inimigos) >= MAX_INIMIGOS_VIVOS:

        estado["suspenso"] = True
        estado["tempo"] = 0.0

    return posicao
