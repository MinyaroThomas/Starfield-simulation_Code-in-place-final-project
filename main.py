import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starfield Simulation - Code in Place Final Project")

# Colors
BACKGROUND = (10, 10, 30)
STAR_COLORS = [
    (255, 255, 255),  # White
    (200, 200, 255),  # Light blue
    (255, 240, 200),  # Light yellow
    (200, 255, 200),  # Light green
    (255, 200, 200)   # Light red
]
TEXT_COLOR = (220, 220, 255)
HIGHLIGHT_COLOR = (100, 200, 255)

# Star class
class Star:
    def __init__(self):
        self.reset()
        self.z = random.uniform(0.1, 1.0)  # Initial depth
        
    def reset(self):
        # Start from the center with a random direction
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, WIDTH // 2)
        self.x += math.cos(angle) * distance
        self.y += math.sin(angle) * distance
        self.z = random.uniform(0.1, 1.0)  # Depth
        self.speed = random.uniform(0.05, 0.2)
        self.color = random.choice(STAR_COLORS)
        self.size = random.uniform(1.0, 3.0)
        
    def update(self):
        # Move star toward viewer
        self.z += self.speed
        
        # If star has passed the viewer, reset it
        if self.z > 10:
            self.reset()
            
    def draw(self, surface):
        # Calculate star position based on depth
        x = self.x / self.z + WIDTH // 2 * (1 - 1 / self.z)
        y = self.y / self.z + HEIGHT // 2 * (1 - 1 / self.z)
        
        # Calculate size based on depth
        current_size = self.size / self.z
        
        # Draw the star
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            # Draw glow effect
            glow_size = current_size * 2
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.color, 50), (glow_size, glow_size), glow_size)
            surface.blit(glow_surf, (x - glow_size, y - glow_size))
            
            # Draw the star itself
            pygame.draw.circle(surface, self.color, (x, y), current_size)

# Create stars
stars = [Star() for _ in range(300)]

# Create a constellation of special stars
constellation = []
for _ in range(15):
    star = Star()
    star.speed = random.uniform(0.01, 0.03)  # Slower moving
    star.color = HIGHLIGHT_COLOR
    star.size = random.uniform(2.0, 4.0)
    constellation.append(star)
stars.extend(constellation)

# Font setup
title_font = pygame.font.SysFont("Arial", 48, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 28)
info_font = pygame.font.SysFont("Arial", 20)

# Animation variables
rotation = 0
scale = 1.0
pulse_dir = 0.01

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                # Reset all stars
                for star in stars:
                    star.reset()
    
    # Update stars
    for star in stars:
        star.update()
    
    # Update animation variables
    rotation += 0.2
    scale += pulse_dir
    if scale > 1.1 or scale < 0.9:
        pulse_dir *= -1
    
    # Draw everything
    screen.fill(BACKGROUND)
    
    # Draw stars
    for star in stars:
        star.draw(screen)
    
    # Draw title with animation
    title_text = title_font.render("Starfield Simulation", True, TEXT_COLOR)
    subtitle_text = subtitle_font.render("Code in Place Final Project", True, HIGHLIGHT_COLOR)
    
    # Apply pulsing effect to title
    scaled_title = pygame.transform.rotozoom(title_text, 0, scale)
    scaled_subtitle = pygame.transform.rotozoom(subtitle_text, 0, scale)
    
    screen.blit(scaled_title, (WIDTH//2 - scaled_title.get_width()//2, 50))
    screen.blit(scaled_subtitle, (WIDTH//2 - scaled_subtitle.get_width()//2, 110))
    
    # Draw instructions
    instructions = [
        "Press R: Reset simulation",
        "Press ESC: Exit",
        "Click: Create a new star",
        f"Stars: {len(stars)}"
    ]
    
    for i, text in enumerate(instructions):
        text_surf = info_font.render(text, True, TEXT_COLOR)
        screen.blit(text_surf, (20, HEIGHT - 120 + i*30))
    
    # Draw physics info
    physics_info = [
        "Physics:",
        f"- Star speed: {stars[0].speed:.2f} to {stars[-1].speed:.2f}",
        f"- Star depth: {min(s.z for s in stars):.2f} to {max(s.z for s in stars):.2f}"
    ]
    
    for i, text in enumerate(physics_info):
        text_surf = info_font.render(text, True, HIGHLIGHT_COLOR)
        screen.blit(text_surf, (WIDTH - 250, HEIGHT - 150 + i*30))
    
    # Draw interactive message
    mouse_pos = pygame.mouse.get_pos()
    if 100 < mouse_pos[0] < WIDTH - 100 and 400 < mouse_pos[1] < 500:
        interact_text = info_font.render("Click anywhere to add a star!", True, HIGHLIGHT_COLOR)
        screen.blit(interact_text, (WIDTH//2 - interact_text.get_width()//2, 450))
    
    # Handle mouse clicks
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_star = Star()
        new_star.x = (mouse_x - WIDTH//2) * new_star.z
        new_star.y = (mouse_y - HEIGHT//2) * new_star.z
        new_star.z = random.uniform(0.1, 0.5)  # Start closer
        stars.append(new_star)
        # Wait a bit to prevent too many stars at once
        pygame.time.delay(100)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
