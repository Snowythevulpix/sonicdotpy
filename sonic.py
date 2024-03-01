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
gravity = 0.025 
jump_power = 10  # Initial jump power
is_jumping = False

# Sonic's dimensions
sonic_width = still_image.get_width()
sonic_height = still_image.get_height()

# Enemy properties
enemy_width = sonic_width  # Match player's width
enemy_height = sonic_height  # Match player's height
enemy_speed = 0.5
enemy_spawn_delay = 3  # in seconds
enemy_spawn_timer = enemy_spawn_delay

# Load the enemy image and print debug information
enemy_img = pygame.image.load(os.path.join("assets", "enemy1.png")).convert_alpha()
print("Enemy Image Dimensions:", enemy_img.get_width(), "x", enemy_img.get_height())

# Floor properties
floor_height = 100

# Discord Rich Presence client ID
client_id = "1212820562452160592"

# Initialize Discord Rich Presence
try:
    RPC = Presence(client_id)
    RPC.connect()
except Exception as e:
    print("Error initializing Discord Rich Presence:", e)

# Update Discord Rich Presence in a separate thread
def update_presence():
    while True:
        try:
            RPC.update(
                large_image="sonic_icon",
                details="Playing Sonicdotpy",
                state="In-game",
                start=int(time.time())
            )
            time.sleep(15)  # Update every 15 seconds
        except Exception as e:
            print("Error updating Discord Rich Presence:", e)
            break

# Start the thread to update presence if RPC is initialized
if 'RPC' in globals():
    threading.Thread(target=update_presence, daemon=True).start()

class Enemy:
    def __init__(self):
        self.x = random.randint(0, screen_width - enemy_width)  # Spawn at a random x position
        self.y = screen_height - floor_height - enemy_height  # Spawn on the floor
        self.vel_x = enemy_speed  # Initial movement direction

    def move(self):
        self.x += self.vel_x

        # Bounce off the screen edges
        if self.x <= 0 or self.x + enemy_width >= screen_width:
            self.vel_x *= -1

    def draw(self, screen):
        screen.blit(enemy_img, (self.x, self.y))

# Create an instance of the enemy
current_enemy = None

# Main loop
running = True
playing = False
last_direction = "right"  # Initially facing right
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click event
            if not playing:  # Start the game if not already playing
                playing = True
                pygame.display.set_caption("Sonicdotpy - Playing")  # Change window title when playing
        elif event.type == pygame.KEYDOWN:  # Check for key press events
            if event.key == pygame.K_SPACE and not is_jumping:  # Check if spacebar is pressed and Sonic is not already jumping
                sonic_vel_y = -jump_power
                is_jumping = True

    keys = pygame.key.get_pressed()
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
            is_jumping = False  # Reset jumping state when landing

        # Limit Sonic's movement within the screen boundaries
        sonic_x = max(0, min(sonic_x, screen_width - sonic_width))

        # Spawn enemy
        enemy_spawn_timer -= 1 / 60  # Decrease the timer based on the frame rate
        if enemy_spawn_timer <= 0:
            current_enemy = Enemy()
            enemy_spawn_timer = enemy_spawn_delay

        # Check for collision with the enemy
        if current_enemy and sonic_x < current_enemy.x + enemy_width and \
                sonic_x + sonic_width > current_enemy.x and \
                sonic_y < current_enemy.y + enemy_height and \
                sonic_y + sonic_height > current_enemy.y:
            print("Game Over, Sonic Died")
            running = False

        # Draw playing screen
        screen.fill(BLUE)  # Dark blue background

        # Draw the floor
        pygame.draw.rect(screen, WHITE, (0, screen_height - floor_height, screen_width, floor_height))

        # Draw Sonic
        screen.blit(current_image, (sonic_x, sonic_y))
        
        # Move and draw enemy
        if current_enemy:
            current_enemy.move()
            current_enemy.draw(screen)

    else:
        # Draw home screen
        screen.blit(background_image, (0, 0))

    # Update the display
    pygame.display.flip()

# Close Discord Rich Presence connection when the game exits
if 'RPC' in globals():
    RPC.close()
