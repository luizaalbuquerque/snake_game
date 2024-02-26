from tkinter import font
import pygame
import random

pygame.init()
square_width = 750
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 36)

def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]


def reset():
    target.center = generate_starting_position()
    snake_pixel.center = generate_starting_position()
    return snake_pixel.copy()


def is_out_of_bounds():
    return snake_pixel.bottom > square_width or snake_pixel.top < 0 \
        or snake_pixel.left < 0 or snake_pixel.right > square_width


snake_pixel = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1

target = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
target.center = generate_starting_position()

# Initial speed and speed increment
speed = 5
speed_increment = 1

# setting boolean to false 
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #  screen background
    screen.fill("black")

    # Game over message for user 
    if game_over:
        text = font.render("Game Over! Press any key to restart.", True, (255, 255, 255))
        text_rect = text.get_rect(center=(square_width // 2, square_width // 2))
        screen.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if any(keys):
            game_over = False
            snake_pixel.center = generate_starting_position()
            snake = [snake_pixel.copy()]
            snake_length = 1
            continue

    if is_out_of_bounds():
        game_over = True

    if not game_over:
        if snake_pixel.center == target.center:
            target.center = generate_starting_position()
            snake_length += 1
            snake.append(snake_pixel.copy())

            # Snake movement speed 
            speed += speed_increment

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            snake_direction = (0, -pixel_width)
        if keys[pygame.K_s]:
            snake_direction = (0, pixel_width)
        if keys[pygame.K_a]:
            snake_direction = (-pixel_width, 0)
        if keys[pygame.K_d]:
            snake_direction = (pixel_width, 0)

        for snake_part in snake:
            pygame.draw.rect(screen, "green", snake_part)

        pygame.draw.rect(screen, "red", target)

        snake_pixel.move_ip(snake_direction)
        snake.append(snake_pixel.copy())
        snake = snake[-snake_length:]

    pygame.display.flip()

    clock.tick(speed)

pygame.quit()
