import math

from config import DANO_PISTOLA, RAIO_ACERTO_INIMIGO
from raycasting import lancar_raio
from config import VELOCIDADE_INIMIGO, DISTANCIA_PARADA_INIMIGO, DANO_ATAQUE_INIMIGO, ALCANCE_ATAQUE_INIMIGO, INTERVALO_ATAQUE_INIMIGO
from navegacao import calcular_caminho
from colisoes import posicao_livre


def criar_inimigos():
    inimigos = [
        {
            "posicao": (5.5, 1.5), 
            "vida": 3,
            "ativo": True,
            "proxima_celula": None,
            "recarga_ataque": 0.0,
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


def atualizar_inimigos(inimigos, posicao_jogador, delta_tempo):
    jogador_x, jogador_y = posicao_jogador

    for inimigo in inimigos:
        if not inimigo["ativo"]:
            continue

        inimigo_x, inimigo_y = inimigo["posicao"]

        distancia_jogador = math.hypot(
            jogador_x - inimigo_x,
            jogador_y - inimigo_y,
        )

        if distancia_jogador <= DISTANCIA_PARADA_INIMIGO:
            inimigo["proxima_celula"] = None
            continue

        celula_inimigo =(
            math.floor(inimigo_x),
            math.floor(inimigo_y),
        )

        celula_jogador = (
            math.floor(jogador_x),
            math.floor(jogador_y),
        )

        if celula_inimigo == celula_jogador:
            inimigo["proxima_celula"] = None
            alvo_x = jogador_x
            alvo_y = jogador_y

        else:
            if inimigo["proxima_celula"] is None:
                caminho = calcular_caminho(
                    celula_inimigo,
                    celula_jogador,
                )

                if len(caminho) < 2:
                    continue

                inimigo["proxima_celula"] = caminho[1]


            proxima_x, proxima_y = inimigo["proxima_celula"]

            alvo_x = proxima_x + 0.5
            alvo_y = proxima_y + 0.5

        dx = alvo_x - inimigo_x
        dy = alvo_y - inimigo_y

        distancia_alvo = math.hypot(dx, dy)

        if distancia_alvo < 0.0001:
            inimigo["proxima_celula"] = None
            continue

        passo = min(
            VELOCIDADE_INIMIGO * delta_tempo,
            distancia_alvo,
            max(
                0.0, distancia_jogador - DISTANCIA_PARADA_INIMIGO,
            )
        )

        novo_x = inimigo_x + (dx / distancia_alvo) * passo
        novo_y = inimigo_y + (dy / distancia_alvo) * passo

        if posicao_livre(novo_x, novo_y):
            inimigo["posicao"] = (novo_x, novo_y)

            if math.hypot(
                alvo_x - novo_x,
                alvo_y - novo_y,
            ) < 0.0001:

                inimigo["proxima_celula"] = None

            else:
                inimigo["proxima_celula"] = None


def atualizar_ataques_inimigos(
    inimigos,
    posicao_jogador,
    delta_tempo,
):
    dano_total = 0

    jogador_x, jogador_y = posicao_jogador

    for inimigo in inimigos:

        # Inimigos eliminados não atacam
        if not inimigo["ativo"]:
            continue

        # Atualiza o intervalo entre ataques
        inimigo["recarga_ataque"] = max(
            0.0,
            inimigo["recarga_ataque"] - delta_tempo,
        )

        # Ainda não pode atacar novamente
        if inimigo["recarga_ataque"] > 0:
            continue

        inimigo_x, inimigo_y = inimigo["posicao"]

        # Vetor do inimigo até o jogador
        dx = jogador_x - inimigo_x
        dy = jogador_y - inimigo_y

        distancia = math.hypot(dx, dy)

        # Jogador fora do alcance
        if distancia > ALCANCE_ATAQUE_INIMIGO:
            continue

        # Direção do inimigo para o jogador
        angulo_ataque = math.atan2(dy, dx)

        # Verifica se há parede entre eles
        resultado_parede = lancar_raio(
            inimigo["posicao"],
            angulo_ataque,
        )

        if resultado_parede is not None:
            distancia_parede = resultado_parede[2]

            if distancia_parede < distancia - 0.0001:
                continue

        # Ataque autorizado
        dano_total += DANO_ATAQUE_INIMIGO

        # Reinicia o intervalo entre ataques
        inimigo["recarga_ataque"] = (
            INTERVALO_ATAQUE_INIMIGO
        )

    return dano_total
