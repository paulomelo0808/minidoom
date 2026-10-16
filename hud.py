
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
