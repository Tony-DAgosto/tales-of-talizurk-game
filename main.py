import pygame
from sys import exit

pygame.init()

# CONSTANTS
WORLD_WIDTH = 5000
WORLD_HEIGHT = 5000
screen = pygame.display.set_mode((1600,1000), pygame.RESIZABLE)
clock = pygame.time.Clock()
player_rect = pygame.Rect((WORLD_WIDTH // 2,WORLD_HEIGHT // 2,65,65))
speed = 8

# Dialogue font
dialogue_font = pygame.font.Font("Fonts/Minecraftia-Regular.ttf", 40)
npc1_e2start = dialogue_font.render("Press E to speak with Williard.", False, 'Black') # diff colors 4 testing
npc1_task_desc = dialogue_font.render("Task description.", False, 'White')

nearby_npc = None

# Rocks
landmark_list = [
    pygame.Rect(400, 400, 100, 100),
    pygame.Rect(500, 1400, 100, 100),
    pygame.Rect(375, 2900, 100, 100),
    pygame.Rect(675, 3400, 100, 100),
    pygame.Rect(800, 4700, 100, 100),
    pygame.Rect(1650, 400, 100, 100),
    pygame.Rect(2250, 1700, 100, 100),
    pygame.Rect(3650, 2200, 100, 100),
    pygame.Rect(4400, 900, 100, 100),
    pygame.Rect(1650, 3300, 100, 100),
    pygame.Rect(2650, 2650, 100, 100),
    pygame.Rect(3050, 700, 100, 100),
    pygame.Rect(4200, 4650, 100, 100),
    pygame.Rect(3700, 3950, 100, 100),
    pygame.Rect(4800, 4700, 100, 100)
]

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, color, dialogue_popup, name):
        super().__init__()
        self.rect = pygame.Rect(x, y, 65, 65)
        self.color = color
        self.dialogue_popup = dialogue_popup
        self.hitbox = self.rect.inflate(200,200)
        self.name = name
        
f_npc = NPC(2000, 2600, 'Blue4', "Here is your first task", "Williard")

npc_list = []

npc_list.append(f_npc)

pygame.display.set_caption("The Story of Talizurk")

game_state = "roaming"

run = True

# Game Loop
while run:
    # **EVENT PHASE**
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Game state machine
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and nearby_npc is not None:
                game_state = "dialogue"
            if (event.key == pygame.K_y or event.key == pygame.K_n) and game_state == "dialogue":
                game_state = "roaming"
    
    # print(game_state)

    # **UPDATE PHASE**
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    # Player movement speed
    if keys[pygame.K_LSHIFT]:
        speed = 4
    else:
        speed = 8

   # HORIZONTAL PLAYER MOVEMENT
    if keys[pygame.K_a] and game_state == "roaming":
        player_rect.x -= speed
    if keys[pygame.K_d] and game_state == "roaming":
        player_rect.x += speed

    # RESOLVE PLYR HORIZ MVMNT
    for landmark in landmark_list:
        if player_rect.colliderect(landmark) and (keys[pygame.K_a] or keys[pygame.K_d]):
            if player_rect.x > landmark.x:
                player_rect.left = landmark.right
            if player_rect.x < landmark.x:
                player_rect.right = landmark.left

    # Horizontal collision detection for npc
    for npc in npc_list:
        if player_rect.colliderect(npc) and (keys[pygame.K_a] or keys[pygame.K_d]):
            if player_rect.x > npc.rect.x:
                player_rect.left = npc.rect.right
            if player_rect.x < npc.rect.x:
                player_rect.right = npc.rect.left

    # VERTICAL PLAYER MOVEMENT
    if keys[pygame.K_w] and game_state == "roaming":
        player_rect.y -= speed
    if keys[pygame.K_s] and game_state == "roaming":
        player_rect.y += speed

    # RESOLVE PLYR VERT MVMNT
    for landmark in landmark_list:
        if player_rect.colliderect(landmark) and (keys[pygame.K_w] or keys[pygame.K_s]):
            if player_rect.y > landmark.y:
                player_rect.top = landmark.bottom
            if player_rect.y < landmark.y:
                player_rect.bottom = landmark.top
    
    # Vertical collision detection for npc
    for npc in npc_list:
        if player_rect.colliderect(npc) and (keys[pygame.K_w] or keys[pygame.K_s]):
            if player_rect.y > npc.rect.y:
                player_rect.top = npc.rect.bottom
            if player_rect.y < npc.rect.y:
                player_rect.bottom = npc.rect.top

    # Checks if player is within npc range
    nearby_npc = None
    for npc in npc_list:
        if player_rect.colliderect(npc.hitbox):
            nearby_npc = npc

    player_rect.clamp_ip(pygame.Rect(0,0,WORLD_WIDTH,WORLD_HEIGHT))

    # Set up camera x & y offset
    camera_x = player_rect.centerx - (screen.get_width() // 2)
    camera_y = player_rect.centery - (screen.get_height() // 2)

    # Keeps camera from showing black void
    camera_x = max(0, min(camera_x, WORLD_WIDTH - screen.get_width()))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - screen.get_height()))

    # **DRAW PHASE**
    screen.fill((75, 140, 45))

    # Draw rocks
    for landmark in landmark_list:
        draw_landmark = landmark.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, 'Gray60', draw_landmark)

    # Draw npc hitbox -> debugging
    #for npc in npc_list:
    #    draw_npc_hitbox = npc.hitbox.move(-camera_x, -camera_y)
    #    pygame.draw.rect(screen, "lightblue1", draw_npc_hitbox)
    
    # Draw first npc
    draw_f_npc = f_npc.rect.move(-camera_x, -camera_y)
    pygame.draw.rect(screen, f_npc.color, draw_f_npc)

    # Draw player
    draw_player_rect = player_rect.move(-camera_x, -camera_y)
    pygame.draw.rect(screen, 'Brown4', draw_player_rect)

    # If player within npc range -> display prompt to speak with them
    if game_state == "roaming" and nearby_npc is not None:
            screen.blit(npc1_e2start, ((screen.get_width() / 2) - (npc1_e2start.width / 2), 150)) # first npc, first popup

    if game_state == "dialogue":
        screen.blit(npc1_task_desc, ((screen.get_width() / 2) - (npc1_task_desc.width / 2), 150))

    print(nearby_npc)
    # Updates the screen with anything changed by user events
    pygame.display.update()

    # Tells game loop to only run 60 times per second
    clock.tick(60)
