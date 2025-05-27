import pygame
import sys
import os

WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magia i Miecz")
pygame.init()

# Wczytaj obraz planszy
board_image = pygame.image.load(os.path.join("img", "Plansza.png"))


# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Wyświetlanie planszy
    screen.fill((0, 0, 0))  # Czyszczenie ekranu
    screen.blit(board_image, (0, 0))  # Wyświetlenie obrazu planszy
    
    pygame.display.flip()  # Aktualizacja ekranu

pygame.quit()
sys.exit()
