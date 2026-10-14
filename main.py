import pygame

from config import LARGURA, ALTURA, FPS, TITULO, COR_FUNDO


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)

    relogio = pygame.time.Clock()

    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
    
        tela.fill(COR_FUNDO)
        pygame.display.flip()
    
        relogio.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()