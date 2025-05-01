import pygame, sys, time, random

speed = 15

# Window size
frame_size_x = 1380
frame_size_y = 840

check_errors = pygame.init()

if check_errors[1] > 0:
    print("Error " + str(check_errors[1]))
else:
    print("Game successfully initialized")

# Initialize game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

fps_controller = pygame.time.Clock()

# Square size (snake body and food)
square_size = 60

# Initialize game variables
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_spawn = True
    score = 0

init_vars()

# Display score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()

    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)

    game_window.blit(score_surface, score_rect)

# Display game over message
def game_over():
    game_over_font = pygame.font.SysFont('consolas', 50)
    game_over_surface = game_over_font.render("GAME OVER", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 3)
    game_window.blit(game_over_surface, game_over_rect)

    restart_font = pygame.font.SysFont('consolas', 30)
    restart_surface = restart_font.render("Press R to Restart or Q to Quit", True, white)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (frame_size_x / 2, frame_size_y / 2)
    game_window.blit(restart_surface, restart_rect)

    pygame.display.update()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == ord("w")) and direction != "DOWN":
                direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == ord("s")) and direction != "UP":
                direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == ord("a")) and direction != "RIGHT":
                direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == ord("d")) and direction != "LEFT":
                direction = "RIGHT"

    # Move the snake
    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size

    # Check for boundary collision and wrap around
    if head_pos[0] < 0 or head_pos[0] >= frame_size_x or head_pos[1] < 0 or head_pos[1] >= frame_size_y:
        game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:  # Restart the game
                    init_vars()  # Reset the game variables and start over
                    break
    else:
        # Eating food
        snake_body.insert(0, list(head_pos))
        if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawn new food if eaten
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                        random.randrange(1, (frame_size_y // square_size)) * square_size]
            food_spawn = True

        # Graphics: Draw everything
        game_window.fill(black)

        # Draw snake body
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0] + 2, pos[1] + 2, square_size - 2, square_size - 2))

        # Draw food
        pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], square_size, square_size))

        # Check for collision with self
        for block in snake_body[1:]:
            if head_pos[0] == block[0] and head_pos[1] == block[1]:
                game_over()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:  # Quit the game
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_r:  # Restart the game
                            init_vars()  # Reset the game variables and start over
                            break

        # Show score
        show_score(1, white, 'consolas', 20)

        pygame.display.update()

        # Control game speed
        fps_controller.tick(speed)

