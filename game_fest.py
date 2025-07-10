import pygame
import sys
import random
import math

F = (0, 167, 231) 
P = (69, 194, 2)  
A = (203, 189, 147) 
N = (0, 0, 0)    
B = (255, 255, 255) 
R = (255, 0, 0)   

pygame.init()
ventana = pygame.display.set_mode((600, 760))
pygame.display.set_caption("Golf Fest")
Clock = pygame.time.Clock()

AGUA = pygame.mixer.music.load("sounds/agua.mp3")
pygame.mixer.music.play(1,0.0)

GOLPE = pygame.mixer.Sound("sounds/golpe.mp3")
VICTORIA = pygame.mixer.Sound("sounds/victoria.mp3")

logo = pygame.image.load("logo.jpg")
logo = pygame.transform.scale(logo, (300, 300))
mjs = pygame.image.load("mjs.png")
mjs = pygame.transform.scale(mjs, (600, 780))

arbol_imgs = [
    pygame.image.load("arbolv.png").convert_alpha(),
    pygame.image.load("arbolr.png").convert_alpha(),
    pygame.image.load("arboln.png").convert_alpha()
]
arbol_imgs = [pygame.transform.scale(img, (40, 40)) for img in arbol_imgs]

pantalla_inicio = True
radio = 10
vx, vy = 0, 0
dragging = False
start_pos = None
golpes_restantes = 8
nivel = 1
hole_pos = (300, 340)
hole_radius = 20

arbol_posiciones = [
    (50, 580),
    (200, 580),
    (115, 250),
    (450, 50),
    (510, 50),
    (520, 110),
    (520, 170),
    (220, 330),
    (250, 290)
]
arboles = [(pos, random.choice(arbol_imgs)) for pos in arbol_posiciones]

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
    for zona in pasto_zonas + [pygame.Rect(p[0], p[1], 40, 40) for p, _ in arboles]:
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
        fuente = pygame.font.SysFont("Arial", 50)
        ventana.blit(fuente.render("Bienvenidos al Golf Fest", True, B), (60, 400))
        fuente = pygame.font.SysFont("Arial", 30, True)
        ventana.blit(fuente.render("Para seguir presione", True, B), (100, 450))
        ventana.blit(fuente.render("ESPACIO", True, R), (420, 450))
        fuente = pygame.font.SysFont("Arial", 20, True)
        ventana.blit(fuente.render("Mariangel Ortegate", True, B), (200, 580))
        ventana.blit(fuente.render("Jhoasnel Mendez", True, B), (210, 610))
        ventana.blit(fuente.render("Sofia Galvis", True, B), (230, 640))
    else: 
        ventana.fill(F)

        fuente_contador = pygame.font.SysFont("Arial", 25, True)
        ventana.blit(fuente_contador.render(f"Golpes: {golpes_restantes}", True, B), (20, 20))

        pygame.draw.ellipse(ventana, P, (10, 550, 250, 150))
        pygame.draw.rect(ventana, P, (80, 50, 100, 550))
        pygame.draw.rect(ventana, P, (180, 50, 370, 100))
        pygame.draw.rect(ventana, P, (450, 150, 100, 300))
        pygame.draw.rect(ventana, P, (270, 350, 180, 100))
        pygame.draw.ellipse(ventana, P, (200, 280, 150, 250))

        for zona in arena_zonas:
            pygame.draw.rect(ventana, A, zona)

        ball_rect = pygame.Rect(ball_x - radio, ball_y - radio, radio * 2, radio * 2)
        for pos, img in arboles:
            ventana.blit(img, pos)
            if ball_rect.colliderect(pygame.Rect(pos[0], pos[1], 40, 40)):
                vx = -vx * 1.2
                vy = -vy * 1.2

        if golpes_restantes == 0:
            vx = 0
            vy = 0

        ball_x += vx
        ball_y += vy
        ball_rect = pygame.Rect(ball_x - radio, ball_y - radio, radio * 2, radio * 2)
        en_arena = any(ball_rect.colliderect(zona) for zona in arena_zonas)

        if en_arena:
            vx *= 0.85
            vy *= 0.85
        else:
            vx *= 0.98
            vy *= 0.98

        if abs(vx) < 0.05: vx = 0
        if abs(vy) < 0.05: vy = 0

        if not is_on_safe_zone(ball_x, ball_y):
            reset_posicion()

        if dragging and start_pos:
            pygame.draw.line(ventana, R, (ball_x, ball_y), pygame.mouse.get_pos(), 3)

        pygame.draw.circle(ventana, N, hole_pos, hole_radius)

        pygame.draw.circle(ventana, B, (int(ball_x), int(ball_y)), radio)

        if math.hypot(ball_x - hole_pos[0], ball_y - hole_pos[1]) < hole_radius:
            nivel += 1
            reset_nivel()

        if golpes_restantes == 0 and vx == 0 and vy == 0:
            fuente_fin = pygame.font.SysFont("Arial", 35, True)
            ventana.blit(fuente_fin.render("¡Se acabaron los golpes!", True, R), (120, 320))
            ventana.blit(fuente_fin.render("Presiona R para reiniciar", True, B), (100, 370))

    pygame.display.flip()
