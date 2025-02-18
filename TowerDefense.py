import pygame


grid_size = 50
num_row = 8
num_column = 12
screen_width = grid_size*num_column
screen_height = grid_size*num_row
screen = pygame.display.set_mode([screen_width, screen_height])

grass_block = pygame.image.load('grass_block.png')
grass_block = pygame.transform.scale(grass_block, (grid_size, grid_size))
tank = pygame.image.load('tank.png')
gun=pygame.image.load('gun.png')
path_block = pygame.image.load('grass.png')
path_block = pygame.transform.scale(path_block, (grid_size, grid_size))

map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0] ]

path = [ [7,0], [7,1], [7,2], [7,3], [7,4], [7,5], [7,6], [7,7], [7,8], [6,8], [5,8], [4,8], [4,9], [4,10], [3,10], [2,10], [1,10], [1,11], [0,11],[-1,11]]

def move_to(object1, object2, cx, cy, goal_x, goal_y, num_steps):
    rect = object1.get_rect()
    cx += (goal_x - cx)/num_steps
    cy += (goal_y - cy)/num_steps
    rect.center = (cx, cy)
    screen.blit(object1, rect)
    screen.blit(object2, rect)
    return cx, cy

def draw_map():
    for b in range(num_row):
        grid_y = b*grid_size
        for j in range(num_column):
            grid_x = j*grid_size
            if map[b][j] == 0:
                screen.blit(path_block, (grid_x, grid_y))
            else:
                screen.blit(grass_block, (grid_x, grid_y))
        pygame.display.update()

Running = True
draw_map()

def draw_enemy(enemy):
    tank = enemy[0]
    num_steps = enemy[1]
    cx = enemy[2]
    cy = enemy[3]
    old_direction = enemy[4]
    goal_x = enemy[5]
    goal_y = enemy[6]
    i = enemy[7]
    if num_steps > 1:
        num_steps -= 1
    else:
        if i < len(path)-1:
            i += 1
            num_steps = 30
            goal_y = path[i][0]*grid_size+grid_size/2
            goal_x = path[i][1]*grid_size+grid_size/2
            direction = 0
            if goal_y > cy + 1:
                direction = 90
            if goal_y < cy-1:
                direction = -90
            if goal_x < cx - 1:
                direction = 180
            tank = pygame.transform.rotate(tank, direction-old_direction)
            old_direction = direction
            cx, cy = move_to(tank, tank, cx, cy, goal_x, goal_y, num_steps)
            print("calling move_to with",cx,cy,goal_x,goal_y,num_steps)
            #enemy[0] = tank
            #enemy[4]=old_direction
            #enemy[5] = goal_x
            #enemy[6] = goal_y
            #enemy[7] = i
            enemy[1] = num_steps
            enemy[2] = cx
            enemy[3] = cy
        else:
            return False

enemy_list = []
#enemy_list = [enemy]
last_time = 0
num_enemy = 5
enemy_counter = 0
while(Running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    if pygame.time.get_ticks() - last_time > 2000 and enemy_counter < num_enemy:
        enemy_list.append([tank, 0, -40, 520, 0, 0, 0, -1])
        last_time = pygame.time.get_ticks()
        enemy_counter += 1
        print(last_time)
        print("Added enemy number ",enemy_counter)
    draw_map()
    for enemy in enemy_list:
        draw_enemy(enemy)
    pygame.time.Clock().tick(30)
    pygame.display.update()
