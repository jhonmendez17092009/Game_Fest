import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("sounds/agua.mp3")
pygame.mixer.music.play(-1)

GOLPE = pygame.mixer.Sound("sounds/golpe.mp3")
VICTORIA = pygame.mixer.Sound("sounds/victoria.mp3")

F = (0, 167, 231) 
P = (69, 194, 2)  
A = (203, 189, 147) 
N = (0, 0, 0)    
B = (255, 255, 255) 
R = (255, 0, 0)   

VERDE_CESPED = (142, 199, 57)
AZUL_AGUA = (47, 166, 255)
NARANJA_BORDE = (200, 100, 40)
VERDE_OSCURO = (50, 130, 30)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

ANCHO, ALTO = 600, 760
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Golf Fest")
Clock = pygame.time.Clock()

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
nivel = 1

radio = 10
vx, vy = 0, 0
dragging = False
start_pos = None
golpes_restantes = 8
hole_pos = (300, 340)
hole_radius = 20

arbol_posiciones = [
    (50, 580), (200, 580), (115, 250), (450, 50), (510, 50),
    (520, 110), (520, 170), (220, 330), (250, 290)
]
arboles = [(pos, random.choice(arbol_imgs)) for pos in arbol_posiciones]

pasto_zonas = [
    pygame.Rect(80, 50, 100, 550), pygame.Rect(180, 50, 370, 100),
    pygame.Rect(450, 150, 100, 300), pygame.Rect(270, 350, 180, 100),
    pygame.Rect(10, 550, 250, 150), pygame.Rect(200, 280, 150, 250)
]
arena_zonas = [
    pygame.Rect(80, 150, 100, 50), pygame.Rect(350, 50, 50, 100),
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
    vx = vy = 0
    golpes_restantes = 8

def reset_posicion():
    global ball_x, ball_y, vx, vy
    ball_x = initial_x
    ball_y = initial_y
    vx = vy = 0

reset_nivel()

radio_pelota = 8
inicio_x = 540
inicio_y = 555
pelota_x = inicio_x
pelota_y = inicio_y
vx2, vy2 = 0, 0
friccion = 0.98
en_movimiento = False

hoyo_x = 100
hoyo_y = 160
hoyo_radio = 10
victoria = False

golpes = 0
MAX_GOLPES = 7
arrastrando = False
punto_inicio = None

arbol_posiciones_n2 = [  
    (80, 150), (130, 190), (400, 140), (110, 330),
    (470, 350), (200, 160), (300, 220), (500, 100),
    (50, 250), (520, 270), (150, 100), (430, 300)
]

arboles_n2 = []
for pos in arbol_posiciones_n2:
    imagen = random.choice(arbol_imgs)
    rect = imagen.get_rect(topleft=pos)
    arboles_n2.append((pos, imagen, rect))

lagos = [
    (140, 460, 40), (180, 450, 30), (160, 480, 35),
    (120, 440, 25), (180, 490, 25), (260, 310, 20),
    (270, 320, 15), (280, 300, 18), (360, 190, 20),
    (370, 180, 15), (350, 200, 12),
]

campo_rect = pygame.Rect(38, 78, 524, 484)

def fondo_nivel2():
    ventana.fill(VERDE_OSCURO)
    pygame.draw.rect(ventana, VERDE_CESPED, (30, 70, 540, 500))
    pygame.draw.rect(ventana, NARANJA_BORDE, (30, 70, 540, 500), 8)
    pygame.draw.rect(ventana, (80, 40, 20), (470, 520, 100, 40))
    for cx, cy, r in lagos:
        pygame.draw.circle(ventana, AZUL_AGUA, (cx, cy), r)
    for pos, img, rect in arboles_n2:
        ventana.blit(img, pos)
    pygame.draw.circle(ventana, NEGRO, (hoyo_x, hoyo_y), hoyo_radio)
    pygame.draw.circle(ventana, BLANCO, (int(pelota_x), int(pelota_y)), radio_pelota)
    fuente = pygame.font.SysFont(None, 28)
    texto = fuente.render(f"Golpes: {golpes} / Max Golpes: {MAX_GOLPES}", True, BLANCO)
    ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 10))
    if golpes >= MAX_GOLPES and not victoria:
        mensaje = fuente.render("Presiona R para reiniciar", True, BLANCO)
        ventana.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
    if arrastrando and punto_inicio:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(ventana, NEGRO, (pelota_x, pelota_y), mouse_pos, 2)

def reiniciar_nivel2():
    global pelota_x, pelota_y, vx2, vy2, en_movimiento, victoria, arrastrando, punto_inicio, arboles_n2
    pelota_x, pelota_y = inicio_x, inicio_y
    vx2 = vy2 = 0
    en_movimiento = False
    victoria = False
    arrastrando = False
    punto_inicio = None
    arboles_n2.clear()
    for pos in arbol_posiciones_n2:
        imagen = random.choice(arbol_imgs)
        rect = imagen.get_rect(topleft=pos)
        arboles_n2.append((pos, imagen, rect))

while True:
    Clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if pantalla_inicio and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pantalla_inicio = False
        if nivel == 1:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and golpes_restantes == 0:
                reset_nivel()
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
                    GOLPE.play()
                dragging = False
                start_pos = None
        elif nivel == 2:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and golpes >= MAX_GOLPES:
                golpes = 0
                reiniciar_nivel2()
            elif event.type == pygame.MOUSEBUTTONDOWN and not en_movimiento and golpes < MAX_GOLPES:
                if math.hypot(pelota_x - event.pos[0], pelota_y - event.pos[1]) <= radio_pelota + 10:
                    arrastrando = True
                    punto_inicio = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and arrastrando:
                punto_fin = event.pos
                dx = punto_inicio[0] - punto_fin[0]
                dy = punto_inicio[1] - punto_fin[1]
                distancia = math.hypot(dx, dy)
                if distancia > 0:
                    fuerza = min(distancia / 10, 10)
                    vx2 = dx / distancia * fuerza
                    vy2 = dy / distancia * fuerza
                    en_movimiento = True
                    golpes += 1
                    GOLPE.play()
                arrastrando = False
                punto_inicio = None

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
    elif nivel == 1:
        ventana.fill(F)
        fuente_contador = pygame.font.SysFont("Arial", 25, True)
        ventana.blit(fuente_contador.render(f"Golpes: {golpes_restantes}", True, B), (20, 20))
        for zona in pasto_zonas:
            pygame.draw.rect(ventana, P, zona)
        for zona in arena_zonas:
            pygame.draw.rect(ventana, A, zona)
        ball_rect = pygame.Rect(ball_x - radio, ball_y - radio, radio * 2, radio * 2)
        for pos, img in arboles:
            ventana.blit(img, pos)
            if ball_rect.colliderect(pygame.Rect(pos[0], pos[1], 40, 40)):
                vx = -vx * 1.2
                vy = -vy * 1.2
        if golpes_restantes == 0:
            vx = vy = 0
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
            nivel = 2
            VICTORIA.play()
        if golpes_restantes == 0 and vx == 0 and vy == 0:
            fuente_fin = pygame.font.SysFont("Arial", 35, True)
            ventana.blit(fuente_fin.render("¡Se acabaron los golpes!", True, R), (120, 320))
            ventana.blit(fuente_fin.render("Presiona R para reiniciar", True, B), (100, 370))
    elif nivel == 2:
        if en_movimiento:
            pelota_x += vx2
            pelota_y += vy2
            vx2 *= friccion
            vy2 *= friccion
            if abs(vx2) < 0.1 and abs(vy2) < 0.1:
                en_movimiento = False
        pelota_rect = pygame.Rect(pelota_x - radio_pelota, pelota_y - radio_pelota, radio_pelota * 2, radio_pelota * 2)
        if not campo_rect.contains(pelota_rect):
            if pelota_rect.left <= campo_rect.left or pelota_rect.right >= campo_rect.right:
                vx2 = -vx2
            if pelota_rect.top <= campo_rect.top or pelota_rect.bottom >= campo_rect.bottom:
                vy2 = -vy2
            if pelota_rect.left < campo_rect.left:
                pelota_x = campo_rect.left + radio_pelota
            if pelota_rect.right > campo_rect.right:
                pelota_x = campo_rect.right - radio_pelota
            if pelota_rect.top < campo_rect.top:
                pelota_y = campo_rect.top + radio_pelota
            if pelota_rect.bottom > campo_rect.bottom:
                pelota_y = campo_rect.bottom - radio_pelota
        for i in range(len(arboles_n2) - 1, -1, -1):
            pos, img, rect = arboles_n2[i]
            if pelota_rect.colliderect(rect):
                vx2 = -vx2
                vy2 = -vy2
                arboles_n2.pop(i)
        for cx, cy, r in lagos:
            if math.hypot(pelota_x - cx, pelota_y - cy) < r:
                reiniciar_nivel2()
                break
        if math.hypot(pelota_x - hoyo_x, pelota_y - hoyo_y) < hoyo_radio:
            victoria = True
            en_movimiento = False
            vx2 = vy2 = 0
            VICTORIA.play()
        fondo_nivel2()
    pygame.display.flip()
