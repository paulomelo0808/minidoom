import math

POSICAO_CHAVE = (9.5, 9.5)

RAIO_COLETA_CHAVE = 0.45


def verificar_coleta_chave(posicao_jogador):
    """Verifica se o jogador está próximo da chave."""

    distancia = math.dist(
        posicao_jogador,
        POSICAO_CHAVE,
    )

    return distancia <= RAIO_COLETA_CHAVE


# Posição da saída do labirinto
POSICAO_SAIDA = (10.5, 1.5)

# Distância necessária para alcançar a saída
RAIO_ATIVACAO_SAIDA = 0.55


def verificar_vitoria(posicao_jogador, tem_chave):
    """Verifica se o jogador cumpriu o objetivo da fase."""

    # A saída permanece bloqueada sem a chave
    if not tem_chave:
        return False

    # Distância do jogador até o centro da saída
    distancia = math.dist(
        posicao_jogador,
        POSICAO_SAIDA,
    )

    return distancia <= RAIO_ATIVACAO_SAIDA
