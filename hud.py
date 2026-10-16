
import pygame

from config import (
    LARGURA,
    ALTURA,
    VIDA_MAXIMA_JOGADOR,
)


def desenhar_hud(tela, vida, fonte):

    # Fundo do painel
    pygame.draw.rect(
        tela,
        (25, 25, 32),
        (18, 18, 222, 65),
        border_radius=6,
    )

    # Texto da vida
    texto = fonte.render(
        f"VIDA: {vida}/{VIDA_MAXIMA_JOGADOR}",
        True,
        (240, 240, 240),
    )

    tela.blit(texto, (30, 25))

    # Fundo da barra
    pygame.draw.rect(
        tela,
        (80, 35, 40),
        (30, 60, 195, 12),
    )

    # Largura proporcional à vida
    largura_vida = int(
        195 * vida / VIDA_MAXIMA_JOGADOR
    )

    # Barra de vida atual
    pygame.draw.rect(
        tela,
        (210, 65, 75),
        (30, 60, largura_vida, 12),
    )


def desenhar_derrota(tela, fonte_grande, fonte_pequena):

    # Camada escura semitransparente
    camada = pygame.Surface(
        (LARGURA, ALTURA),
        pygame.SRCALPHA,
    )

    camada.fill((0, 0, 0, 185))
    tela.blit(camada, (0, 0))

    # Título de derrota
    titulo = fonte_grande.render(
        "GAME OVER",
        True,
        (220, 65, 65),
    )

    # Instrução de reinício
    instrucao = fonte_pequena.render(
        "Pressione R para reiniciar",
        True,
        (240, 240, 240),
    )

    # Centraliza os textos
    titulo_rect = titulo.get_rect(
        center=(LARGURA // 2, ALTURA // 2 - 35)
    )

    instrucao_rect = instrucao.get_rect(
        center=(LARGURA // 2, ALTURA // 2 + 30)
    )

    tela.blit(titulo, titulo_rect)
    tela.blit(instrucao, instrucao_rect)



def desenhar_vitoria(tela, fonte_grande, fonte_pequena):
    """Exibe a tela de vitória sobre o cenário."""

    # Cria uma camada semitransparente
    camada = pygame.Surface(
        (LARGURA, ALTURA),
        pygame.SRCALPHA,
    )

    camada.fill((0, 0, 0, 190))
    tela.blit(camada, (0, 0))

    # Mensagem principal
    titulo = fonte_grande.render(
        "VOCE VENCEU!",
        True,
        (245, 205, 80),
    )

    # Mensagem secundária
    mensagem = fonte_pequena.render(
        "Voce encontrou a chave e escapou!",
        True,
        (235, 235, 235),
    )

    # Instrução de reinício
    reiniciar = fonte_pequena.render(
        "Pressione R para jogar novamente",
        True,
        (190, 190, 190),
    )

    # Centraliza os textos
    titulo_rect = titulo.get_rect(
        center=(LARGURA // 2, ALTURA // 2 - 65)
    )

    mensagem_rect = mensagem.get_rect(
        center=(LARGURA // 2, ALTURA // 2)
    )

    reiniciar_rect = reiniciar.get_rect(
        center=(LARGURA // 2, ALTURA // 2 + 55)
    )

    # Desenha os textos
    tela.blit(titulo, titulo_rect)
    tela.blit(mensagem, mensagem_rect)
    tela.blit(reiniciar, reiniciar_rect)
