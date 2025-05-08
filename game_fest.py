import pygame 
import sys 

F = (0, 167, 231)
P = (69, 194, 2)
L = (219, 119, 0)
N = (0, 0, 0)

pygame.init()

# Cambiar a pantalla completa
ventana = pygame.display.set_mode((600, 780))
pygame.display.set_caption("golf")

Clock = pygame.time.Clock()

while 1:
    Clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    ventana.fill(F)

    pygame.draw.ellipse(ventana,P, (10,550,250,150))
    pygame.draw.rect(ventana,P, ((80,50), (100,550)))
    pygame.draw.rect(ventana,P, ((180,50), (370,100)))
    pygame.draw.rect(ventana,P, ((450,150), (100,300)))
    pygame.draw.rect(ventana,P, ((270,350), (180,100)))
    pygame.draw.ellipse(ventana,P, (200,280,150,250))
    pygame.draw.rect(ventana,L, ((50,580), (30,30)))
    pygame.draw.rect(ventana,L, ((200,580), (30,30)))
    pygame.draw.rect(ventana,L, ((95,600), (90,90)))
    pygame.draw.rect(ventana,L, ((115,250), (30,150)))
    pygame.draw.rect(ventana,L, ((450,50), (30,30)))
    pygame.draw.rect(ventana,L, ((510,50), (30,30)))
    pygame.draw.rect(ventana,L, ((520,110), (30,30)))
    pygame.draw.rect(ventana,L, ((520,170), (30,30)))
    pygame.draw.rect(ventana,L, ((220,330), (30,30)))
    pygame.draw.rect(ventana,L, ((250,290), (30,30)))
    pygame.draw.circle(ventana,N, (300,340), 20)
    pygame.draw.rect(ventana,L, ((230,430), (60,60)))




    pygame.display.flip()
