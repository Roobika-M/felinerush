import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
window_width, window_height = 612, 358
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Feline Rush")

# Load background
background_image = pygame.image.load("bg4.jpg").convert()
background_width = background_image.get_width()

bg1 = 0
bg2 = background_width
speed = 6

# Load the ten images for the cat animation
cat_frames = [pygame.image.load(f"cat_frame{i}.png").convert_alpha() for i in range(1, 11)]

sprite_width = cat_frames[0].get_width()
sprite_height = cat_frames[0].get_height()

cat_x, cat_y = 100, window_height - sprite_height  
frame_index = 0
animation_speed = 0.75 
animation_counter = 0

# Rat’s sprite images
rat_frames = [pygame.image.load(f"rat_frame{i}.png").convert_alpha() for i in range(1, 5)]

# Rat images
rat_width, rat_height = 80, 40  
resized_rat_frames = [pygame.transform.scale(frame, (rat_width, rat_height)) for frame in rat_frames]

# Rat jumping variables
rat_x = window_width / 2 - rat_width / 2
rat_y = window_height - rat_height
rat_ground_y = rat_y  
rat_jump_velocity = -15  
rat_gravity = 1 
rat_velocity_y = 0  
is_jumping = False

rat_frame_index = 0
rat_animation_speed = 0.5
rat_animation_counter = 0

# Score          
score = 0
font = pygame.font.Font(None, 36) 

# Obstacle image
obstacle_image = pygame.image.load("obstacle.png").convert_alpha()
obstacle_width = 40
obstacle_height = 40
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))

# Obstacle list
obstacles = []
obstacle_speed = 8
obstacle_timer = 0
obstacle_interval = 50 

# Replay button
replay_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 50)
game_over = False


def reset_game():
    global bg1, bg2, speed, cat_x, cat_y, frame_index, animation_speed, animation_counter
    global rat_x, rat_y, rat_ground_y, rat_jump_velocity, rat_gravity, rat_velocity_y, is_jumping
    global rat_frame_index, rat_animation_speed, rat_animation_counter, score, obstacles
    global obstacle_speed, obstacle_timer, obstacle_interval, game_over

    bg1 = 0
    bg2 = background_width
    speed = 6
    cat_x, cat_y = 100, window_height - sprite_height
    frame_index = 0
    animation_speed = 0.75
    animation_counter = 0
    rat_x = window_width / 2 - rat_width / 2
    rat_y = window_height - rat_height
    rat_ground_y = rat_y
    rat_jump_velocity = -15
    rat_gravity = 1
    rat_velocity_y = 0
    is_jumping = False
    rat_frame_index = 0
    rat_animation_speed = 0.5
    rat_animation_counter = 0
    score = 0
    obstacles = []
    obstacle_speed = 8
    obstacle_timer = 0
    obstacle_interval = 50
    game_over = False

# Main game loop
while True:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                is_jumping = True
                rat_velocity_y = rat_jump_velocity
            if event.key == pygame.K_r and game_over:
                reset_game()
                continue
            if event.key == pygame.K_q and game_over:
                pygame.quit()
                exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if replay_button.collidepoint((mouse_x, mouse_y)):
                reset_game()
                continue

    if not game_over:
        bg1 -= speed
        bg2 -= speed

        if bg1 <= -background_width:
            bg1 = background_width
        if bg2 <= -background_width:
            bg2 = background_width

        # Update animation frame for cat
        animation_counter += animation_speed
        if animation_counter >= 1:
            animation_counter = 0
            frame_index = (frame_index + 1) % len(cat_frames)

        # Update animation frame for rat
        rat_animation_counter += rat_animation_speed
        if rat_animation_counter >= 1:
            rat_animation_counter = 0
            rat_frame_index = (rat_frame_index + 1) % len(resized_rat_frames)

        # Handle the rat's jump
        if is_jumping:
            rat_velocity_y += rat_gravity
            rat_y += rat_velocity_y
            if rat_y >= rat_ground_y:
                rat_y = rat_ground_y
                is_jumping = False
                rat_velocity_y = 0

        # Generate new obstacles
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            obstacle_timer = 0
            new_obstacle = {"x": window_width, "y": window_height - obstacle_height, "scored": False}
            obstacles.append(new_obstacle)

        # Move and check for collisions with obstacles
        for obstacle in obstacles[:]:
            obstacle["x"] -= obstacle_speed
            if obstacle["x"] < -obstacle_width:
                obstacles.remove(obstacle)

            # Rat successfully passed the obstacle
            if not obstacle["scored"] and obstacle["x"] + obstacle_width < rat_x:
                score += 1
                obstacle["scored"] = True

            # Check for collision with the cat
            if cat_x + sprite_width > obstacle["x"] and cat_x < obstacle["x"] + obstacle_width:
                if cat_y + sprite_height > obstacle["y"]:
                    continue

            # Collision with the rat
            if rat_x + rat_width > obstacle["x"] and rat_x < obstacle["x"] + obstacle_width:
                if rat_y + rat_height > obstacle["y"] and not is_jumping:
                    game_over = True
                    continue

    # Scrolling background
    window.blit(background_image, (bg1, 0))
    window.blit(background_image, (bg2, 0))

    # Draw the stationary cat in the left corner
    window.blit(cat_frames[frame_index], (cat_x, cat_y))

    # Draw the stationary rat in the center with resized dimensions
    window.blit(resized_rat_frames[rat_frame_index], (rat_x, rat_y))

    # Draw obstacles
    for obstacle in obstacles:
        window.blit(obstacle_image, (obstacle["x"], obstacle["y"]))

    # Render and display the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    if game_over:
        # Draw the replay button
        pygame.draw.rect(window, (0, 255, 0), replay_button)

        # Center the text inside the replay button
        replay_text = font.render("Replay", True, (0, 0, 0))
        text_x = replay_button.x + (replay_button.width - replay_text.get_width()) // 2
        text_y = replay_button.y + (replay_button.height - replay_text.get_height()) // 2

        # Draw the replay text
        window.blit(replay_text, (text_x, text_y))
    
    pygame.display.update()
