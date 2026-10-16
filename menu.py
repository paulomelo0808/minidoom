
import pygame

from config import LARGURA, ALTURA


OPCOES_MENU = (
    "INICIAR JOGO",
    "CONTROLES",
    "SAIR",
)

OPCOES_PAUSA = (
    "CONTINUAR",
    "REINICIAR PARTIDA",
    "VOLTAR AO MENU",
)

COR_FUNDO_MENU = (23, 24, 33)
COR_DESTAQUE = (160, 55, 50)
COR_TEXTO = (235, 230, 220)


def desenhar_menu(
    tela,
    opcao_selecionada,
    fonte_grande,
    fonte_pequena,
):
    """Desenha o menu principal do Mini DOOM."""

    tela.fill(COR_FUNDO_MENU)

    # Título
    titulo = fonte_grande.render(
        "MINI DOOM",
        True,
        (225, 75, 65),
    )

    titulo_rect = titulo.get_rect(
        center=(LARGURA // 2, 90)
    )

    tela.blit(titulo, titulo_rect)

    # Subtítulo
    subtitulo = fonte_pequena.render(
        "RETRO RAYCASTING FPS",
        True,
        (155, 155, 165),
    )

    subtitulo_rect = subtitulo.get_rect(
        center=(LARGURA // 2, 140)
    )

    tela.blit(subtitulo, subtitulo_rect)

    # Opções do menu
    for indice, opcao in enumerate(OPCOES_MENU):

        selecionada = indice == opcao_selecionada

        retangulo = pygame.Rect(
            0,
            0,
            310,
            58,
        )

        retangulo.center = (
            LARGURA // 2,
            230 + indice * 75,
        )

        if selecionada:
            cor_fundo = COR_DESTAQUE
            cor_borda = (220, 100, 85)
        else:
            cor_fundo = (38, 40, 53)
            cor_borda = (90, 90, 105)

        pygame.draw.rect(
            tela,
            cor_fundo,
            retangulo,
            border_radius=5,
        )

        pygame.draw.rect(
            tela,
            cor_borda,
            retangulo,
            2,
            border_radius=5,
        )

        texto = fonte_pequena.render(
            opcao,
            True,
            COR_TEXTO,
        )

        tela.blit(
            texto,
            texto.get_rect(center=retangulo.center),
        )

    # Instrução
    instrucao = fonte_pequena.render(
        "SETAS: SELECIONAR    ENTER: CONFIRMAR",
        True,
        (145, 145, 155),
    )

    tela.blit(
        instrucao,
        instrucao.get_rect(
            center=(LARGURA // 2, ALTURA - 45)
        ),
    )


def desenhar_controles(
    tela,
    fonte_grande,
    fonte_pequena,
):
    """Exibe a tela de instruções do jogo."""

    tela.fill(COR_FUNDO_MENU)

    titulo = fonte_grande.render(
        "CONTROLES",
        True,
        (225, 75, 65),
    )

    tela.blit(
        titulo,
        titulo.get_rect(
            center=(LARGURA // 2, 75)
        ),
    )

    instrucoes = (
        "W A S D  -  Movimentar",
        "MOUSE  -  Olhar ao redor",
        "CLIQUE ESQUERDO  -  Atirar",
        "TAB  -  Mostrar mapa",
        "ESC  -  Pausar ou continuar",
        "OBJETIVO  -  Encontrar chave e saida",
    )

    for indice, instrucao in enumerate(instrucoes):

        texto = fonte_pequena.render(
            instrucao,
            True,
            COR_TEXTO,
        )

        tela.blit(
            texto,
            texto.get_rect(
                center=(
                    LARGURA // 2,
                    155 + indice * 49,
                )
            ),
        )

    voltar = fonte_pequena.render(
        "ENTER OU ESC - VOLTAR",
        True,
        (225, 175, 90),
    )

    tela.blit(
        voltar,
        voltar.get_rect(
            center=(LARGURA // 2, ALTURA - 45)
        ),
    )




def desenhar_pausa(
    tela,
    fonte_grande,
    fonte_pequena,
    opcao_selecionada,
):
    """Desenha o menu de pausa sobre a partida."""

    # Escurece o cenário
    camada = pygame.Surface(
        (LARGURA, ALTURA),
        pygame.SRCALPHA,
    )

    camada.fill((0, 0, 0, 190))
    tela.blit(camada, (0, 0))

    # Título
    titulo = fonte_grande.render(
        "JOGO PAUSADO",
        True,
        (245, 205, 100),
    )

    tela.blit(
        titulo,
        titulo.get_rect(
            center=(LARGURA // 2, ALTURA // 2 - 145)
        ),
    )

    # Desenha as três opções
    for indice, opcao in enumerate(OPCOES_PAUSA):

        selecionada = indice == opcao_selecionada

        retangulo = pygame.Rect(
            0,
            0,
            310,
            50,
        )

        retangulo.center = (
            LARGURA // 2,
            ALTURA // 2 - 35 + indice * 65,
        )

        if selecionada:
            cor_fundo = (140, 70, 55)
            cor_borda = (235, 150, 95)
        else:
            cor_fundo = (38, 40, 53)
            cor_borda = (100, 100, 110)

        pygame.draw.rect(
            tela,
            cor_fundo,
            retangulo,
            border_radius=5,
        )

        pygame.draw.rect(
            tela,
            cor_borda,
            retangulo,
            2,
            border_radius=5,
        )

        texto = fonte_pequena.render(
            opcao,
            True,
            (245, 245, 245),
        )

        tela.blit(
            texto,
            texto.get_rect(center=retangulo.center),
        )

    # Instrução inferior
    instrucao = fonte_pequena.render(
        "SETAS: SELECIONAR   ENTER: CONFIRMAR",
        True,
        (190, 190, 195),
    )

    tela.blit(
        instrucao,
        instrucao.get_rect(
            center=(LARGURA // 2, ALTURA - 40)
        ),
    )
