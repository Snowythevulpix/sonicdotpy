import time
from pypresence import Presence
import pygame
import sys
import threading
import random
import os

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sonicdotpy - Home Screen")  # Initial window title

# Load and resize the background image
background_image = pygame.image.load(os.path.join("assets", "background.gif")).convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the still, walking, and running GIFs
still_image = pygame.image.load(os.path.join("assets", "still.gif")).convert_alpha()
walking_image = pygame.image.load(os.path.join("assets", "walking.gif")).convert_alpha()
running_image = pygame.image.load(os.path.join("assets", "running.gif")).convert_alpha()

# Set initial sprite and animation variables
current_image = still_image

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 139)  # Dark blue
BLACK = (0, 0, 0)    # Black for obstacles

# Sonic's initial position and velocity
sonic_x = screen_width // 2  # Initial position centered
sonic_y = screen_height // 2
sonic_speed = 2  # Initial speed
sonic_vel_x = 0
sonic_vel_y = 0
gravity = 0.5

# Sonic's dimensions
sonic_width = still_image.get_width()
sonic_height = still_image.get_height()

# Floor properties
floor_height = 100

# Discord Rich Presence client ID
client_id = "1212820562452160592"

# Initialize Discord Rich Presence
RPC = Presence(client_id)
RPC.connect()

# Update Discord Rich Presence in a separate thread
def update_presence():
    while True:
        RPC.update(
            large_image="sonic_icon",
            details="Playing Sonicdotpy",
            state="In-game",
            start=int(time.time())
        )
        time.sleep(15)  # Update every 15 seconds

# Start the thread to update presence
threading.Thread(target=update_presence, daemon=True).start()

# List to hold obstacle positions
obstacles = []

# Generate obstacles
def generate_obstacles():
    # Generate obstacles as Sonic moves to the right
    if sonic_vel_x > 0:
        obstacle_y = random.randint(floor_height, screen_height - 100)
        obstacle_x = random.randint(screen_width, screen_width + 200)  # Adjusted obstacle spawn area
        obstacles.append(pygame.Rect(obstacle_x, obstacle_y, 5, sonic_height))  # Adjusted obstacle size

# Main loop
running = True
playing = False
last_direction = "right"  # Initially facing right
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        playing = True
        pygame.display.set_caption("Sonicdotpy - Playing")  # Change window title when playing

    if playing:
        current_time = pygame.time.get_ticks() / 1000

        if keys[pygame.K_LEFT]:
            sonic_vel_x = -sonic_speed
            current_image = pygame.transform.flip(walking_image, True, False)  # Mirror the sprite when moving left
            last_direction = "left"
        elif keys[pygame.K_RIGHT]:
            sonic_vel_x = sonic_speed
            current_image = walking_image
            last_direction = "right"
        else:
            sonic_vel_x = 0
            if sonic_vel_y == 0:  # Check if Sonic is not moving horizontally or vertically
                if last_direction == "left":
                    current_image = pygame.transform.flip(still_image, True, False)  # Mirror still.gif
                else:
                    current_image = still_image

        sonic_x += sonic_vel_x

        # Apply gravity to Sonic
        sonic_vel_y += gravity
        sonic_y += sonic_vel_y

        # Check if Sonic is touching the floor
        if sonic_y + sonic_height >= screen_height - floor_height:
            sonic_y = screen_height - floor_height - sonic_height
            sonic_vel_y = 0

        # Limit Sonic's movement within the screen boundaries
        sonic_x = max(0, min(sonic_x, screen_width - sonic_width))

        # Generate obstacles
        generate_obstacles()

        # Draw playing screen
        screen.fill(BLUE)  # Dark blue background

        # Draw the floor
        pygame.draw.rect(screen, WHITE, (0, screen_height - floor_height, screen_width, floor_height))

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)

        # Draw Sonic
        screen.blit(current_image, (sonic_x, sonic_y))

    else:
        # Draw home screen
        screen.blit(background_image, (0, 0))

    # Update the display
    pygame.display.flip()

# Close Discord Rich Presence connection when the game exits
RPC.close()
