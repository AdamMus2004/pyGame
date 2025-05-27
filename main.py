import pygame
import sys
import os
import random

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magia i miecz")
pygame.init()

# Wczytaj obraz planszy
board_image = pygame.image.load(os.path.join("img", "Plansza.png"))
# Wczytaj obraz kostki
dice_image = pygame.image.load(os.path.join("img", "Kostki.png")).convert_alpha()

# Przygotuj klatki kostki
frames = [dice_image.subsurface((i*128, 0, 128, 128)) for i in range(21)]

# Kolory
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Przycisk
button_rect = pygame.Rect(WIDTH - 200, HEIGHT - 100, 150, 50)
button_font = pygame.font.SysFont(None, 30)

# Stałe dla kostki
SEQUENCE = [4, 6, 5, 1, 2, 3]  # Kolejność cyfr w spritesheet
STATIC_FRAMES = [0, 4, 8, 12, 16, 20]  # Indeksy klatek statycznych (4,6,5,1,2,3)
FPS = 30
REPETITION_COUNT = 1  # Liczba "obrotów" przed zatrzymaniem

# Zmienne do animacji kostki
animation_active = False
animation_frames = []
counter = 0
final_frame = 0

def animate_dice_roll():
    global animation_active, animation_frames, counter, final_frame
    
    # Losuj wynik i znajdź jego indeks
    target = random.randint(1, 6)  # Teraz wszystkie cyfry 1-6 mają szansę 1/6
    target_index = SEQUENCE.index(target)
    
    # Oblicz potrzebne klatki animacji
    animation_frames = []
    for _ in range(REPETITION_COUNT):
        for i in range(len(SEQUENCE)):
            # Dodaj animację przejścia (3 klatki po każdej cyfrze)
            if i != len(SEQUENCE) - 1:  # Pomijamy animację po ostatniej cyfrze (3)
                start = STATIC_FRAMES[i] + 1
                animation_frames.extend([start, start+1, start+2])
    
    # Dodaj ścieżkę do celu
    for i in range(target_index + 1):
        if i != len(SEQUENCE) - 1:
            start = STATIC_FRAMES[i] + 1
            animation_frames.extend([start, start+1, start+2])
    
    counter = 0
    animation_active = True
    final_frame = STATIC_FRAMES[target_index]

# Główna pętla gry
running = True
clock = pygame.time.Clock()
while running:
    mouse_pos = pygame.mouse.get_pos()
    button_hovered = button_rect.collidepoint(mouse_pos)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                animate_dice_roll()
    
    # Wyświetlanie planszy
    screen.fill((0, 0, 0))  # Czyszczenie ekranu
    screen.blit(board_image, (0, 0))  # Wyświetlenie obrazu planszy
    
    # Wyświetlanie kostki
    if animation_active:
        if counter < len(animation_frames):
            dice_frame = frames[animation_frames[counter]]
            counter += 1
        else:
            dice_frame = frames[final_frame]
            animation_active = False
    else:
        # Pokaż ostatnią klatkę lub domyślną, jeśli jeszcze nie było rzutu
        if final_frame:
            dice_frame = frames[final_frame]
        else:
            dice_frame = frames[0]  # Domyślnie pierwsza klatka (4)
    
    # Wyświetl kostkę na środku ekranu
    dice_x = (WIDTH - 150) // 2
    dice_y = (HEIGHT - 150) // 2
    screen.blit(pygame.transform.scale(dice_frame, (150, 150)), (dice_x, dice_y))
    
    # Rysuj przycisk
    button_color = BUTTON_HOVER_COLOR if button_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    button_text = button_font.render("Rzuć kostką", True, BUTTON_TEXT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    
    pygame.display.flip()  # Aktualizacja ekranu
    clock.tick(30)  # Limit do 30 FPS

pygame.quit()
sys.exit()
