import pygame

pygame.init()

# set up the screen window
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Hello Pygame")
clock = pygame.time.Clock()

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.arc(screen, (255, 255, 255), (50, 50, 50, 50), 10, 20, 1)

    pygame.display.flip()

# quit Pygame
pygame.quit()