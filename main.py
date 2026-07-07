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
npc1_task_desc = dialogue_font.render("Touch the rectangle on the far side of the map. (y/n)", False, 'Black')
task1_obj_completion_msg1 = dialogue_font.render("You have completed Williard's task,", False, 'Black')
task1_obj_completion_msg2 = dialogue_font.render(" go back and see him for your reward.", False, 'Black')
williard_give_scrap1_msg1 = dialogue_font.render("Congratulations on completing your first quest,", False, 'Gold')
williard_give_scrap1_msg2 = dialogue_font.render("check your journal for your reward!", False, 'Gold')

nearby_npc = None
active_task = None

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

# Scraps
scrap1 = "Hear ye, hear ye, for now this region is settled in scorn!"

# Collected Scraps List
collected_scraps = []

# Completed Tasks
completed_tasks = []

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, color, dialogue_popup, name):
        super().__init__()
        self.rect = pygame.Rect(x, y, 65, 65)
        self.color = color
        self.dialogue_popup = dialogue_popup
        self.hitbox = self.rect.inflate(200,200)
        self.name = name
        
Williard = NPC(2000, 2600, 'Blue4', "Here is your first task", "Williard")

npc_list = []

npc_list.append(Williard)

pygame.display.set_caption("The Story of Talizurk")

game_state = "roaming"

williard_done = False

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
            if event.key == pygame.K_e and nearby_npc == "Williard":
                game_state = "dialogue"
            if (event.key == pygame.K_y or event.key == pygame.K_n) and game_state == "dialogue" and nearby_npc == "Williard":
                game_state = "working"
                task1_obj = pygame.Rect(4900, 4900, 100, 100)
                active_task = "Task 1"

    # **UPDATE PHASE**
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    # Player movement speed
    if keys[pygame.K_LSHIFT]:
        speed = 4
    elif keys[pygame.K_SPACE]:
        speed = 16
    else:
        speed = 8

   # HORIZONTAL PLAYER MOVEMENT
    if keys[pygame.K_a] and (game_state == "roaming" or game_state == "working"):
        player_rect.x -= speed
    if keys[pygame.K_d] and (game_state == "roaming" or game_state == "working"):
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
    if keys[pygame.K_w] and (game_state == "roaming" or game_state == "working"):
        player_rect.y -= speed
    if keys[pygame.K_s] and (game_state == "roaming" or game_state == "working"):
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
            nearby_npc = npc.name
    
    # Checks if task 1 has been completed, if it has, add it to completed tasks list and set active_task to None
    if game_state == "working" and player_rect.colliderect(task1_obj):
        completed_tasks.append(active_task)
        active_task = None
        game_state = "roaming"
    
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
    
    # Draw first npc, Williard
    draw_f_npc = Williard.rect.move(-camera_x, -camera_y)
    pygame.draw.rect(screen, Williard.color, draw_f_npc)

    # Draw player
    draw_player_rect = player_rect.move(-camera_x, -camera_y)
    pygame.draw.rect(screen, 'Brown4', draw_player_rect)

    # Draw objective for task 1
    if game_state == "working" and active_task == "Task 1":
        draw_task1_obj = task1_obj.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, 'Yellow', draw_task1_obj)

    # WILLIARD INTERACTIONS
    # If player within npc range -> display prompt to speak with them
    if game_state == "roaming" and nearby_npc == "Williard" and not ("Task 1" in completed_tasks):
            screen.blit(npc1_e2start, ((screen.get_width() / 2) - (npc1_e2start.width / 2), 150)) # first npc, first popup

    if game_state == "dialogue" and nearby_npc == "Williard":
        screen.blit(npc1_task_desc, ((screen.get_width() / 2) - (npc1_task_desc.width / 2), 150))

    if game_state == "roaming" and nearby_npc == "Williard" and ("Task 1" in completed_tasks):
        screen.blit(williard_give_scrap1_msg1, ((screen.get_width() / 2) - (williard_give_scrap1_msg1.width / 2), 150))
        screen.blit(williard_give_scrap1_msg2, ((screen.get_width() / 2) - (williard_give_scrap1_msg2.width / 2), 150 + (williard_give_scrap1_msg2.height)))

        # Williard vanish or otherwise be of no use anymore added here eventually

    # Same as above, but only adds scrap 1 to collected_scraps list once
    if game_state == "roaming" and nearby_npc == "Williard" and ("Task 1" in completed_tasks) and not williard_done: 
        collected_scraps.append(scrap1) # Add "reward" (Scrap 1) to list of collected scraps for journal
        williard_done = True

    if "Task 1" in completed_tasks and (not (nearby_npc == "Williard")) and not collected_scraps:
        screen.blit(task1_obj_completion_msg1, ((screen.get_width() / 2) - (task1_obj_completion_msg1.width / 2), 150))
        screen.blit(task1_obj_completion_msg2, ((screen.get_width() / 2) - (task1_obj_completion_msg2.width / 2), 150 + (task1_obj_completion_msg2.height)))
    
    # DEBUG:
    # -------------------------
    # Print nearby npc, none if not near any
    print(nearby_npc)
    # Print completed tasks list
    print(completed_tasks)
    # Print collected scraps list
    print(collected_scraps)

    # Updates the screen with anything changed by user events
    pygame.display.update()

    # Tells game loop to only run 60 times per second
    clock.tick(60)
