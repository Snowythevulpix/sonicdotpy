import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sonicdotpy - Home Screen")  # Initial window title

# Load and resize the background image
background_image = pygame.image.load("background.gif").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the still, walking, and running GIFs
still_image = pygame.image.load("still.gif").convert_alpha()
walking_image = pygame.image.load("walking.gif").convert_alpha()
running_image = pygame.image.load("running.gif").convert_alpha()

# Set initial sprite and animation variables
current_image = still_image
animation_start_time = 0
animation_duration = 2  # in seconds

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 139)  # Dark blue

# Sonic's initial position and velocity
sonic_x = screen_width // 2
sonic_y = screen_height // 2
sonic_vel_x = 0
sonic_vel_y = 0
gravity = 0.5

# Sonic's dimensions
sonic_width = still_image.get_width()
sonic_height = still_image.get_height()

# Floor properties
floor_height = 100

# Movement timer
movement_timer = 0

# Camera position
camera_x = 0

# Sonic speed
sonic_speed = 2

# Main loop
running = True
playing = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playing = True
                pygame.display.set_caption("Sonicdotpy - Playing")  # Change window title when playing

    keys = pygame.key.get_pressed()
    if playing:
        current_time = pygame.time.get_ticks() / 1000

        if keys[pygame.K_LEFT]:
            sonic_vel_x = -sonic_speed
            current_image = pygame.transform.flip(walking_image, True, False)  # Mirror the sprite when moving left
            movement_timer += 1 / 60  # Assuming 60 frames per second
        elif keys[pygame.K_RIGHT]:
            sonic_vel_x = sonic_speed
            current_image = walking_image
            movement_timer += 1 / 60
        else:
            sonic_vel_x = 0
            current_image = still_image
            movement_timer = 0

        sonic_x += sonic_vel_x

        # Apply gravity to Sonic
        sonic_vel_y += gravity
        sonic_y += sonic_vel_y

        # Check if Sonic is touching the floor
        if sonic_y + sonic_height >= screen_height - floor_height:
            sonic_y = screen_height - floor_height - sonic_height
            sonic_vel_y = 0

        # Transition to running if moving for one second
        if movement_timer >= 1 and current_image == walking_image:
            current_image = running_image

        # Update camera position to follow Sonic
        camera_x = max(0, min(sonic_x - screen_width // 2, screen_width - screen_width))

        # Draw playing screen
        screen.fill(BLUE)  # Dark blue background

        # Draw the floor
        pygame.draw.rect(screen, WHITE, (0, screen_height - floor_height, screen_width, floor_height))

        # Draw Sonic
        screen.blit(current_image, (sonic_x - camera_x, sonic_y))

    else:
        # Draw home screen
        screen.blit(background_image, (0, 0))

    # Update the display
    pygame.display.flip()
