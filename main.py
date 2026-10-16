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
    VIDA_MAXIMA_JOGADOR,
)

from mapa import MAPA, POSICAO_INICIAL
from raycasting import lancar_raio
from renderizador import desenhar_fps, criar_textura_porta
from jogador import atualizar_posicao
from arma import (criar_sprite_arma, desenhar_arma, desenhar_mira, desenhar_flash,)
from inimigos import (criar_inimigos, processar_disparo, atualizar_inimigos, atualizar_ataques_inimigos,)
from renderizador_inimigos import (criar_sprite_inimigo, desenhar_inimigos,)
from hud import (desenhar_hud, desenhar_derrota, desenhar_vitoria,)
from spawn import (criar_inimigos_aleatorios, criar_estado_spawn, atualizar_spawn,)
from objetivos import (POSICAO_CHAVE, POSICAO_SAIDA, verificar_coleta_chave, verificar_vitoria,)
from renderizador_chave import (criar_sprite_chave, desenhar_chave,)
from menu import (OPCOES_MENU, desenhar_menu, desenhar_controles, desenhar_pausa, OPCOES_PAUSA)


def main():

    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)

    sprite_arma = criar_sprite_arma()
    sprite_inimigo = criar_sprite_inimigo()
    sprite_chave = criar_sprite_chave()
    textura_porta = criar_textura_porta()

    relogio = pygame.time.Clock()
    executando = True
    mostrar_mapa = False

    estado_jogo = "MENU"
    opcao_menu = 0
    opcao_pausa = 0
    reiniciar_pendente = False

    mouse_capturado = False
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    pygame.mouse.get_rel()

    angulo_jogador = ANGULO_INICIAL
    posicao_jogador = POSICAO_INICIAL

    inimigos = criar_inimigos_aleatorios(posicao_jogador)
    estado_spawn = criar_estado_spawn()
    tem_chave = False

    tempo_ate_proximo_tiro = 0.0
    tempo_efeito_tiro = 0.0

    vida_jogador = VIDA_MAXIMA_JOGADOR
    venceu = False

    fonte_hud = pygame.font.Font(None, 32)
    fonte_grande = pygame.font.Font(None, 72)
    fonte_pequena = pygame.font.Font(None, 36)

    while executando:

        delta_tempo = min(relogio.tick(FPS) / 1000.0, 0.05)

        # Atualiza os temporizadores apenas durante a partida
        if (
            estado_jogo == "JOGANDO"
            and vida_jogador > 0
            and not venceu
        ):
        
            tempo_ate_proximo_tiro = max(
                0.0,
                tempo_ate_proximo_tiro - delta_tempo,
            )
        
            tempo_efeito_tiro = max(
                0.0,
                tempo_efeito_tiro - delta_tempo,
            )

        # Eventos
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                executando = False
                continue

            # Eventos do menu e da tela de controles
            if estado_jogo in ("MENU", "CONTROLES"):

                if evento.type == pygame.KEYDOWN:

                    if estado_jogo == "MENU":

                        # Navega para a opção anterior
                        if evento.key == pygame.K_UP:

                            opcao_menu = (
                                opcao_menu - 1
                            ) % len(OPCOES_MENU)

                        # Navega para a próxima opção
                        elif evento.key == pygame.K_DOWN:

                            opcao_menu = (
                                opcao_menu + 1
                            ) % len(OPCOES_MENU)

                        # Confirma a opção
                        elif evento.key in (
                            pygame.K_RETURN,
                            pygame.K_KP_ENTER,
                        ):

                            if opcao_menu == 0:
                                reiniciar_pendente = True

                                # Iniciar jogo
                                estado_jogo = "JOGANDO"
                                mouse_capturado = True

                                pygame.event.set_grab(True)
                                pygame.mouse.set_visible(False)
                                pygame.mouse.get_rel()

                            elif opcao_menu == 1:

                                # Abrir controles
                                estado_jogo = "CONTROLES"

                            elif opcao_menu == 2:

                                # Sair do jogo
                                executando = False

                    elif estado_jogo == "CONTROLES":

                        if evento.key in (
                            pygame.K_ESCAPE,
                            pygame.K_RETURN,
                            pygame.K_KP_ENTER,
                        ):

                            estado_jogo = "MENU"

                # Impede que eventos do menu cheguem ao jogo
                continue

            
            
            # Eventos do menu de pausa
            if estado_jogo == "PAUSADO":

                if evento.type == pygame.KEYDOWN:

                    # Opção anterior
                    if evento.key == pygame.K_UP:
                        opcao_pausa = (
                            opcao_pausa - 1
                        ) % len(OPCOES_PAUSA)

                    # Próxima opção
                    elif evento.key == pygame.K_DOWN:
                        opcao_pausa = (
                            opcao_pausa + 1
                        ) % len(OPCOES_PAUSA)

                    # Esc continua a partida
                    elif evento.key == pygame.K_ESCAPE:
                        estado_jogo = "JOGANDO"
                        mouse_capturado = True

                        pygame.event.set_grab(True)
                        pygame.mouse.set_visible(False)
                        pygame.mouse.get_rel()

                    # Confirma a opção selecionada
                    elif evento.key in (
                        pygame.K_RETURN,
                        pygame.K_KP_ENTER,
                    ):

                        if opcao_pausa == 0:
                            # Continuar
                            estado_jogo = "JOGANDO"
                            mouse_capturado = True

                            pygame.event.set_grab(True)
                            pygame.mouse.set_visible(False)
                            pygame.mouse.get_rel()

                        elif opcao_pausa == 1:
                            # Reiniciar partida
                            reiniciar_pendente = True

                        elif opcao_pausa == 2:
                            # Voltar ao menu principal
                            estado_jogo = "MENU"
                            opcao_menu = 0
                            mouse_capturado = False

                            pygame.event.set_grab(False)
                            pygame.mouse.set_visible(True)
                            pygame.mouse.get_rel()

                # Bloqueia comandos da partida na pausa
                continue



            # Eventos normais da partida
            if evento.type == pygame.KEYDOWN:



                # Solicita reinício após vitória ou derrota
                if evento.key == pygame.K_r and (
                    vida_jogador == 0 or venceu
                ):
                    reiniciar_pendente = True

                    vida_jogador = VIDA_MAXIMA_JOGADOR

                    posicao_jogador = POSICAO_INICIAL
                    angulo_jogador = ANGULO_INICIAL

                    inimigos = criar_inimigos_aleatorios(posicao_jogador)
                    estado_spawn = criar_estado_spawn()

                    tem_chave = False

                    venceu = False
                    estado_jogo = "JOGANDO"

                    tempo_ate_proximo_tiro = 0.0
                    tempo_efeito_tiro = 0.0

                    mostrar_mapa = False
                    mouse_capturado = True

                    pygame.event.set_grab(True)
                    pygame.mouse.set_visible(False)
                    pygame.mouse.get_rel()


                elif evento.key == pygame.K_TAB:
                    mostrar_mapa = not mostrar_mapa

                elif (
                    evento.key == pygame.K_ESCAPE
                    and estado_jogo == "JOGANDO"
                    and vida_jogador > 0
                    and not venceu
                ):
                    estado_jogo = "PAUSADO"
                    opcao_pausa = 0
                    
                    mouse_capturado = False
                
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
                    pygame.mouse.get_rel()

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if (
                    evento.button == 1
                    and mouse_capturado
                    and not mostrar_mapa
                    and tempo_ate_proximo_tiro <= 0
                    and vida_jogador > 0
                    and not venceu
                ):

                    tempo_ate_proximo_tiro = INTERVALO_ENTRE_TIROS
                    tempo_efeito_tiro = DURACAO_EFEITO_TIRO

                    alvo = processar_disparo (posicao_jogador, angulo_jogador, inimigos)

                    if alvo is None:
                        print("DISPARO: nunhum inimigo atingido")
                    else:
                        print("INIMIGO ATINGIDO!" f"Vida restante: {alvo['vida']}")

                        if not alvo ["ativo"]:
                            print("INIMIGO ELIMINADO!")


        deslocamento_x, _ = pygame.mouse.get_rel()

        if (
            estado_jogo == "JOGANDO"
            and mouse_capturado
            and vida_jogador > 0
            and not venceu
        ):
            
            angulo_jogador += (deslocamento_x * SENSIBILIDADE_MOUSE)
            angulo_jogador %= 2 * math.pi

            teclas = pygame.key.get_pressed()

            posicao_jogador = atualizar_posicao(
                posicao_jogador,
                angulo_jogador,
                teclas,
                delta_tempo,
            )

            # Verifica se o jogador coletou a chave
            if not tem_chave:

                if verificar_coleta_chave(posicao_jogador):

                    tem_chave = True

                    print("CHAVE COLETADA!")
                    print("Novos inimigos não serão mais gerados.")

            atualizar_inimigos(
                inimigos, 
                posicao_jogador,
                delta_tempo,
            )

            dano_recebido = atualizar_ataques_inimigos( inimigos, posicao_jogador, delta_tempo,)

            if dano_recebido > 0:
                vida_jogador = max(0, vida_jogador - dano_recebido,)
                print(f"Jogador recebeu {dano_recebido} de dano."
                    f"Vida restante: {vida_jogador}")

            if vida_jogador > 0:

                novo_inimigo = atualizar_spawn(
                    inimigos,
                    posicao_jogador,
                    delta_tempo,
                    estado_spawn,
                    tem_chave,
                )

                if novo_inimigo is not None:
                    print(
                        f"NOVO INIMIGO! Posição: {novo_inimigo}"
                    )


            # Verifica se o objetivo da fase foi concluído
            if (
                vida_jogador > 0
                and not venceu
                and verificar_vitoria(
                    posicao_jogador,
                    tem_chave,
                )
            ):
                venceu = True

                print("FASE CONCLUIDA!")
                print("O jogador encontrou a chave e alcancou a saida.")


        
        # Executa o reinício solicitado
        if reiniciar_pendente:

            # Restaura jogador
            posicao_jogador = POSICAO_INICIAL
            angulo_jogador = ANGULO_INICIAL
            vida_jogador = VIDA_MAXIMA_JOGADOR

            # Restaura inimigos e geração
            inimigos = criar_inimigos_aleatorios(
                posicao_jogador
            )
            estado_spawn = criar_estado_spawn()

            # Restaura objetivos
            tem_chave = False
            venceu = False

            # Restaura efeitos da arma
            tempo_ate_proximo_tiro = 0.0
            tempo_efeito_tiro = 0.0

            # Restaura visualização
            mostrar_mapa = False

            # Inicia a partida
            estado_jogo = "JOGANDO"
            mouse_capturado = True

            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)
            pygame.mouse.get_rel()

            # A solicitação foi atendida
            reiniciar_pendente = False



        if (vida_jogador == 0 or venceu) and mouse_capturado:

            mouse_capturado = False

            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)
            pygame.mouse.get_rel()

        
        # Renderiza o menu principal
        if estado_jogo == "MENU":

            desenhar_menu(
                tela,
                opcao_menu,
                fonte_grande,
                fonte_pequena,
            )

            pygame.display.flip()
            continue

        # Renderiza a tela de controles
        if estado_jogo == "CONTROLES":

            desenhar_controles(
                tela,
                fonte_grande,
                fonte_pequena,
            )

            pygame.display.flip()
            continue


        # Renderização
        if mostrar_mapa:
            tela.fill(COR_FUNDO)
            desenhar_mapa(
                tela,
                posicao_jogador,
                angulo_jogador,
                inimigos,
                tem_chave,
            )
        else:

            profundidades = desenhar_fps(
                tela,
                posicao_jogador,
                angulo_jogador,
                textura_porta,
            )

            if not tem_chave:
                desenhar_chave(
                    tela,
                    posicao_jogador,
                    angulo_jogador,
                    sprite_chave,
                    profundidades,
                )

            desenhar_inimigos(
                tela,
                inimigos,
                posicao_jogador,
                angulo_jogador,
                sprite_inimigo,
                profundidades,
            )


            recuo = 0

            if tempo_efeito_tiro > 0:
                recuo = int(
                    RECUO_MAXIMO
                    * tempo_efeito_tiro
                    / DURACAO_EFEITO_TIRO
                )

            desenhar_arma(
                tela,
                sprite_arma,
                recuo,
            )

            if tempo_efeito_tiro > 0:
                desenhar_flash(
                    tela,
                    sprite_arma,
                    recuo,
                )

            desenhar_mira(tela)

        # Indicador de chave no HUD
        if tem_chave:
            mensagem_chave = "CHAVE: COLETADA"
            cor_chave = (245, 205, 80)
        else:
            mensagem_chave = "CHAVE: PENDENTE"
            cor_chave = (180, 180, 180)

        texto_chave = fonte_hud.render(
            mensagem_chave,
            True,
            cor_chave,
        )

        tela.blit(
            texto_chave,
            (
                LARGURA - texto_chave.get_width() - 25,
                25,
            ),
        )

        # Interface do jogador
        desenhar_hud(
            tela,
            vida_jogador,
            fonte_hud,
        )

        
        # Tela de vitória
        if venceu:
            desenhar_vitoria(
                tela,
                fonte_grande,
                fonte_pequena,
            )

        # Tela de derrota
        elif vida_jogador <= 0:
            desenhar_derrota(
                tela,
                fonte_grande,
                fonte_pequena,
            )

        # Interface de pausa
        if estado_jogo == "PAUSADO":
            desenhar_pausa(
                tela,
                fonte_grande,
                fonte_pequena,
                opcao_pausa,
            )

        pygame.display.flip()


    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)

    pygame.quit()


def desenhar_mapa(tela, posicao_jogador, angulo_jogador, inimigos, tem_chave):

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


    # Representa a saída no mapa superior
    saida_x, saida_y = POSICAO_SAIDA

    pixel_saida_x = int(
        origem_x + saida_x * TAMANHO_CELULA
    )

    pixel_saida_y = int(
        origem_y + saida_y * TAMANHO_CELULA
    )

    # Marcador azul
    retangulo_saida = pygame.Rect(
        pixel_saida_x - 9,
        pixel_saida_y - 9,
        18,
        18,
    )

    pygame.draw.rect(
        tela,
        (55, 145, 220),
        retangulo_saida,
    )

    pygame.draw.rect(
        tela,
        (220, 230, 245),
        retangulo_saida,
        2,
    )



    # Desenha a chave enquanto não foi coletada
    if not tem_chave:

        chave_x, chave_y = POSICAO_CHAVE

        # Converte coordenadas do mundo em pixels
        pixel_chave_x = int(
            origem_x + chave_x * TAMANHO_CELULA
        )

        pixel_chave_y = int(
            origem_y + chave_y * TAMANHO_CELULA
        )

        # Marcador amarelo
        pygame.draw.circle(
            tela,
            (245, 205, 80),
            (pixel_chave_x, pixel_chave_y),
            9,
        )

        # Contorno escuro
        pygame.draw.circle(
            tela,
            (60, 45, 20),
            (pixel_chave_x, pixel_chave_y),
            9,
            2,
        )


    for inimigo in inimigos:
        if not inimigo["ativo"]:
            continue

        inimigo_x, inimigo_y = inimigo["posicao"]

        pixel_inimigo_x = ( origem_x + inimigo_x * TAMANHO_CELULA)

        pixel_inimigo_y = (origem_y + inimigo_y * TAMANHO_CELULA)

        pygame.draw.circle( tela, (210, 70, 70),(
                                                    int(pixel_inimigo_x),
                                                    int(pixel_inimigo_y),
                                                ),
                                                8,
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
