import pygame
import random
import sys

pygame.init()

ANCHO = 400
ALTO = 600

NEGRO = (0, 0, 0)
AZUL = (0, 102, 204)
ROJO = (200, 0, 0)
BLANCO = (255, 255, 255)

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("¡Esquiva los cuadrados!")

jugador_ancho = 50
jugador_alto = 50
jugador_x = ANCHO // 2 - jugador_ancho // 2
jugador_y = ALTO - jugador_alto - 10
jugador_velocidad = 5

obs_ancho = 50
obs_alto = 50
obs_x = random.randint(0, ANCHO - obs_ancho)
obs_y = -obs_alto
obs_velocidad = 5

clock = pygame.time.Clock()

fuente = pygame.font.SysFont(None, 36)
puntuacion = 0

while True:
    clock.tick(60)
    ventana.fill(NEGRO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador_x > 0:
        jugador_x -= jugador_velocidad
    if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - jugador_ancho:
        jugador_x += jugador_velocidad

    obs_y += obs_velocidad
    if obs_y > ALTO:
        obs_y = -obs_alto
        obs_x = random.randint(0, ANCHO - obs_ancho)
        puntuacion += 1
        obs_velocidad += 0.5 

    jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_ancho, jugador_alto)
    obs_rect = pygame.Rect(obs_x, obs_y, obs_ancho, obs_alto)

    pygame.draw.rect(ventana, AZUL, jugador_rect)
    pygame.draw.rect(ventana, ROJO, obs_rect)

    if jugador_rect.colliderect(obs_rect):
        texto = fuente.render("¡Perdiste! Puntuación: " + str(puntuacion), True, BLANCO)
        ventana.blit(texto, (50, ALTO // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    texto = fuente.render("Puntos: " + str(puntuacion), True, BLANCO)
    ventana.blit(texto, (10, 10))

    pygame.display.flip()