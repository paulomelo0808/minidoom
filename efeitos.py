from config import DURACAO_EFEITO_DANO


def desenhar_efeito_dano(tela, camada, tempo_restante):
    """Desenha um flash vermelho que desaparece gradualmente."""

    if tempo_restante <= 0:
        return

    # Calcula a intensidade entre 0 e 1
    intensidade = min(
        1.0,
        tempo_restante / DURACAO_EFEITO_DANO,
    )

    # Opacidade proporcional ao tempo restante
    opacidade = int(110 * intensidade)

    # Preenche a camada com vermelho semitransparente
    camada.fill((200, 25, 35, opacidade))

    # Desenha a camada sobre o cenário
    tela.blit(camada, (0, 0))