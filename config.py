import math

LARGURA = 960
ALTURA = 540
FPS = 60
TITULO = "Mini DOOM"
COR_FUNDO = (25, 25, 35)

#MAPA 2D
TAMANHO_CELULA = 40

#Ambiente
COR_PAREDE = (100, 110, 125)
COR_CHAO = (40, 45, 55)
COR_GRADE = (65, 70, 80)
COR_JOGADOR = (60, 220, 150)

#Jogador
ANGULO_INICIAL = 0.0
CAMPO_VISAO = math.radians(60) #Campo de visão de 60 graus
VELOCIDADE_ROTACAO = math.radians(120) #Velocidade em radianos por seg
VELOCIDADE_MOVIMENTO = 3.0 #Velocidade do jogador em celula por seg
SENSIBILIDADE_MOUSE = 0.003
RAIO_JOGADOR = 0.20