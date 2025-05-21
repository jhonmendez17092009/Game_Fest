import pygame
import sys
import random
import math

F = (0, 167, 231)  
P = (69, 194, 2)   
L = (219, 119, 0)  
N = (0, 0, 0)     
B = (255, 255, 255) 
R = (255, 0, 0)     
A = (203, 189, 147) 

pygame.init()
ventana = pygame.display.set_mode((600, 760))
pygame.display.set_caption("Golf Fest")
Clock = pygame.time.Clock()

logo = pygame.image.load("logo.jpg")
logo = pygame.transform.scale(logo, (300, 300))
mjs = pygame.image.load("mjs.png")
mjs = pygame.transform.scale(mjs, (600, 780))

pantalla_inicio = True

radio = 10
vx, vy = 0, 0
dragging = False
start_pos = None
golpes_restantes = 8
nivel = 1

hole_pos = (300, 340)
hole_radius = 20

obstaculos = [
    pygame.Rect(50, 580, 30, 30),
    pygame.Rect(200, 580, 30, 30),
    pygame.Rect(120, 250, 20, 150),
    pygame.Rect(450, 50, 30, 30),
    pygame.Rect(510, 50, 30, 30),
    pygame.Rect(520, 110, 30, 30),
    pygame.Rect(520, 170, 30, 30),
    pygame.Rect(220, 330, 30, 30),
    pygame.Rect(250, 290, 30, 30)
]
pasto_zonas = [
    pygame.Rect(80, 50, 100, 550),
    pygame.Rect(180, 50, 370, 100),
    pygame.Rect(450, 150, 100, 300),
    pygame.Rect(270, 350, 180, 100),
    pygame.Rect(10, 550, 250, 150),
    pygame.Rect(200, 280, 150, 250)
]
arena_zonas = [
    pygame.Rect(80, 150, 100, 50),
    pygame.Rect(350, 50, 50, 100),
    pygame.Rect(450, 400, 100, 50)
]

def is_on_safe_zone(x, y):
    ball_rect = pygame.Rect(x - radio, y - radio, radio * 2, radio * 2)
    for zona in pasto_zonas + obstaculos:
        if ball_rect.colliderect(zona):
            return True
    return False

def reset_nivel():
    global ball_x, ball_y, vx, vy, golpes_restantes, initial_x, initial_y
    initial_x = random.randint(120, 170)
    initial_y = random.randint(620, 670)
    ball_x = initial_x
    ball_y = initial_y
    vx = 0
    vy = 0
    golpes_restantes = 8

def reset_posicion():
    global ball_x, ball_y, vx, vy
    ball_x = initial_x
    ball_y = initial_y
    vx = 0
    vy = 0

reset_nivel()

while True:
    Clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pantalla_inicio = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and golpes_restantes == 0:
            reset_nivel()

        if not pantalla_inicio:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if math.hypot(pygame.mouse.get_pos()[0] - ball_x, pygame.mouse.get_pos()[1] - ball_y) < radio + 10:
                    dragging = True
                    start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                end_pos = pygame.mouse.get_pos()
                dx = start_pos[0] - end_pos[0]
                dy = start_pos[1] - end_pos[1]
                if golpes_restantes > 0:
                    vx = dx / 10
                    vy = dy / 10
                    golpes_restantes -= 1
                dragging = False
                start_pos = None

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

        fuente_contador = pygame.font.SysFont("Arial", 25, True)
        contador_texto = fuente_contador.render(f"Golpes: {golpes_restantes}", True, B)
        ventana.blit(contador_texto, (20, 20))

        pygame.draw.ellipse(ventana, P, (10, 550, 250, 150))
        pygame.draw.rect(ventana, P, ((80, 50), (100, 550)))
        pygame.draw.rect(ventana, P, ((180, 50), (370, 100)))
        pygame.draw.rect(ventana, P, ((450, 150), (100, 300)))
        pygame.draw.rect(ventana, P, ((270, 350), (180, 100)))
        pygame.draw.ellipse(ventana, P, (200, 280, 150, 250))

        for arena in arena_zonas:
            pygame.draw.rect(ventana, A, arena)

        ball_rect = pygame.Rect(ball_x - radio, ball_y - radio, radio * 2, radio * 2)
        for obs in obstaculos:
            pygame.draw.rect(ventana, L, obs)
            if ball_rect.colliderect(obs):
                vx = -vx * 1.2
                vy = -vy * 1.2

        if golpes_restantes == 0:
            vx = 0
            vy = 0

        ball_x += vx
        ball_y += vy

        ball_rect = pygame.Rect(ball_x - radio, ball_y - radio, radio * 2, radio * 2)
        en_arena = any(ball_rect.colliderect(arena) for arena in arena_zonas)

        if en_arena:
            vx *= 0.85
            vy *= 0.85
        else:
            vx *= 0.98
            vy *= 0.98

        if abs(vx) < 0.05: vx = 0
        if abs(vy) < 0.05: vy = 0

        if not is_on_safe_zone(ball_x, ball_y):
            reset_posicion()  # ← solo reinicia posición, no los golpes

        if dragging and start_pos:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(ventana, R, (ball_x, ball_y), mouse_pos, 3)

        pygame.draw.circle(ventana, N, hole_pos, hole_radius)

        pygame.draw.circle(ventana, B, (int(ball_x), int(ball_y)), radio)

        if math.hypot(ball_x - hole_pos[0], ball_y - hole_pos[1]) < hole_radius:
            nivel += 1
            reset_nivel()

        if golpes_restantes == 0 and vx == 0 and vy == 0:
            fuente_fin = pygame.font.SysFont("Arial", 35, True)
            texto1 = fuente_fin.render("¡Se acabaron los golpes!", True, R)
            texto2 = fuente_fin.render("Presiona R para reiniciar", True, B)
            ventana.blit(texto1, ((600 - texto1.get_width()) // 2, 320))
            ventana.blit(texto2, ((600 - texto2.get_width()) // 2, 370))

    pygame.display.flip()
