import math

from config import DANO_PISTOLA, RAIO_ACERTO_INIMIGO
from raycasting import lancar_raio

def criar_inimigos():
    inimigos = [
        {
            "posicao": (5.5, 1.5), 
            "vida": 3,
            "ativo": True,
        }
    ]

    return inimigos


def processar_disparo(posicao_jogador, angulo_jogador, inimigos):

    # Direção central do disparo
    direcao_x = math.cos(angulo_jogador)
    direcao_y = math.sin(angulo_jogador)

    # Descobre a distância até a primeira parede
    resultado_parede = lancar_raio(
        posicao_jogador,
        angulo_jogador,
    )

    if resultado_parede is None:
        distancia_parede = math.inf
    else:
        distancia_parede = resultado_parede[2]

    # Inicialmente, nenhum inimigo foi atingido
    alvo = None
    menor_distancia = distancia_parede

    jogador_x, jogador_y = posicao_jogador

    for inimigo in inimigos:

        if not inimigo["ativo"]:
            continue

        inimigo_x, inimigo_y = inimigo["posicao"]

        # Vetor do jogador até o inimigo
        dx = inimigo_x - jogador_x
        dy = inimigo_y - jogador_y

        # Projeção do inimigo na direção do tiro
        projecao = (
            dx * direcao_x
            + dy * direcao_y
        )

        # Ignora inimigos atrás do jogador
        if projecao <= 0:
            continue

        # Distância perpendicular ao raio, ao quadrado
        distancia_lateral_quadrada = max(
            0.0,
            dx * dx + dy * dy - projecao * projecao,
        )

        raio_quadrado = RAIO_ACERTO_INIMIGO ** 2

        # O raio não intersecta a área do inimigo
        if distancia_lateral_quadrada > raio_quadrado:
            continue

        # Distância até o primeiro ponto de contato
        distancia_contato = max(
            0.0,
            projecao - math.sqrt(
                raio_quadrado - distancia_lateral_quadrada
            ),
        )

        # Seleciona o inimigo mais próximo,
        # desde que esteja antes da parede
        if distancia_contato < menor_distancia:
            menor_distancia = distancia_contato
            alvo = inimigo

    # Nenhum inimigo atingido
    if alvo is None:
        return None

    # Aplica o dano
    alvo["vida"] -= DANO_PISTOLA

    # Elimina o inimigo quando a vida chega a zero
    if alvo["vida"] <= 0:
        alvo["vida"] = 0
        alvo["ativo"] = False

    return alvo
