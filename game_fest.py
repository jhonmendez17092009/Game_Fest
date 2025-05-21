import pygame
import sys
import random

F = (0, 167, 231)
P = (69, 194, 2)
L = (219, 119, 0)
N = (0, 0, 0)
B = (255, 255, 255)
R = (255, 0, 0)

c_1 = random.randint(120, 170)
c_2 = random.randint(620, 670)

pygame.init()

ventana = pygame.display.set_mode((600, 780))
pygame.display.set_caption("Golf Fest")
Clock = pygame.time.Clock()

logo = pygame.image.load("logo.jpg")
logo = pygame.transform.scale(logo, (300, 300))

mjs = pygame.image.load("mjs.png")
mjs = pygame.transform.scale(mjs, (600, 780))

pantalla_inicio = True

while True:
    Clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                pantalla_inicio = False

    if pantalla_inicio:
        ventana.blit(mjs, (0, 0))

        ventana.blit(logo, (150, 80))
        font = pygame.font.SysFont(None, 60)
        texto = font.render("Bienvenidos al Golf Fest", True, B)
        ventana.blit(texto, (60, 400))
        fuente_arial = pygame.font.SysFont("Arial", 35, 1, 1)
        ventana.blit(fuente_arial.render("Para seguir presione", 1, B), (60, 450))
        ventana.blit(fuente_arial.render("ESPACIO", 1, R), (410, 450))
        fuente_arial = pygame.font.SysFont("Arial", 20, 1, 1)
        ventana.blit(fuente_arial.render("Mariangel Ortegate", 1, B), (200, 580))
        ventana.blit(fuente_arial.render("Jhoasnel Mendez", 1, B), (210, 610))
        ventana.blit(fuente_arial.render("Sofia Galvis", 1, B), (230, 640))

    else:
        ventana.fill(F)

        # Pasto
        pygame.draw.ellipse(ventana, P, (10, 550, 250, 150))
        pygame.draw.rect(ventana, P, ((80, 50), (100, 550)))
        pygame.draw.rect(ventana, P, ((180, 50), (370, 100)))
        pygame.draw.rect(ventana, P, ((450, 150), (100, 300)))
        pygame.draw.rect(ventana, P, ((270, 350), (180, 100)))
        pygame.draw.ellipse(ventana, P, (200, 280, 150, 250))
        # Obstáculos
        pygame.draw.rect(ventana, L, ((50, 580), (30, 30)))
        pygame.draw.rect(ventana, L, ((200, 580), (30, 30)))
        pygame.draw.rect(ventana, L, ((115, 250), (30, 150)))
        pygame.draw.rect(ventana, L, ((450, 50), (30, 30)))
        pygame.draw.rect(ventana, L, ((510, 50), (30, 30)))
        pygame.draw.rect(ventana, L, ((520, 110), (30, 30)))
        pygame.draw.rect(ventana, L, ((520, 170), (30, 30)))
        pygame.draw.rect(ventana, L, ((220, 330), (30, 30)))
        pygame.draw.rect(ventana, L, ((250, 290), (30, 30)))
        # Hoyo
        pygame.draw.circle(ventana, N, (300, 340), 30)
        # Pelota
        pygame.draw.circle(ventana, B, (c_1, c_2), 20)

    pygame.display.flip()
