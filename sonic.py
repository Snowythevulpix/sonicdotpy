import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sonicdotpy - Home Screen")

# Load and resize the background GIF
background_image = pygame.image.load("background.gif").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Colors
RED = (255, 87, 51)
BLUE = ((0, 255, 255))

# Fonts
font = pygame.font.Font(None, 64)

# Texts
title_text = font.render("Sonicdotpy - made by Ninestails", True, RED)
start_text = font.render("Press SPACE to Start", True, BLUE)

# Calculate Y-coordinate for text at the bottom
title_text_bottom_y = screen_height - 100
start_text_bottom_y = screen_height - 50

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start the game or transition to the next screen
                running = False

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Draw title text at the bottom
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, title_text_bottom_y))

    # Draw start text at the bottom
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, start_text_bottom_y))

    # Update the display
    pygame.display.flip()

# Code to start the game or transition to the next screen goes here
print("Starting the game...")
