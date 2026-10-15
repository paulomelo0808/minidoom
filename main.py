import math
import pygame

from config import (
    LARGURA,
    ALTURA,
    FPS,
    TITULO,
    COR_FUNDO,
    TAMANHO_CELULA,
    COR_PAREDE,
    COR_CHAO,
    COR_GRADE,
    COR_JOGADOR,
    ANGULO_INICIAL,
    CAMPO_VISAO,
    VELOCIDADE_ROTACAO,
    SENSIBILIDADE_MOUSE,
    INTERVALO_ENTRE_TIROS,
    DURACAO_EFEITO_TIRO,
    RECUO_MAXIMO,
)

from mapa import MAPA, POSICAO_INICIAL
from raycasting import lancar_raio
from renderizador import desenhar_fps
from jogador import atualizar_posicao
from arma import (criar_sprite_arma, desenhar_arma, desenhar_mira, desenhar_flash,)

def main():

    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)

    sprite_arma = criar_sprite_arma()

    relogio = pygame.time.Clock()
    executando = True
    mostrar_mapa = False

    #Configurações do mouse
    mouse_capturado = True
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False) #esconde o cursor
    pygame.mouse.get_rel()

    angulo_jogador = ANGULO_INICIAL
    posicao_jogador = POSICAO_INICIAL

    tempo_ate_proximo_tiro = 0.0
    tempo_efeito_tiro = 0.0

    while executando:

        delta_tempo = min(relogio.tick(FPS) / 1000.0, 0.05)

        tempo_ate_proximo_tiro = max(0.0, tempo_ate_proximo_tiro - delta_tempo,)
        tempo_efeito_tiro = max(0.0, tempo_efeito_tiro - delta_tempo,)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_TAB:
                    mostrar_mapa = not mostrar_mapa

                # Libera ou captura o cursor
                elif evento.key == pygame.K_ESCAPE:
                    mouse_capturado = not mouse_capturado
                    pygame.event.set_grab(mouse_capturado)
                    pygame.mouse.set_visible(not mouse_capturado)
                    # Descarta movimentos acumulados
                    pygame.mouse.get_rel()

            #Disparo do tiro
            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if (
                    evento.button == 1
                    and mouse_capturado
                    and not mostrar_mapa
                    and tempo_ate_proximo_tiro <= 0
                ):

                    tempo_ate_proximo_tiro = INTERVALO_ENTRE_TIROS

                    tempo_efeito_tiro = DURACAO_EFEITO_TIRO


        # Lê o deslocamento horizontal do mouse
        deslocamento_x, _ = pygame.mouse.get_rel()

        if mouse_capturado:
            # Atualiza a direção da câmera
            angulo_jogador += (deslocamento_x * SENSIBILIDADE_MOUSE)
            # Mantém o ângulo entre 0 e 2*pi
            angulo_jogador %= 2 * math.pi

            # Leitura contínua do teclado
            teclas = pygame.key.get_pressed()

            # Atualiza a posição do jogador
            posicao_jogador = atualizar_posicao(
                posicao_jogador,
                angulo_jogador,
                teclas,
                delta_tempo,
            )


        # Renderização
        if mostrar_mapa:
            tela.fill(COR_FUNDO)
            desenhar_mapa(
                tela,
                posicao_jogador,
                angulo_jogador,
            )
        else:
            desenhar_fps(
                tela,
                posicao_jogador,
                angulo_jogador,
            )

            recuo = 0

            if tempo_efeito_tiro > 0:
                recuo = int(RECUO_MAXIMO * tempo_efeito_tiro / DURACAO_EFEITO_TIRO)

            desenhar_arma(tela, sprite_arma, recuo,)

            if tempo_efeito_tiro > 0:
                desenhar_flash(tela, sprite_arma, recuo,)
            desenhar_mira(tela)

        pygame.display.flip()

    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)

    pygame.quit()


def desenhar_mapa(tela, posicao_jogador, angulo_jogador):

    # Calcula as dimensões do mapa em pixels
    largura_mapa = len(MAPA[0]) * TAMANHO_CELULA
    altura_mapa = len(MAPA) * TAMANHO_CELULA

    # Centraliza o mapa na janela
    origem_x = (LARGURA - largura_mapa) // 2
    origem_y = (ALTURA - altura_mapa) // 2

    # Percorre as linhas e colunas do mapa
    for y, linha in enumerate(MAPA):
        for x, celula in enumerate(linha):

            # Converte coordenadas do mapa em pixels
            pixel_x = origem_x + x * TAMANHO_CELULA
            pixel_y = origem_y + y * TAMANHO_CELULA

            retangulo = pygame.Rect(
                pixel_x,
                pixel_y,
                TAMANHO_CELULA,
                TAMANHO_CELULA,
            )

            # Desenha paredes e corredores
            if celula == "1":
                cor = COR_PAREDE
            else:
                cor = COR_CHAO

            pygame.draw.rect(tela, cor, retangulo)

            # Desenha os limites das células
            pygame.draw.rect(
                tela,
                COR_GRADE,
                retangulo,
                1,
            )

    # Posição inicial do jogador
    jogador_x, jogador_y = posicao_jogador

    pixel_jogador_x = origem_x + jogador_x * TAMANHO_CELULA
    pixel_jogador_y = origem_y + jogador_y * TAMANHO_CELULA


    # Representação visual do campo de visão
    for deslocamento in (
        -CAMPO_VISAO / 2,
        0,
        CAMPO_VISAO / 2,
    ):
        angulo_raio = angulo_jogador + deslocamento

        #calcula a primeira intersecao com uma parede
        resultado = lancar_raio(
            posicao_jogador,
            angulo_raio,
        )

        if resultado is None:
            continue

        x_impacto, y_impacto, distancia = resultado

        destino_x = origem_x + x_impacto * TAMANHO_CELULA
        destino_y = origem_y + y_impacto * TAMANHO_CELULA

        #Desenha o raio ate a parede
        pygame.draw.line(
            tela,
            (230, 190, 80),
            (pixel_jogador_x, pixel_jogador_y),
            (destino_x, destino_y),
            2,
        )

        #Marca o ponto de impacto
        pygame.draw.circle(
            tela,
            (255, 100, 80),
            (int(destino_x), int(destino_y)),
            4,
        )

if __name__ == "__main__":
    main()
