import pygame
import sys
import math
import random

pygame.init()

ANCHO, ALTO = 600, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Golf ¡Encuentra el hoyo!")

# Colores 
VERDE_CESPED = (142, 199, 57)
AZUL_AGUA = (47, 166, 255)
NARANJA_BORDE = (200, 100, 40)
VERDE_OSCURO = (50, 130, 30)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Pelota
radio_pelota = 8
inicio_x = 540
inicio_y = 555
pelota_x = inicio_x
pelota_y = inicio_y
vx, vy = 0, 0
friccion = 0.98
en_movimiento = False

# Hoyo
hoyo_x = 100
hoyo_y = 160
hoyo_radio = 10
victoria = False

# Árboles con sprites
arbol_imgs = [
    pygame.image.load("arbolv.png").convert_alpha(),
    pygame.image.load("arbolr.png").convert_alpha(),
    pygame.image.load("arboln.png").convert_alpha()
]
arbol_imgs = [pygame.transform.scale(img, (40, 40)) for img in arbol_imgs]

arbol_posiciones = [  
    (80, 150), (130, 190), (400, 140), (110, 330),
    (470, 350), (200, 160), (300, 220), (500, 100),
    (50, 250), (520, 270), (150, 100), (430, 300)
]

arboles = []
for pos in arbol_posiciones:
    imagen = random.choice(arbol_imgs)
    rect = imagen.get_rect(topleft=pos)
    arboles.append((pos, imagen, rect))

# Lagos
lagos = [
    (140, 460, 40), (180, 450, 30), (160, 480, 35),
    (120, 440, 25), (180, 490, 25), (260, 310, 20),
    (270, 320, 15), (280, 300, 18), (360, 190, 20),
    (370, 180, 15), (350, 200, 12),
]

golpes = 0
MAX_GOLPES = 7
arrastrando = False
punto_inicio = None

def fondo():
    ventana.fill(VERDE_OSCURO)
    pygame.draw.rect(ventana, VERDE_CESPED, (30, 70, 540, 500))
    pygame.draw.rect(ventana, NARANJA_BORDE, (30, 70, 540, 500), 8)
    pygame.draw.rect(ventana, (80, 40, 20), (470, 520, 100, 40))

    for cx, cy, r in lagos:
        pygame.draw.circle(ventana, AZUL_AGUA, (cx, cy), r)

    for pos, img, rect in arboles:
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

def reiniciar():
    global pelota_x, pelota_y, vx, vy, en_movimiento, victoria, arrastrando, punto_inicio, arboles
    pelota_x, pelota_y = inicio_x, inicio_y
    vx = vy = 0
    en_movimiento = False
    victoria = False
    arrastrando = False
    punto_inicio = None

    # Reiniciar árboles
    arboles.clear()
    for pos in arbol_posiciones:
        imagen = random.choice(arbol_imgs)
        rect = imagen.get_rect(topleft=pos)
        arboles.append((pos, imagen, rect))

reloj = pygame.time.Clock()
campo_rect = pygame.Rect(38, 78, 524, 484)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r and golpes >= MAX_GOLPES:
            golpes = 0
            reiniciar()
        elif evento.type == pygame.MOUSEBUTTONDOWN and not en_movimiento and golpes < MAX_GOLPES:
            if math.hypot(pelota_x - evento.pos[0], pelota_y - evento.pos[1]) <= radio_pelota + 10:
                arrastrando = True
                punto_inicio = evento.pos
        elif evento.type == pygame.MOUSEBUTTONUP and arrastrando:
            punto_fin = evento.pos
            dx = punto_inicio[0] - punto_fin[0]
            dy = punto_inicio[1] - punto_fin[1]
            distancia = math.hypot(dx, dy)
            if distancia > 0:
                fuerza = min(distancia / 10, 10)
                vx = dx / distancia * fuerza
                vy = dy / distancia * fuerza
                en_movimiento = True
                golpes += 1
            arrastrando = False
            punto_inicio = None

    if en_movimiento:
        pelota_x += vx
        pelota_y += vy
        vx *= friccion
        vy *= friccion
        if abs(vx) < 0.1 and abs(vy) < 0.1:
            en_movimiento = False

    pelota_rect = pygame.Rect(pelota_x - radio_pelota, pelota_y - radio_pelota, radio_pelota * 2, radio_pelota * 2)

    if not campo_rect.contains(pelota_rect):
        if pelota_rect.left <= campo_rect.left or pelota_rect.right >= campo_rect.right:
            vx = -vx
        if pelota_rect.top <= campo_rect.top or pelota_rect.bottom >= campo_rect.bottom:
            vy = -vy
        if pelota_rect.left < campo_rect.left:
            pelota_x = campo_rect.left + radio_pelota
        if pelota_rect.right > campo_rect.right:
            pelota_x = campo_rect.right - radio_pelota
        if pelota_rect.top < campo_rect.top:
            pelota_y = campo_rect.top + radio_pelota
        if pelota_rect.bottom > campo_rect.bottom:
            pelota_y = campo_rect.bottom - radio_pelota

    for i in range(len(arboles) - 1, -1, -1):
        pos, img, rect = arboles[i]
        if pelota_rect.colliderect(rect):
            vx = -vx
            vy = -vy
            arboles.pop(i)

    for cx, cy, r in lagos:
        if math.hypot(pelota_x - cx, pelota_y - cy) < r:
            reiniciar()
            break

    if math.hypot(pelota_x - hoyo_x, pelota_y - hoyo_y) < hoyo_radio:
        victoria = True
        en_movimiento = False
        vx = vy = 0

    fondo()
    pygame.display.flip()
    reloj.tick(60)
