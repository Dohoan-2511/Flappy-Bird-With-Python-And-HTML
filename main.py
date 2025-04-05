import pygame, sys, random

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    gap_size = 150
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos - gap_size - pipe_surface.get_height()))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    new_pipes = []
    for pipe in pipes:
        pipe.centerx -= 5
        if pipe.right > 0:  # Chỉ giữ lại các ống còn trên màn hình
            new_pipes.append(pipe)
    return new_pipes

def draw_floor():
    screen.blit(floor, (floor_x_pos, 500))
    screen.blit(floor, (floor_x_pos + floor.get_width(), 500))

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 600:
        return False
    return True

def rotate_bird(bird1):
    return pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(400, 50))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(400, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_core)}', True, (255, 255, 255)) # chu day nhe 
        high_score_rect = high_score_surface.get_rect(center=(400, 400))
        screen.blit(high_score_surface, high_score_rect)



def update_score(score,high_core):
    if score > high_core:
        high_core = score  # Cập nhật high score khi kết thúc game
    return high_core

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
# Khởi tạo pygame và màn hình
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Biến game
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_core = 0
game_font = pygame.font.Font('Filegame/04B_19.TTF', 40)

# Load hình ảnh
bg = pygame.image.load('FileGame/assets/background-night.png')
bg = pygame.transform.scale(bg, (800, 600))
floor = pygame.image.load('FileGame/assets/floor.png')
floor = pygame.transform.scale2x(floor)

floor_x_pos = 0

# Chim
bird = pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 384))

# Ống
pipe_surface = pygame.image.load('FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [400, 300, 200]

# tao man hinh ket thuc
game_over_surface = pygame.image.load('FileGame/assets/message.png').convert_alpha()
game_over_react = game_over_surface.get_rect(center=(400, 200))


#chen am thanh 
flap_sound = pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
# Vòng lặp game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -11
                #chen tam thanh     
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 200)
                bird_movement = 0
                score = 0  # Reset điểm khi restart
        if event.type == spawnpipe: 
            pipe_list.extend(create_pipe())

    screen.blit(bg, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipe(pipe_list) 
        score += 0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_react) 
        high_core = update_score(score,high_core)  # Cập nhật high score
        if score > high_core:
            high_core = score  # Cập nhật high score khi kết thúc game
        score_display('game_over')

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -floor.get_width():
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
